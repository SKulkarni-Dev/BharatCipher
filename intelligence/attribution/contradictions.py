from ..models.evidence import Evidence


def find_contradictions(
    hypothesis,
    evidence
):
    """
    Identify evidence that contradicts
    an attribution hypothesis.

    This is a rule-based baseline.
    """

    contradictions = []

    hypothesis_entities = set(
        hypothesis.entity_ids
    )

    for item in evidence:

        evidence_entities = set(
            item.entity_ids
        )

        # Evidence must concern the same
        # entities as the hypothesis.
        if not hypothesis_entities.issubset(
            evidence_entities
        ):
            continue

        evidence_type = (
            item.evidence_type.upper()
        )

        # Explicit contradiction
        if evidence_type in {
            "CONTRADICTION",
            "CONFLICT",
            "DIFFERENT_INFRASTRUCTURE",
            "TEMPORAL_CONFLICT",
            "BEHAVIOR_CONFLICT"
        }:

            contradictions.append(item)

    return contradictions