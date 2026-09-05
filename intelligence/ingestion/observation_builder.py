from datetime import datetime, timezone
import hashlib

from ..models.observations import Observation


def _calculate_sha256(content: str) -> str:
    """
    Calculate SHA-256 hash of the observation content.
    """
    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def build_observations(records, source_reliability=0.5):
    """
    Convert validated intelligence records into
    Observation objects with provenance and integrity metadata.
    """

    observations = []

    collection_time = datetime.now(timezone.utc).isoformat()

    for index, record in enumerate(records, start=1):

        content = record["content"]

        observation = Observation(
            observation_id=f"OBS-{index:03d}",

            source=record["source"],

            content=content,

            observed_at=record.get("observed_at"),

            source_reliability=source_reliability,

            # ------------------------------------------
            # Provenance
            # ------------------------------------------

            source_type=record.get(
                "source_type",
                "unknown"
            ),

            collection_method=record.get(
                "collection_method",
                "unknown"
            ),

            collection_time=record.get(
                "collection_time",
                collection_time
            ),

            source_reference=record.get(
                "source_reference"
            ),

            original_timestamp=record.get(
                "original_timestamp",
                record.get("observed_at")
            ),

            # ------------------------------------------
            # Integrity
            # ------------------------------------------

            content_hash=_calculate_sha256(content),

            integrity_status=record.get(
                "integrity_status",
                "UNVERIFIED"
            )
        )

        observations.append(observation)

    return observations