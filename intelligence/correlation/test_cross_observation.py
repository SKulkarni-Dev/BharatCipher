from intelligence.models.entities import Entity
from intelligence.models.observations import Observation


# ------------------------------------------
# Observation 1
# ------------------------------------------

obs1_entities = [

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
    )
]


obs1 = Observation(
    observation_id="OBS-001",
    source="dataset_A",
    content="shadowX was associated with PGP-A.",
    observed_at="2026-08-28T10:00:00Z",
    source_reliability=0.90,
    entity_ids=[
        entity.entity_id
        for entity in obs1_entities
    ]
)


# ------------------------------------------
# Observation 2
# ------------------------------------------

obs2_entities = [

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
    )
]


obs2 = Observation(
    observation_id="OBS-002",
    source="dataset_B",
    content="shadow_88 was associated with PGP-A.",
    observed_at="2026-08-29T14:30:00Z",
    source_reliability=0.85,
    entity_ids=[
        entity.entity_id
        for entity in obs2_entities
    ]
)


# ------------------------------------------
# Observation 3
# ------------------------------------------

obs3_entities = [

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


obs3 = Observation(
    observation_id="OBS-003",
    source="dataset_C",
    content="darkfox was associated with PGP-B.",
    observed_at="2026-08-30T08:00:00Z",
    source_reliability=0.90,
    entity_ids=[
        entity.entity_id
        for entity in obs3_entities
    ]
)


# ------------------------------------------
# Print observations
# ------------------------------------------

observations = [
    obs1,
    obs2,
    obs3
]


print("CROSS-OBSERVATION DATASET")
print("-------------------------")

for observation in observations:

    print(
        f"{observation.observation_id} | "
        f"{observation.source} | "
        f"Entities: {observation.entity_ids}"
    )