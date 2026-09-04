from intelligence.ingestion.loader import load_json
from intelligence.ingestion.validator import validate_records
from intelligence.ingestion.observation_builder import build_observations
from intelligence.ingestion.entity_builder import attach_entities_to_observation


# Load dataset
from pathlib import Path

records = load_json(
    str(Path(__file__).parent / "test_data.json")
)

# Validate
valid_records, errors = validate_records(
    records
)

# Build observations
observations = build_observations(
    valid_records,
    source_reliability=0.85
)


print("OBSERVATION → ENTITY PIPELINE")
print("=============================")


all_entities = []


for observation in observations:

    entities = attach_entities_to_observation(
        observation
    )

    all_entities.extend(entities)

    print(
        f"\n{observation.observation_id}"
    )

    print(
        f"Source: {observation.source}"
    )

    print(
        f"Entity IDs: {observation.entity_ids}"
    )

    for entity in entities:

        print(
            f"  {entity.entity_type}: "
            f"{entity.value}"
        )


print("\nTOTAL ENTITIES")
print("--------------")
print(len(all_entities))
