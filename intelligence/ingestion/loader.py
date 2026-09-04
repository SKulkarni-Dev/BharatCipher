import json
from pathlib import Path


def load_json(file_path):
    """
    Load intelligence records from a JSON file.

    The JSON file must contain either:
    - a list of records
    - an object containing a 'records' list
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    if path.suffix.lower() != ".json":
        raise ValueError(
            "Only JSON files are supported by this loader."
        )

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    if isinstance(data, list):
        records = data

    elif isinstance(data, dict):

        records = data.get("records")

        if not isinstance(records, list):
            raise ValueError(
                "JSON object must contain a 'records' list."
            )

    else:
        raise ValueError(
            "JSON dataset must contain a list of records."
        )

    return records