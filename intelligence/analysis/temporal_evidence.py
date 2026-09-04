from ..models.evidence import Evidence


def build_temporal_evidence(
    entity_a_id,
    entity_b_id,
    observations_a,
    observations_b,
    temporal_result
):
    """
    Convert temporal analysis into structured evidence.

    Temporal overlap is supporting evidence.
    Temporal consistency without overlap is neutral.
    Temporal conflict is contradicting evidence only
    when explicitly established by the analysis.
    """

    if temporal_result == "INSUFFICIENT_DATA":
        return None

    if temporal_result == "TEMPORALLY_OVERLAPPING":

        evidence_type = "TEMPORAL_OVERLAP"

        description = (
            "The activity periods of the two "
            "identities overlap."
        )

        strength = 0.60

    elif temporal_result == "TEMPORALLY_CONSISTENT":

        # Non-overlapping activity does not prove
        # that the identities are different.
        return None

    elif temporal_result == "TEMPORALLY_CONFLICTING":

        evidence_type = "TEMPORAL_CONFLICT"

        description = (
            "The observed activity timeline "
            "contains a temporal conflict."
        )

        strength = 0.70

    else:
        return None

    all_observations = (
        observations_a +
        observations_b
    )

    observation_ids = [
        observation.observation_id
        for observation in all_observations
    ]

    sources = list(
        dict.fromkeys(
            observation.source
            for observation in all_observations
        )
    )

    reliability_values = [
        observation.source_reliability
        for observation in all_observations
        if observation.source_reliability is not None
    ]

    if reliability_values:

        reliability = (
            sum(reliability_values)
            / len(reliability_values)
        )

    else:

        reliability = 0.0

    return Evidence(

        evidence_id="TEMPORAL-" + (
            f"{entity_a_id[-6:]}"
            f"-"
            f"{entity_b_id[-6:]}"
        ),

        evidence_type=evidence_type,

        description=description,

        source="temporal_analysis",

        observed_at=(
            all_observations[-1].observed_at
            if all_observations
            else None
        ),

        entity_ids=[
            entity_a_id,
            entity_b_id
        ],

        reliability=round(
            reliability,
            4
        ),

        strength=strength,

        metadata={
            "temporal_result": temporal_result,
            "observation_ids": observation_ids,
            "sources": sources
        }
    )