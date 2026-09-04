import hashlib


def generate_evidence_id(
    relationship_id,
    observation_ids,
    evidence_type
):
    """
    Generate a stable, deterministic evidence ID.
    """

    raw = (
        f"{relationship_id}|"
        f"{'|'.join(sorted(observation_ids))}|"
        f"{evidence_type}"
    )

    digest = hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()[:12]

    return f"EVID-{digest.upper()}"