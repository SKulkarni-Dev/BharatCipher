import sys
from pathlib import Path

from investigation_engine import investigate_dataset
from output.report import generate_report


DEFAULT_DATASET = "ingestion/test_temporal_dataset.json"


def main():

    # -------------------------
    # DATASET PATH
    # -------------------------

    if len(sys.argv) > 2:
        print("Usage: python app.py [dataset_path]")
        return

    if len(sys.argv) == 2:
        dataset_path = sys.argv[1]
    else:
        dataset_path = DEFAULT_DATASET

    # -------------------------
    # CHECK DATASET
    # -------------------------

    if not Path(dataset_path).exists():
        print(f"Dataset not found: {dataset_path}")
        return

    # -------------------------
    # RUN INVESTIGATION
    # -------------------------

    result = investigate_dataset(
        dataset_path
    )

    # -------------------------
    # GENERATE HUMAN-READABLE REPORT
    # -------------------------

    print(
        generate_report(result)
    )


if __name__ == "__main__":
    main()