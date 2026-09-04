from intelligence.models.entities import Entity
from intelligence.models.observations import Observation

from intelligence.correlation.correlator import correlate_observations


# ------------------------------------------
# Entities
# ------------------------------------------

entities = [

    Entity(
        entity_id="ENT-001",
        entity_type="username",
        value="shadowX",
        source="dataset_A"
    ),

    Entity(
        entity_id="ENT-002",
        entity_type="pgp",
        value="PGP-A",
        source="dataset_A"
    ),

    Entity(
        entity_id="ENT-003",
        entity_type="username",
        value="shadow_88",
        source="dataset_B"
    ),

    Entity(
        entity_id="ENT-004",
        entity_type="pgp",
        value="PGP-A",
        source="dataset_B"
    ),

    Entity(
        entity_id="ENT-005",
        entity_type="username",
        value="darkfox",
        source="dataset_C"
    ),

    Entity(
        entity_id="ENT-006",
        entity_type="pgp",
        value="PGP-B",
        source="dataset_C"
    )
]


# ------------------------------------------
# Observations
# ------------------------------------------

observations = [

    Observation(
        observation_id="OBS-001",
        source="dataset_A",
        content="shadowX was associated with PGP-A.",
        observed_at="2026-08-28T10:00:00Z",
        source_reliability=0.90,
        entity_ids=[
            "ENT-001",
            "ENT-002"
        ]
    ),

    Observation(
        observation_id="OBS-002",
        source="dataset_B",
        content="shadow_88 was associated with PGP-A.",
        observed_at="2026-08-29T14:30:00Z",
        source_reliability=0.85,
        entity_ids=[
            "ENT-003",
            "ENT-004"
        ]
    ),

    Observation(
        observation_id="OBS-003",
        source="dataset_C",
        content="darkfox was associated with PGP-B.",
        observed_at="2026-08-30T08:00:00Z",
        source_reliability=0.90,
        entity_ids=[
            "ENT-005",
            "ENT-006"
        ]
    )
]


# ------------------------------------------
# Run correlation
# ------------------------------------------

relationships = correlate_observations(
    observations,
    entities
)


print("CROSS-OBSERVATION CORRELATION")
print("-----------------------------")


for relationship in relationships:

    print(
        f"{relationship.source_entity_id} "
        f"--[{relationship.relationship_type}]--> "
        f"{relationship.target_entity_id}"
    )

    print(
        f"Shared indicator: "
        f"{relationship.metadata['shared_indicator']}"
    )

    print(
        f"Observations: "
        f"{relationship.metadata['observation_ids']}"
    )

    print()