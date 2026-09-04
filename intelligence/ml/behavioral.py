from collections import Counter
from datetime import datetime
from typing import Dict, List


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Keep a value between 0 and 1."""
    return max(minimum, min(maximum, value))


def _parse_timestamp(timestamp: str):
    """Parse an ISO-8601 timestamp."""
    if not timestamp:
        return None

    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def extract_behavioral_features(observations: List[Dict]) -> Dict:
    """
    Extract behavioral features from a collection of observations.

    Expected observation fields:
        source
        observed_at
        content

    The function is designed for controlled/synthetic investigation data.
    """

    if not isinstance(observations, list):
        raise TypeError("observations must be a list")

    if not observations:
        return {
            "observation_count": 0,
            "source_count": 0,
            "source_distribution": {},
            "activity_hours": [],
            "activity_hour_distribution": {},
            "average_time_gap_hours": 0.0,
            "activity_span_hours": 0.0,
            "content_length_average": 0.0,
        }

    timestamps = []
    sources = []
    content_lengths = []

    for observation in observations:
        if not isinstance(observation, dict):
            continue

        source = observation.get("source")

        if source:
            sources.append(source)

        content = observation.get("content") or ""
        content_lengths.append(len(content))

        timestamp = _parse_timestamp(
            observation.get("observed_at")
        )

        if timestamp:
            timestamps.append(timestamp)

    timestamps.sort()

    source_counts = Counter(sources)

    total_sources = len(sources)

    source_distribution = {
        source: round(count / total_sources, 4)
        for source, count in sorted(source_counts.items())
    } if total_sources else {}

    activity_hours = [
        timestamp.hour
        for timestamp in timestamps
    ]

    hour_counts = Counter(activity_hours)

    total_timestamps = len(activity_hours)

    activity_hour_distribution = {
        str(hour): round(count / total_timestamps, 4)
        for hour, count in sorted(hour_counts.items())
    } if total_timestamps else {}

    if len(timestamps) >= 2:
        gaps = []

        for previous, current in zip(
            timestamps,
            timestamps[1:]
        ):
            gap_seconds = (
                current - previous
            ).total_seconds()

            gaps.append(
                max(gap_seconds / 3600.0, 0.0)
            )

        average_time_gap_hours = (
            sum(gaps) / len(gaps)
        )
    else:
        average_time_gap_hours = 0.0

    if len(timestamps) >= 2:
        activity_span_hours = (
            timestamps[-1] - timestamps[0]
        ).total_seconds() / 3600.0
    else:
        activity_span_hours = 0.0

    content_length_average = (
        sum(content_lengths) / len(content_lengths)
        if content_lengths
        else 0.0
    )

    return {
        "observation_count": len(observations),
        "source_count": len(source_counts),

        "source_distribution": source_distribution,

        "activity_hours": activity_hours,

        "activity_hour_distribution": activity_hour_distribution,

        "average_time_gap_hours": round(
            average_time_gap_hours,
            4
        ),

        "activity_span_hours": round(
            activity_span_hours,
            4
        ),

        "content_length_average": round(
            content_length_average,
            4
        ),
    }


def compare_behavioral_features(
    features_a: Dict,
    features_b: Dict
) -> Dict:
    """
    Compare two behavioral profiles.

    Returns component-level similarity scores from 0 to 1.
    """

    similarities = {}

    # Activity frequency similarity
    count_a = features_a.get("observation_count", 0)
    count_b = features_b.get("observation_count", 0)

    maximum_count = max(count_a, count_b, 1)

    similarities["observation_frequency"] = _clamp(
        1.0 - abs(count_a - count_b) / maximum_count
    )

    # Source distribution similarity
    sources_a = features_a.get(
        "source_distribution",
        {}
    )

    sources_b = features_b.get(
        "source_distribution",
        {}
    )

    all_sources = set(sources_a) | set(sources_b)

    if all_sources:
        source_difference = sum(
            abs(
                sources_a.get(source, 0.0)
                - sources_b.get(source, 0.0)
            )
            for source in all_sources
        )

        similarities["source_pattern"] = _clamp(
            1.0 - source_difference / 2.0
        )
    else:
        similarities["source_pattern"] = 1.0

    # Activity-hour similarity
    hours_a = features_a.get(
        "activity_hour_distribution",
        {}
    )

    hours_b = features_b.get(
        "activity_hour_distribution",
        {}
    )

    all_hours = set(hours_a) | set(hours_b)

    if all_hours:
        hour_difference = sum(
            abs(
                hours_a.get(hour, 0.0)
                - hours_b.get(hour, 0.0)
            )
            for hour in all_hours
        )

        similarities["activity_time_pattern"] = _clamp(
            1.0 - hour_difference / 2.0
        )
    else:
        similarities["activity_time_pattern"] = 1.0

    # Average time-gap similarity
    gap_a = float(
        features_a.get(
            "average_time_gap_hours",
            0.0
        )
    )

    gap_b = float(
        features_b.get(
            "average_time_gap_hours",
            0.0
        )
    )

    gap_max = max(gap_a, gap_b, 1.0)

    similarities["posting_interval_pattern"] = _clamp(
        1.0 - abs(gap_a - gap_b) / gap_max
    )

    # Activity-span similarity
    span_a = float(
        features_a.get(
            "activity_span_hours",
            0.0
        )
    )

    span_b = float(
        features_b.get(
            "activity_span_hours",
            0.0
        )
    )

    span_max = max(span_a, span_b, 1.0)

    similarities["activity_span_pattern"] = _clamp(
        1.0 - abs(span_a - span_b) / span_max
    )

    # Average content length similarity
    length_a = float(
        features_a.get(
            "content_length_average",
            0.0
        )
    )

    length_b = float(
        features_b.get(
            "content_length_average",
            0.0
        )
    )

    length_max = max(length_a, length_b, 1.0)

    similarities["content_length_pattern"] = _clamp(
        1.0 - abs(length_a - length_b) / length_max
    )

    return {
        key: round(value, 4)
        for key, value in similarities.items()
    }


def calculate_behavioral_similarity(
    features_a: Dict,
    features_b: Dict
) -> float:
    """
    Calculate an overall behavioral similarity score.
    """

    component_scores = compare_behavioral_features(
        features_a,
        features_b
    )

    if not component_scores:
        return 0.0

    score = sum(component_scores.values()) / len(
        component_scores
    )

    return round(_clamp(score), 4)


def interpret_behavioral_similarity(
    score: float
) -> str:
    """Convert a behavioral score into an interpretable category."""

    score = _clamp(float(score))

    if score >= 0.85:
        return "HIGH_SIMILARITY"

    if score >= 0.65:
        return "MODERATE_SIMILARITY"

    if score >= 0.40:
        return "POSSIBLE_SIMILARITY"

    return "LOW_SIMILARITY"


if __name__ == "__main__":
    profile_a = [
        {
            "source": "forum_A",
            "observed_at": "2026-08-28T10:00:00Z",
            "content": "Controlled sample one."
        },
        {
            "source": "forum_A",
            "observed_at": "2026-08-28T12:00:00Z",
            "content": "Controlled sample two."
        },
        {
            "source": "forum_B",
            "observed_at": "2026-08-29T10:00:00Z",
            "content": "Controlled sample three."
        },
    ]

    profile_b = [
        {
            "source": "forum_A",
            "observed_at": "2026-08-28T10:30:00Z",
            "content": "Another controlled sample."
        },
        {
            "source": "forum_A",
            "observed_at": "2026-08-28T12:30:00Z",
            "content": "Another controlled sample."
        },
        {
            "source": "forum_B",
            "observed_at": "2026-08-29T10:30:00Z",
            "content": "Another controlled sample."
        },
    ]

    features_a = extract_behavioral_features(
        profile_a
    )

    features_b = extract_behavioral_features(
        profile_b
    )

    score = calculate_behavioral_similarity(
        features_a,
        features_b
    )

    print("BEHAVIORAL PROFILE - A")
    for key, value in features_a.items():
        print(f"{key}: {value}")

    print("\nBEHAVIORAL PROFILE - B")
    for key, value in features_b.items():
        print(f"{key}: {value}")

    print("\nBEHAVIORAL SIMILARITY")

    print(f"Score: {score}")

    print(
        f"Assessment: "
        f"{interpret_behavioral_similarity(score)}"
    )

    print("\nCOMPONENT SCORES")

    components = compare_behavioral_features(
        features_a,
        features_b
    )

    for key, value in components.items():
        print(f"{key}: {value}")