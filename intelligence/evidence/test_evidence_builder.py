from intelligence.models.entities import Entity
from intelligence.models.observations import Observation

from intelligence.correlation.correlator import correlate_observations
from intelligence.evidence.evidence_builder import build_evidence


# ------------------------------------------
# Entities
# ------------------------------------------
entities = [

    Entity(
        entity_id="ENT-DBCECA8B1A13",
        entity_type="username",
        value="shadowX",
        source="dataset_A"
    ),

    Entity(
        entity_id="ENT-FBD46245BCA1",
        entity_type="pgp",
        value="PGP-A",
        source="dataset_A"
    ),

    Entity(
        entity_id="ENT-E73C4E1171F6",
        entity_type="username",
        value="shadow_88",
        source="dataset_B"
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
            "ENT-DBCECA8B1A13",
            "ENT-FBD46245BCA1"
        ]
    ),

    Observation(
        observation_id="OBS-002",
        source="dataset_B",
        content="shadow_88 was associated with PGP-A.",
        observed_at="2026-08-29T14:30:00Z",
        source_reliability=0.80,
        entity_ids=[
            "ENT-E73C4E1171F6",
            "ENT-FBD46245BCA1"
        ]
    )
]


# ------------------------------------------
# Correlate
# ------------------------------------------

relationships = correlate_observations(
    observations,
    entities
)


print("RELATIONSHIPS")
print("-------------")

for relationship in relationships:

    print(
        f"{relationship.source_entity_id} "
        f"--[{relationship.relationship_type}]--> "
        f"{relationship.target_entity_id}"
    )


# ------------------------------------------
# Build evidence
# ------------------------------------------

print("\nEVIDENCE")
print("--------")


for relationship in relationships:

    evidence = build_evidence(
        relationship,
        observations,
        entities
    )

    print(evidence)