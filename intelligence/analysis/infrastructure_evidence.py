from ..models.evidence import Evidence


def build_infrastructure_evidence(
    entity_a_id,
    entity_b_id,
    observations_a,
    observations_b,
    shared_infrastructure
):
    """
    Convert shared infrastructure into evidence.

    Multiple shared infrastructure indicators
    are represented as separate evidence objects.
    """

    if not shared_infrastructure:
        return []

    all_observations = (
        observations_a
        +
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
            /
            len(reliability_values)
        )

    else:

        reliability = 0.0

    evidence = []

    for infrastructure in shared_infrastructure:

        infrastructure_type = (
            infrastructure.entity_type.upper()
        )

        evidence.append(

            Evidence(

                evidence_id=(
                    "INFRA-"
                    f"{entity_a_id[-6:]}"
                    "-"
                    f"{entity_b_id[-6:]}"
                    "-"
                    f"{infrastructure.entity_id[-6:]}"
                ),

                evidence_type=(
                    f"SHARED_{infrastructure_type}"
                ),

                description=(
                    f"The same {infrastructure.entity_type} "
                    f"'{infrastructure.value}' was observed "
                    f"across both identities."
                ),

                source="infrastructure_analysis",

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

                strength=0.65,

                metadata={

                    "shared_infrastructure": (
                        infrastructure.value
                    ),

                    "infrastructure_type": (
                        infrastructure.entity_type
                    ),

                    "observation_ids": (
                        observation_ids
                    ),

                    "sources": sources
                }
            )
        )

    return evidence
