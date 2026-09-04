import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

DB_PATH = Path(__file__).resolve().parent.parent / "sih26151.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _migrate_legacy_single_key_schema(conn):
    """
    One-time migration for databases created before IDs were scoped
    per-investigation.

    observation_id / relationship_id / hypothesis_id are per-run
    sequential counters (OBS-001, REL-001, HYP-001, ...) and
    entity_id / evidence_id are deterministic content hashes, so the
    same ID can legitimately appear in more than one investigation.
    Older versions of this schema declared these columns as a
    standalone PRIMARY KEY, which made a second investigation crash
    with "UNIQUE constraint failed" as soon as it reused any ID.

    This detects that legacy layout and rebuilds each affected table
    with a composite (investigation_id, id) primary key, copying all
    existing rows across first so no investigation data is lost.
    """

    tables = {
        "observations": "observation_id",
        "entities": "entity_id",
        "relationships": "relationship_id",
        "evidence": "evidence_id",
        "hypotheses": "hypothesis_id",
    }

    for table, id_column in tables.items():

        exists = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name=?",
            (table,)
        ).fetchone()

        if not exists:
            continue

        columns = conn.execute(
            f"PRAGMA table_info({table})"
        ).fetchall()

        id_col_info = next(
            (c for c in columns if c["name"] == id_column),
            None
        )

        investigation_col_info = next(
            (c for c in columns if c["name"] == "investigation_id"),
            None
        )

        is_legacy = (
            id_col_info is not None
            and id_col_info["pk"] == 1
            and (
                investigation_col_info is None
                or investigation_col_info["pk"] == 0
            )
        )

        if not is_legacy:
            continue

        conn.execute(f"ALTER TABLE {table} RENAME TO {table}_legacy")

        # Re-run the create step for just this table by dropping it
        # from the "already exists" check next time initialize runs.
        conn.execute(f"DROP TABLE IF EXISTS {table}")

        conn.commit()

        # Table will be (re)created with the new schema by the
        # CREATE TABLE IF NOT EXISTS statements that follow, so run
        # those first, then copy the old data across.
        _create_tables(conn)

        column_names = ", ".join(c["name"] for c in columns)

        conn.execute(
            f"INSERT INTO {table} ({column_names}) "
            f"SELECT {column_names} FROM {table}_legacy"
        )

        conn.execute(f"DROP TABLE {table}_legacy")

        conn.commit()


