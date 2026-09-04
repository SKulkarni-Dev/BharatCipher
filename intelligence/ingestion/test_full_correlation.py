from intelligence.ingestion.loader import load_json
from intelligence.ingestion.validator import validate_records
from intelligence.ingestion.observation_builder import build_observations
from intelligence.ingestion.entity_builder import attach_entities_to_observation

from intelligence.correlation.correlator import correlate_observations


# ------------------------------------------
# 1. Load dataset
# ------------------------------------------

from pathlib import Path

records = load_json(
    str(Path(__file__).parent / "test_data.json")
)


# ------------------------------------------
# 2. Validate
# ------------------------------------------

valid_records, errors = validate_records(
    records
)


# ------------------------------------------
# 3. Build observations
# ------------------------------------------

observations = build_observations(
    valid_records,
    source_reliability=0.85
)


# ------------------------------------------
# 4. Extract entities
# ------------------------------------------

all_entities = []

for observation in observations:

    entities = attach_entities_to_observation(
        observation
    )

    all_entities.extend(entities)


# ------------------------------------------
# 5. Cross-observation correlation
# ------------------------------------------

relationships = correlate_observations(
    observations,
    all_entities
)


# ------------------------------------------
# 6. Display results
# ------------------------------------------

print("======================================")
print("FULL CROSS-OBSERVATION CORRELATION")
print("======================================")


print("\nOBSERVATIONS")
print("------------")

for observation in observations:

    print(
        f"{observation.observation_id} | "
        f"{observation.source} | "
        f"{observation.entity_ids}"
    )


print("\nRELATIONSHIPS")
print("-------------")


if not relationships:

    print("No relationships found.")

else:

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

        print(
            f"Sources: "
            f"{relationship.metadata['sources']}"
        )

        print()