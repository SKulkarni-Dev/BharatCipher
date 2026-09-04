def validate_record(record):
    """
    Validate a single intelligence record.

    A valid record must contain:
    - source
    - content
    """

    if not isinstance(record, dict):
        return False, "Record must be a JSON object."

    if not record.get("source"):
        return False, "Missing source."

    if not record.get("content"):
        return False, "Missing content."

    return True, "Valid"


def validate_records(records):
    """
    Validate a collection of intelligence records.

    Returns:
        valid_records
        errors
    """

    valid_records = []
    errors = []

    for index, record in enumerate(records):

        valid, message = validate_record(record)

        if valid:

            valid_records.append(record)

        else:

            errors.append({
                "index": index,
                "error": message
            })

    return valid_records, errors