from intelligence.ml.profile import compare_actor_profiles


def obs(source, time, content):
    return {
        "source": source,
        "observed_at": time,
        "content": content,
    }


# ============================================================
# SAME ACTOR
# ============================================================

same_actor_a = [
    obs("forum_A", "2026-08-28T10:00:00Z",
        "Please send the payment details."),
    obs("forum_A", "2026-08-29T10:30:00Z",
        "Payment received, please confirm."),
    obs("forum_B", "2026-08-30T09:45:00Z",
        "Please send the payment details again."),
]

same_actor_b = [
    obs("forum_C", "2026-08-28T10:15:00Z",
        "Please send the payment details."),
    obs("forum_C", "2026-08-29T10:45:00Z",
        "Payment received, please confirm."),
    obs("forum_D", "2026-08-30T09:30:00Z",
        "Please send the payment details again."),
]


# ============================================================
# DIFFERENT ACTOR
# ============================================================

different_actor = [
    obs("forum_X", "2026-08-28T02:00:00Z",
        "WOW!!! AMAZING DEAL!!! 500% PROFIT!!!"),
    obs("forum_X", "2026-08-29T03:30:00Z",
        "BUY NOW!!! LIMITED OFFER!!!"),
    obs("forum_Y", "2026-08-30T04:15:00Z",
        "CLICK HERE!!! GET RICH FAST!!!"),
]


# ============================================================
# SIMILAR WRITING / DIFFERENT BEHAVIOR
# ============================================================

different_behavior = [
    obs("forum_Z", "2026-08-28T18:00:00Z",
        "Please send the payment details."),
    obs("forum_Z", "2026-08-29T19:30:00Z",
        "Payment received, please confirm."),
    obs("forum_Z", "2026-08-30T20:15:00Z",
        "Please send the payment details again."),
]


def evaluate_case(name, observations_a, observations_b):
    result = compare_actor_profiles(
        observations_a,
        observations_b
    )

    score = result["overall_ml_similarity"]
    assessment = result["overall_assessment"]

    print(f"\n{name}")
    print("-" * 60)
    print(f"Stylometry : {result['stylometric_similarity']:.4f}")
    print(f"Behavior   : {result['behavioral_similarity']:.4f}")
    print(f"Overall ML : {score:.4f}")
    print(f"Assessment : {assessment}")

    return result


def assert_between(value, minimum, maximum, description):
    assert minimum <= value <= maximum, (
        f"{description} expected between "
        f"{minimum} and {maximum}, got {value}"
    )


def main():

    print("=" * 60)
    print("CONTROLLED ML ATTRIBUTION EVALUATION")
    print("=" * 60)

    # --------------------------------------------------------
    # CASE 1
    # Same actor should have strong similarity
    # --------------------------------------------------------

    result_same = evaluate_case(
        "CASE 1 - SAME ACTOR",
        same_actor_a,
        same_actor_b
    )

    assert result_same["overall_ml_similarity"] >= 0.75
    print("PASS - Same actor shows strong similarity")

    # --------------------------------------------------------
    # CASE 2
    # Clearly different actor should score lower
    # --------------------------------------------------------

    result_different = evaluate_case(
        "CASE 2 - DIFFERENT ACTOR",
        same_actor_a,
        different_actor
    )

    assert result_different["overall_ml_similarity"] < \
           result_same["overall_ml_similarity"]

    print("PASS - Different actor scores lower than same actor")

    # --------------------------------------------------------
    # CASE 3
    # Similar writing but different behavior should reduce
    # the overall score compared with pure stylistic similarity
    # --------------------------------------------------------

    result_behavior = evaluate_case(
        "CASE 3 - SIMILAR WRITING / DIFFERENT BEHAVIOR",
        same_actor_a,
        different_behavior
    )

    assert (
        result_behavior["behavioral_similarity"]
        < result_behavior["stylometric_similarity"]
    )

    assert (
        result_behavior["overall_ml_similarity"]
        < result_behavior["stylometric_similarity"]
    )

    print(
        "PASS - Behavioral difference reduces overall similarity"
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("ALL CONTROLLED ML EVALUATION TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
    