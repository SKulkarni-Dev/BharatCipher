import math
from typing import Dict, Tuple


# Features where absolute magnitude matters.
NUMERICAL_FEATURES = [
    "vocabulary_richness",
    "average_word_length",
    "average_sentence_length",
    "punctuation_ratio",
    "digit_ratio",
    "uppercase_ratio",
]


# Features where matching behavior matters.
COUNT_FEATURES = [
    "exclamation_count",
    "question_count",
    "comma_count",
    "period_count",
]


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Keep a score inside the 0-1 range."""
    return max(minimum, min(maximum, value))


def _feature_similarity(value_a: float, value_b: float) -> float:
    """
    Convert two feature values into a similarity score.

    Uses relative difference so features with different scales
    can be compared more fairly.
    """

    value_a = float(value_a)
    value_b = float(value_b)

    denominator = abs(value_a) + abs(value_b)

    if denominator == 0:
        return 1.0

    difference = abs(value_a - value_b)

    return _clamp(1.0 - (difference / denominator))


def _count_similarity(value_a: float, value_b: float) -> float:
    """
    Similarity for count-based features.

    Exact matches receive 1.0.
    Larger differences progressively reduce similarity.
    """

    value_a = float(value_a)
    value_b = float(value_b)

    maximum = max(abs(value_a), abs(value_b), 1.0)

    difference = abs(value_a - value_b)

    return _clamp(1.0 - (difference / maximum))


def _function_word_similarity(
    words_a: Dict[str, float],
    words_b: Dict[str, float]
) -> float:
    """Compare function-word frequency patterns."""

    all_words = set(words_a) | set(words_b)

    if not all_words:
        return 1.0

    differences = []

    for word in all_words:
        value_a = float(words_a.get(word, 0.0))
        value_b = float(words_b.get(word, 0.0))

        differences.append(abs(value_a - value_b))

    average_difference = sum(differences) / len(differences)

    # Function-word frequencies are generally small.
    # Scaling makes the result easier to interpret as 0-1.
    return _clamp(1.0 - min(average_difference * 10.0, 1.0))


def calculate_stylometric_similarity(
    features_a: Dict,
    features_b: Dict
) -> Tuple[float, Dict]:
    """
    Calculate a normalized stylometric similarity score.

    Returns:
        (
            similarity_score,
            component_scores
        )

    similarity_score:
        0.0 = very different
        1.0 = highly similar
    """

    component_scores = {}

    for feature in NUMERICAL_FEATURES:
        component_scores[feature] = _feature_similarity(
            features_a.get(feature, 0.0),
            features_b.get(feature, 0.0)
        )

    for feature in COUNT_FEATURES:
        component_scores[feature] = _count_similarity(
            features_a.get(feature, 0.0),
            features_b.get(feature, 0.0)
        )

    component_scores["function_word_similarity"] = (
        _function_word_similarity(
            features_a.get("function_word_frequency", {}),
            features_b.get("function_word_frequency", {})
        )
    )

    # Equal weighting keeps the first version explainable.
    similarity = sum(component_scores.values()) / len(component_scores)

    return round(_clamp(similarity), 4), {
        key: round(value, 4)
        for key, value in component_scores.items()
    }


def interpret_similarity(score: float) -> str:
    """Convert a similarity score into an interpretable category."""

    score = _clamp(float(score))

    if score >= 0.85:
        return "HIGH_SIMILARITY"

    if score >= 0.65:
        return "MODERATE_SIMILARITY"

    if score >= 0.40:
        return "POSSIBLE_SIMILARITY"

    return "LOW_SIMILARITY"


if __name__ == "__main__":
    from intelligence.ml.stylometry import extract_stylometric_features

    sample_a = (
        "This is a controlled sample. "
        "The writing style contains repeated patterns!"
    )

    sample_b = (
        "This is another controlled sample. "
        "The author uses similar patterns?"
    )

    features_a = extract_stylometric_features(sample_a)
    features_b = extract_stylometric_features(sample_b)

    score, components = calculate_stylometric_similarity(
        features_a,
        features_b
    )

    print("STYLOMETRIC SIMILARITY")
    print(f"Score: {score}")
    print(f"Assessment: {interpret_similarity(score)}")

    print("\nCOMPONENT SCORES")
    for feature, value in components.items():
        print(f"{feature}: {value}")