def _create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS investigations (
            investigation_id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS observations (
            observation_id TEXT NOT NULL,
            investigation_id TEXT NOT NULL,
            source TEXT NOT NULL,
            content TEXT NOT NULL,
            observed_at TEXT,
            source_reliability REAL DEFAULT 0.0,
            metadata TEXT,
            PRIMARY KEY (investigation_id, observation_id),
            FOREIGN KEY (investigation_id)
                REFERENCES investigations(investigation_id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS entities (
            entity_id TEXT NOT NULL,
            investigation_id TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            value TEXT NOT NULL,
            source TEXT,
            first_seen TEXT,
            last_seen TEXT,
            metadata TEXT,
            PRIMARY KEY (investigation_id, entity_id),
            FOREIGN KEY (investigation_id)
                REFERENCES investigations(investigation_id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS relationships (
            relationship_id TEXT NOT NULL,
            investigation_id TEXT NOT NULL,
            source_entity_id TEXT NOT NULL,
            target_entity_id TEXT NOT NULL,
            relationship_type TEXT NOT NULL,
            strength REAL DEFAULT 0.0,
            evidence_ids TEXT,
            source TEXT,
            metadata TEXT,
            PRIMARY KEY (investigation_id, relationship_id),
            FOREIGN KEY (investigation_id)
                REFERENCES investigations(investigation_id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS evidence (
            evidence_id TEXT NOT NULL,
            investigation_id TEXT NOT NULL,
            evidence_type TEXT NOT NULL,
            description TEXT NOT NULL,
            source TEXT NOT NULL,
            observed_at TEXT,
            entity_ids TEXT,
            reliability REAL DEFAULT 0.0,
            strength REAL DEFAULT 0.0,
            metadata TEXT,
            PRIMARY KEY (investigation_id, evidence_id),
            FOREIGN KEY (investigation_id)
                REFERENCES investigations(investigation_id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS hypotheses (
            hypothesis_id TEXT NOT NULL,
            investigation_id TEXT NOT NULL,
            description TEXT NOT NULL,
            entity_ids TEXT,
            supporting_evidence_ids TEXT,
            contradicting_evidence_ids TEXT,
            confidence REAL DEFAULT 0.0,
            assessment TEXT DEFAULT 'UNASSESSED',
            metadata TEXT,
            PRIMARY KEY (investigation_id, hypothesis_id),
            FOREIGN KEY (investigation_id)
                REFERENCES investigations(investigation_id)
                ON DELETE CASCADE
        );
    """)

    conn.commit()


def initialize_database():
    conn = get_connection()

    _migrate_legacy_single_key_schema(conn)

    _create_tables(conn)

    conn.close()


def save_investigation(result):
    from intelligence.output.serializer import investigation_to_dict

    serialized = investigation_to_dict(result)

    investigation_id = f"INV-{uuid4().hex.upper()}"
    created_at = datetime.now(timezone.utc).isoformat()

    conn = get_connection()

    try:
        conn.execute(
            """
            INSERT INTO investigations
            (investigation_id, created_at)
            VALUES (?, ?)
            """,
            (investigation_id, created_at)
        )

        # Observations
        for observation in serialized.get("observations", []):
            conn.execute(
                """
                INSERT INTO observations
                (
                    observation_id,
                    investigation_id,
                    source,
                    content,
                    observed_at,
                    source_reliability,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    observation["observation_id"],
                    investigation_id,
                    observation["source"],
                    observation["content"],
                    observation.get("observed_at"),
                    observation.get("source_reliability", 0.0),
                    json.dumps(observation.get("metadata", {}))
                )
            )

        # Entities
        for entity in serialized.get("entities", []):
            conn.execute(
                """
                INSERT INTO entities
                (
                    entity_id,
                    investigation_id,
                    entity_type,
                    value,
                    source,
                    first_seen,
                    last_seen,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entity["entity_id"],
                    investigation_id,
                    entity["entity_type"],
                    entity["value"],
                    entity.get("source"),
                    entity.get("first_seen"),
                    entity.get("last_seen"),
                    json.dumps(entity.get("metadata", {}))
                )
            )

        # Relationships
        for relationship in serialized.get("relationships", []):
            conn.execute(
                """
                INSERT INTO relationships
                (
                    relationship_id,
                    investigation_id,
                    source_entity_id,
                    target_entity_id,
                    relationship_type,
                    strength,
                    evidence_ids,
                    source,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    relationship["relationship_id"],
                    investigation_id,
                    relationship["source_entity_id"],
                    relationship["target_entity_id"],
                    relationship["relationship_type"],
                    relationship.get("strength", 0.0),
                    json.dumps(relationship.get("evidence_ids", [])),
                    relationship.get("source"),
                    json.dumps(relationship.get("metadata", {}))
                )
            )

        # Evidence
        for item in serialized.get("evidence", []):
            conn.execute(
                """
                INSERT INTO evidence
                (
                    evidence_id,
                    investigation_id,
                    evidence_type,
                    description,
                    source,
                    observed_at,
                    entity_ids,
                    reliability,
                    strength,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item["evidence_id"],
                    investigation_id,
                    item["evidence_type"],
                    item["description"],
                    item["source"],
                    item.get("observed_at"),
                    json.dumps(item.get("entity_ids", [])),
                    item.get("reliability", 0.0),
                    item.get("strength", 0.0),
                    json.dumps(item.get("metadata", {}))
                )
            )

        # Hypotheses
        for hypothesis in serialized.get("hypotheses", []):
            conn.execute(
                """
                INSERT INTO hypotheses
                (
                    hypothesis_id,
                    investigation_id,
                    description,
                    entity_ids,
                    supporting_evidence_ids,
                    contradicting_evidence_ids,
                    confidence,
                    assessment,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    hypothesis["hypothesis_id"],
                    investigation_id,
                    hypothesis["description"],
                    json.dumps(hypothesis.get("entity_ids", [])),
                    json.dumps(
                        hypothesis.get("supporting_evidence_ids", [])
                    ),
                    json.dumps(
                        hypothesis.get("contradicting_evidence_ids", [])
                    ),
                    hypothesis.get("confidence", 0.0),
                    hypothesis.get("assessment", "UNASSESSED"),
                    json.dumps(hypothesis.get("metadata", {}))
                )
            )

        conn.commit()

        return investigation_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def get_investigations():
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT investigation_id, created_at
        FROM investigations
        ORDER BY created_at DESC
        """
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_investigation(investigation_id):
    conn = get_connection()

    investigation = conn.execute(
        """
        SELECT investigation_id, created_at
        FROM investigations
        WHERE investigation_id = ?
        """,
        (investigation_id,)
    ).fetchone()

    if not investigation:
        conn.close()
        return None

    result = {
        "investigation_id": investigation["investigation_id"],
        "created_at": investigation["created_at"],
        "observations": [],
        "entities": [],
        "relationships": [],
        "evidence": [],
        "hypotheses": []
    }

    # Observations
    rows = conn.execute(
        """
        SELECT *
        FROM observations
        WHERE investigation_id = ?
        """,
        (investigation_id,)
    ).fetchall()

    for row in rows:
        item = dict(row)
        item["metadata"] = json.loads(item["metadata"] or "{}")
        result["observations"].append(item)

    # Entities
    rows = conn.execute(
        """
        SELECT *
        FROM entities
        WHERE investigation_id = ?
        """,
        (investigation_id,)
    ).fetchall()

    for row in rows:
        item = dict(row)
        item["metadata"] = json.loads(item["metadata"] or "{}")
        result["entities"].append(item)

    # Relationships
    rows = conn.execute(
        """
        SELECT *
        FROM relationships
        WHERE investigation_id = ?
        """,
        (investigation_id,)
    ).fetchall()

    for row in rows:
        item = dict(row)
        item["evidence_ids"] = json.loads(
            item["evidence_ids"] or "[]"
        )
        item["metadata"] = json.loads(
            item["metadata"] or "{}"
        )
        result["relationships"].append(item)

    # Evidence
    rows = conn.execute(
        """
        SELECT *
        FROM evidence
        WHERE investigation_id = ?
        """,
        (investigation_id,)
    ).fetchall()

    for row in rows:
        item = dict(row)
        item["entity_ids"] = json.loads(
            item["entity_ids"] or "[]"
        )
        item["metadata"] = json.loads(
            item["metadata"] or "{}"
        )
        result["evidence"].append(item)

    # Hypotheses
    rows = conn.execute(
        """
        SELECT *
        FROM hypotheses
        WHERE investigation_id = ?
        """,
        (investigation_id,)
    ).fetchall()

    for row in rows:
        item = dict(row)
        item["entity_ids"] = json.loads(
            item["entity_ids"] or "[]"
        )
        item["supporting_evidence_ids"] = json.loads(
            item["supporting_evidence_ids"] or "[]"
        )
        item["contradicting_evidence_ids"] = json.loads(
            item["contradicting_evidence_ids"] or "[]"
        )
        item["metadata"] = json.loads(
            item["metadata"] or "{}"
        )
        result["hypotheses"].append(item)

    conn.close()

    return result
def create_case(title, description=""):
    case_id = f"CASE-{uuid4().hex[:8].upper()}"
    created_at = datetime.now(timezone.utc).isoformat()

    conn = get_connection()

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute(
            """
            INSERT INTO cases
            (case_id, title, description, status, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                case_id,
                title,
                description,
                "active",
                created_at
            )
        )

        conn.commit()

        return {
            "case_id": case_id,
            "title": title,
            "description": description,
            "status": "active",
            "created_at": created_at
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def get_cases():
    conn = get_connection()

    try:
        # Create table if it does not already exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        rows = conn.execute(
            """
            SELECT
                case_id,
                title,
                description,
                status,
                created_at
            FROM cases
            ORDER BY created_at DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()

initialize_database()