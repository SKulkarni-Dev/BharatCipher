from intelligence.ingestion.loader import load_json
from intelligence.ingestion.validator import validate_records
from intelligence.ingestion.observation_builder import build_observations


# Load
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


print("OBSERVATIONS CREATED")
print("--------------------")

for observation in observations:

    print(
        f"{observation.observation_id} | "
        f"{observation.source} | "
        f"{observation.observed_at}"
    )

    print(
        f"Content: {observation.content}"
    )

    print(
        f"Reliability: "
        f"{observation.source_reliability}"
    )

    print()