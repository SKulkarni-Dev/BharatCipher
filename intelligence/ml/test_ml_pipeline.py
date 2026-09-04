from intelligence.ml.profile import compare_actor_profiles
from intelligence.ml.evidence import build_ml_evidence


def make_observation(source, observed_at, content):
    return {
        "source": source,
        "observed_at": observed_at,
        "content": content,
    }


# ---------------------------------------------------------
# CASE 1: Same actor, different handles
# ---------------------------------------------------------

actor_a = [
    make_observation(
        "forum_A",
        "2026-08-28T10:00:00Z",
        "Need payment details, please send wallet address."
    ),
    make_observation(
        "forum_A",
        "2026-08-29T10:30:00Z",
        "Payment received, please confirm the transaction."
    ),
    make_observation(
        "forum_B",
        "2026-08-30T09:45:00Z",
        "Send the payment details again, please."
    ),
]

actor_b = [
    make_observation(
        "forum_C",
        "2026-08-28T10:15:00Z",
        "Need payment details, please send wallet address."
    ),
    make_observation(
        "forum_C",
        "2026-08-29T10:45:00Z",
        "Payment received, please confirm the transaction."
    ),
    make_observation(
        "forum_D",
        "2026-08-30T09:30:00Z",
        "Send the payment details again, please."
    ),
]


# ---------------------------------------------------------
# CASE 2: Clearly different actors
# ---------------------------------------------------------

actor_c = [
    make_observation(
        "forum_X",
        "2026-08-28T02:00:00Z",
        "WOW!!! AMAZING DEAL!!! 500% PROFIT!!!"
    ),
    make_observation(
        "forum_X",
        "2026-08-29T03:30:00Z",
        "BUY NOW!!! LIMITED OFFER!!!"
    ),
    make_observation(
        "forum_Y",
        "2026-08-30T04:15:00Z",
        "CLICK HERE!!! GET RICH FAST!!!"
    ),
]


# ---------------------------------------------------------
# CASE 3: Similar writing but different behavior
# ---------------------------------------------------------

actor_d = [
    make_observation(
        "forum_Z",
        "2026-08-28T18:00:00Z",
        "Need payment details, please send wallet address."
    ),
    make_observation(
        "forum_Z",
        "2026-08-29T19:30:00Z",
        "Payment received, please confirm the transaction."
    ),
    make_observation(
        "forum_Z",
        "2026-08-30T20:15:00Z",
        "Send the payment details again, please."
    ),
]


def run_case(name, observations_a, observations_b):
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    comparison = compare_actor_profiles(
        observations_a,
        observations_b
    )

    print(
        f"Stylometric similarity: "
        f"{comparison['stylometric_similarity']:.4f}"
    )

    print(
        f"Behavioral similarity: "
        f"{comparison['behavioral_similarity']:.4f}"
    )

    print(
        f"Overall ML similarity: "
        f"{comparison['overall_ml_similarity']:.4f}"
    )

    print(
        f"Assessment: "
        f"{comparison['overall_assessment']}"
    )

    evidence = build_ml_evidence(
        "ENT-A",
        "ENT-B",
        comparison
    )

    print("\nML Evidence:")

    for item in evidence:
        print(
            f"{item.evidence_type}: "
            f"strength={item.strength:.4f}, "
            f"reliability={item.reliability:.2f}"
        )

    return comparison


if __name__ == "__main__":

    # Same actor
    run_case(
        "CASE 1 - SAME ACTOR / DIFFERENT HANDLES",
        actor_a,
        actor_b
    )

    # Different actors
    run_case(
        "CASE 2 - CLEARLY DIFFERENT ACTORS",
        actor_a,
        actor_c
    )

    # Similar writing, different behavior
    run_case(
        "CASE 3 - SIMILAR WRITING / DIFFERENT BEHAVIOR",
        actor_a,
        actor_d
    )

    print("\n" + "=" * 60)
    print("ML PIPELINE TEST COMPLETE")
    print("=" * 60)