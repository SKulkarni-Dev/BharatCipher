from typing import Dict, List

from intelligence.ml.stylometry import (
    extract_stylometric_features,
)
from intelligence.ml.similarity import (
    calculate_stylometric_similarity,
    interpret_similarity,
)

from intelligence.ml.behavioral import (
    extract_behavioral_features,
    calculate_behavioral_similarity,
    compare_behavioral_features,
    interpret_behavioral_similarity,
)


def _clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 1.0,
) -> float:
    """Keep a score between 0 and 1."""
    return max(minimum, min(maximum, value))


def build_actor_profile(
    observations: List[Dict],
) -> Dict:
    """
    Build an explainable ML profile from a collection
    of controlled/synthetic observations.

    The profile contains both stylometric and behavioral
    characteristics.
    """

    if not isinstance(observations, list):
        raise TypeError("observations must be a list")

    texts = [
        observation.get("content", "")
        for observation in observations
        if isinstance(observation, dict)
        and observation.get("content")
    ]

    stylometric_features = []

    for text in texts:
        stylometric_features.append(
            extract_stylometric_features(text)
        )

    behavioral_features = extract_behavioral_features(
        observations
    )

    return {
        "observation_count": len(observations),
        "text_sample_count": len(texts),
        "stylometric_features": stylometric_features,
        "behavioral_features": behavioral_features,
    }


def compare_actor_profiles(
    observations_a: List[Dict],
    observations_b: List[Dict],
) -> Dict:
    """
    Compare two actor profiles.

    Produces:
        - stylometric similarity
        - behavioral similarity
        - combined ML similarity
        - interpretable assessments
        - component-level explanations
    """

    profile_a = build_actor_profile(
        observations_a
    )

    profile_b = build_actor_profile(
        observations_b
    )

    # -------------------------------------------------
    # STYLOMETRY
    # -------------------------------------------------

    texts_a = [
        observation.get("content", "")
        for observation in observations_a
        if isinstance(observation, dict)
        and observation.get("content")
    ]

    texts_b = [
        observation.get("content", "")
        for observation in observations_b
        if isinstance(observation, dict)
        and observation.get("content")
    ]

    stylometric_scores = []

    stylometric_components = []

    for text_a in texts_a:
        for text_b in texts_b:

            features_a = extract_stylometric_features(
                text_a
            )

            features_b = extract_stylometric_features(
                text_b
            )

            score, components = (
                calculate_stylometric_similarity(
                    features_a,
                    features_b,
                )
            )

            stylometric_scores.append(score)
            stylometric_components.append(
                components
            )

    if stylometric_scores:
        stylometric_similarity = (
            sum(stylometric_scores)
            / len(stylometric_scores)
        )
    else:
        stylometric_similarity = 0.0

    # -------------------------------------------------
    # BEHAVIOR
    # -------------------------------------------------

    behavioral_similarity = (
        calculate_behavioral_similarity(
            profile_a["behavioral_features"],
            profile_b["behavioral_features"],
        )
    )

    behavioral_components = (
        compare_behavioral_features(
            profile_a["behavioral_features"],
            profile_b["behavioral_features"],
        )
    )

    # -------------------------------------------------
    # COMBINED ML SCORE
    # -------------------------------------------------

    # Equal weighting for the first explainable version.
    overall_similarity = (
        0.5 * stylometric_similarity
        + 0.5 * behavioral_similarity
    )

    overall_similarity = round(
        _clamp(overall_similarity),
        4,
    )

    return {
        "stylometric_similarity": round(
            stylometric_similarity,
            4,
        ),

        "stylometric_assessment": interpret_similarity(
            stylometric_similarity
        ),

        "behavioral_similarity": round(
            behavioral_similarity,
            4,
        ),

        "behavioral_assessment": (
            interpret_behavioral_similarity(
                behavioral_similarity
            )
        ),

        "overall_ml_similarity": overall_similarity,

        "overall_assessment": interpret_similarity(
            overall_similarity
        ),

        "stylometric_component_scores": (
            stylometric_components
        ),

        "behavioral_component_scores": (
            behavioral_components
        ),

        "profile_a": profile_a,

        "profile_b": profile_b,
    }


if __name__ == "__main__":

    # ---------------------------------------------
    # CONTROLLED TEST DATA
    # ---------------------------------------------

    actor_a = [
        {
            "source": "forum_A",
            "observed_at": "2026-08-28T10:00:00Z",
            "content": (
                "This is a controlled writing sample. "
                "The author uses repeated patterns."
            ),
        },
        {
            "source": "forum_A",
            "observed_at": "2026-08-28T12:00:00Z",
            "content": (
                "Another controlled sample. "
                "The writing follows similar patterns."
            ),
        },
        {
            "source": "forum_B",
            "observed_at": "2026-08-29T10:00:00Z",
            "content": (
                "This sample demonstrates another "
                "controlled observation."
            ),
        },
    ]

    actor_b = [
        {
            "source": "forum_A",
            "observed_at": "2026-08-28T10:30:00Z",
            "content": (
                "This is a controlled writing sample. "
                "The author follows repeated patterns."
            ),
        },
        {
            "source": "forum_A",
            "observed_at": "2026-08-28T12:30:00Z",
            "content": (
                "Another controlled sample. "
                "The writing follows similar patterns."
            ),
        },
        {
            "source": "forum_B",
            "observed_at": "2026-08-29T10:30:00Z",
            "content": (
                "This sample demonstrates another "
                "controlled observation."
            ),
        },
    ]

    result = compare_actor_profiles(
        actor_a,
        actor_b,
    )

    print("===================================")
    print("      ACTOR ML PROFILE COMPARISON")
    print("===================================")

    print(
        f"\nStylometric similarity: "
        f"{result['stylometric_similarity']}"
    )

    print(
        f"Stylometric assessment: "
        f"{result['stylometric_assessment']}"
    )

    print(
        f"\nBehavioral similarity: "
        f"{result['behavioral_similarity']}"
    )

    print(
        f"Behavioral assessment: "
        f"{result['behavioral_assessment']}"
    )

    print(
        f"\nOverall ML similarity: "
        f"{result['overall_ml_similarity']}"
    )

    print(
        f"Overall assessment: "
        f"{result['overall_assessment']}"
    )

    print("\nBEHAVIORAL COMPONENTS")

    for feature, score in (
        result["behavioral_component_scores"]
    ).items():
        print(f"{feature}: {score}")

    print("\nSTYLOMETRIC COMPARISONS")

    for index, components in enumerate(
        result["stylometric_component_scores"],
        start=1,
    ):
        print(f"\nComparison {index}")

        for feature, score in components.items():
            print(f"{feature}: {score}")