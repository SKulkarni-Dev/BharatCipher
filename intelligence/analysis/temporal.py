from datetime import datetime


def parse_timestamp(timestamp):
    """
    Convert an ISO timestamp into a datetime object.
    """

    if not timestamp:
        return None

    try:
        return datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

    except (ValueError, TypeError):
        return None


def compare_observation_times(
    observations_a,
    observations_b
):
    """
    Compare the time periods represented by two
    groups of observations.

    Returns:

        TEMPORALLY_OVERLAPPING
        TEMPORALLY_CONSISTENT
        TEMPORALLY_CONFLICTING
        INSUFFICIENT_DATA
    """

    times_a = [
        parse_timestamp(
            observation.observed_at
        )
        for observation in observations_a
    ]

    times_b = [
        parse_timestamp(
            observation.observed_at
        )
        for observation in observations_b
    ]

    times_a = [
        timestamp
        for timestamp in times_a
        if timestamp is not None
    ]

    times_b = [
        timestamp
        for timestamp in times_b
        if timestamp is not None
    ]

    # ------------------------------------------
    # Missing timestamps
    # ------------------------------------------

    if not times_a or not times_b:
        return "INSUFFICIENT_DATA"

    # ------------------------------------------
    # Determine time ranges
    # ------------------------------------------

    start_a = min(times_a)
    end_a = max(times_a)

    start_b = min(times_b)
    end_b = max(times_b)

    # ------------------------------------------
    # Check overlap
    # ------------------------------------------

    latest_start = max(
        start_a,
        start_b
    )

    earliest_end = min(
        end_a,
        end_b
    )

    if latest_start <= earliest_end:

        return "TEMPORALLY_OVERLAPPING"

    # ------------------------------------------
    # Non-overlapping observations
    # ------------------------------------------

    return "TEMPORALLY_CONSISTENT"