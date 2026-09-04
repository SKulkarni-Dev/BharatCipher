from intelligence.ingestion.loader import load_json
from intelligence.ingestion.validator import validate_records


from pathlib import Path

file_path = str(Path(__file__).parent / "test_data.json")


# ------------------------------------------
# Load dataset
# ------------------------------------------

records = load_json(file_path)


print("LOADED RECORDS")
print("--------------")
print(f"Total: {len(records)}")


# ------------------------------------------
# Validate dataset
# ------------------------------------------

valid_records, errors = validate_records(
    records
)


print("\nVALID RECORDS")
print("-------------")

for record in valid_records:

    print(
        f"{record['source']} | "
        f"{record['content']}"
    )


print("\nINVALID RECORDS")
print("---------------")

for error in errors:

    print(
        f"Record {error['index']}: "
        f"{error['error']}"
    )