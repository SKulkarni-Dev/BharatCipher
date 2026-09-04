import json
from pathlib import Path

from intelligence.investigation_engine import investigate_dataset

from intelligence.output.serializer import (
    investigation_to_dict
)


result = investigate_dataset(
    str(Path(__file__).parent.parent / "ingestion" / "test_data.json")
)

json_result = investigation_to_dict(
    result
)

print(
    json.dumps(
        json_result,
        indent=2
    )
)