from sqlite_db import save_investigation


test_result = {
    "records": [
        {
            "record_id": "TEST-001",
            "source": "test_source",
            "content": "Test investigation"
        }
    ],
    "valid_records": [
        {
            "record_id": "TEST-001",
            "source": "test_source",
            "content": "Test investigation"
        }
    ],
    "validation_errors": [],
    "observations": [],
    "entities": [],
    "relationships": [],
    "evidence": [],
    "hypotheses": []
}


investigation_id = save_investigation(
    test_result
)


print()
print("==============================")
print("DATABASE TEST")
print("==============================")
print(
    f"Investigation saved: "
    f"{investigation_id}"
)