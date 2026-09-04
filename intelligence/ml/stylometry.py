import re
import string
from collections import Counter
from typing import Dict, List


# Common function words.
# These are useful for capturing writing habits without relying on topic-specific words.
FUNCTION_WORDS = [
    "the", "a", "an", "and", "or", "but",
    "if", "then", "because", "so",
    "of", "to", "in", "on", "at",
    "for", "with", "from", "by",
    "is", "are", "was", "were",
    "be", "been", "being",
    "this", "that", "these", "those",
    "it", "they", "we", "you", "i"
]


def _safe_divide(numerator: float, denominator: float) -> float:
    """Safely divide two numbers."""
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _split_sentences(text: str) -> List[str]:
    """Split text into simple sentences."""
    sentences = re.split(r"[.!?]+", text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def _tokenize_words(text: str) -> List[str]:
    """Extract alphabetic/numeric word-like tokens."""
    return re.findall(r"\b[\w']+\b", text.lower())


def extract_stylometric_features(text: str) -> Dict:
    """
    Extract basic stylometric features from a text sample.

    This is a lightweight, explainable feature extractor intended
    for controlled attribution experiments.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    text = text.strip()

    if not text:
        return {
            "character_count": 0,
            "word_count": 0,
            "sentence_count": 0,
            "unique_word_count": 0,
            "vocabulary_richness": 0.0,
            "average_word_length": 0.0,
            "average_sentence_length": 0.0,
            "punctuation_count": 0,
            "punctuation_ratio": 0.0,
            "digit_count": 0,
            "digit_ratio": 0.0,
            "uppercase_count": 0,
            "uppercase_ratio": 0.0,
            "exclamation_count": 0,
            "question_count": 0,
            "comma_count": 0,
            "period_count": 0,
            "function_word_frequency": {},
        }

    words = _tokenize_words(text)
    sentences = _split_sentences(text)

    word_count = len(words)
    character_count = len(text)
    unique_word_count = len(set(words))

    total_word_characters = sum(len(word) for word in words)

    punctuation_count = sum(
        1 for character in text
        if character in string.punctuation
    )

    digit_count = sum(character.isdigit() for character in text)

    uppercase_count = sum(character.isupper() for character in text)

    function_word_counts = Counter(
        word for word in words
        if word in FUNCTION_WORDS
    )

    function_word_frequency = {
        word: round(
            _safe_divide(count, word_count),
            6
        )
        for word, count in sorted(function_word_counts.items())
    }

    return {
        "character_count": character_count,
        "word_count": word_count,
        "sentence_count": len(sentences),

        "unique_word_count": unique_word_count,

        "vocabulary_richness": round(
            _safe_divide(unique_word_count, word_count),
            6
        ),

        "average_word_length": round(
            _safe_divide(total_word_characters, word_count),
            6
        ),

        "average_sentence_length": round(
            _safe_divide(word_count, len(sentences)),
            6
        ),

        "punctuation_count": punctuation_count,

        "punctuation_ratio": round(
            _safe_divide(punctuation_count, character_count),
            6
        ),

        "digit_count": digit_count,

        "digit_ratio": round(
            _safe_divide(digit_count, character_count),
            6
        ),

        "uppercase_count": uppercase_count,

        "uppercase_ratio": round(
            _safe_divide(uppercase_count, character_count),
            6
        ),

        "exclamation_count": text.count("!"),
        "question_count": text.count("?"),
        "comma_count": text.count(","),
        "period_count": text.count("."),

        "function_word_frequency": function_word_frequency,
    }


def compare_stylometric_features(
    features_a: Dict,
    features_b: Dict
) -> Dict:
    """
    Compare two stylometric feature sets.

    Returns absolute differences for the numerical features.
    A later similarity layer can convert these differences
    into a normalized similarity score.
    """

    numerical_features = [
        "character_count",
        "word_count",
        "sentence_count",
        "unique_word_count",
        "vocabulary_richness",
        "average_word_length",
        "average_sentence_length",
        "punctuation_count",
        "punctuation_ratio",
        "digit_count",
        "digit_ratio",
        "uppercase_count",
        "uppercase_ratio",
        "exclamation_count",
        "question_count",
        "comma_count",
        "period_count",
    ]

    differences = {}

    for feature in numerical_features:
        value_a = features_a.get(feature, 0)
        value_b = features_b.get(feature, 0)

        differences[feature] = round(
            abs(float(value_a) - float(value_b)),
            6
        )

    return differences


if __name__ == "__main__":
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

    print("STYLOMETRIC FEATURES - SAMPLE A")
    for key, value in features_a.items():
        print(f"{key}: {value}")

    print("\nSTYLOMETRIC FEATURES - SAMPLE B")
    for key, value in features_b.items():
        print(f"{key}: {value}")

    print("\nFEATURE DIFFERENCES")
    differences = compare_stylometric_features(
        features_a,
        features_b
    )

    for key, value in differences.items():
        print(f"{key}: {value}")