from ..models.evidence import Evidence
from ..models.relationships import Relationship
from ..models.observations import Observation
from .id_generator import generate_evidence_id


def build_evidence(
    relationship,
    observations,
    entities
):
    """
    Create an Evidence object from a discovered
    relationship.

    The evidence keeps the complete provenance:
    relationship → observations → sources.
    """

    entity_map = {
        entity.entity_id: entity
        for entity in entities
    }

    observation_map = {
        observation.observation_id: observation
        for observation in observations
    }

    source_observation_ids = (
        relationship.metadata.get(
            "observation_ids",
            []
        )
    )

    related_entities = [
        relationship.source_entity_id,
        relationship.target_entity_id
    ]

    shared_indicator = relationship.metadata.get(
        "shared_indicator",
        "unknown"
    )

    relationship_type = (
        relationship.relationship_type
    )

    # ------------------------------------------
    # Calculate evidence reliability
    # ------------------------------------------

    reliability_values = []

    for observation_id in source_observation_ids:

        observation = observation_map.get(
            observation_id
        )

        if observation:

            reliability_values.append(
                observation.source_reliability
            )

    if reliability_values:

        reliability = sum(
            reliability_values
        ) / len(reliability_values)

    else:

        reliability = 0.0

    # ------------------------------------------
    # Evidence strength
    # ------------------------------------------

    strength = relationship.strength

    # ------------------------------------------
    # Description
    # ------------------------------------------

    description = (
        f"The same "
        f"{relationship_type.replace('SHARES_', '').lower()} "
        f"indicator '{shared_indicator}' was observed "
        f"across multiple observations."
    )

    # ------------------------------------------
    # Generate stable evidence ID
    # ------------------------------------------

    evidence_id = generate_evidence_id(
        relationship.relationship_id,
        source_observation_ids,
        relationship_type
    )

    # ------------------------------------------
    # Create Evidence
    # ------------------------------------------

    evidence = Evidence(

        evidence_id=evidence_id,

        evidence_type=relationship_type,

        description=description,

        source=relationship.source,

        observed_at=(
            observation_map[
                source_observation_ids[0]
            ].observed_at
            if source_observation_ids
            and source_observation_ids[0]
            in observation_map
            else None
        ),

        entity_ids=related_entities,

        reliability=round(
            reliability,
            4
        ),

        strength=strength,

        metadata={

            "shared_indicator": (
                shared_indicator
            ),

            "relationship_id": (
                relationship.relationship_id
            ),

            "observation_ids": (
                source_observation_ids
            ),

            "sources": (
                relationship.metadata.get(
                    "sources",
                    []
                )
            )
        }
    )

    return evidence