def calculate_confidence(
    supporting_evidence,
    contradicting_evidence
):
    """
    Calculate transparent baseline attribution confidence.

    Each supporting evidence item contributes:

        reliability × strength

    Multiple independent supporting signals are
    combined using:

        1 - product(1 - signal)

    This prevents additional supporting evidence
    from lowering confidence.

    Contradicting evidence reduces the resulting
    confidence.

    This is a rule-based baseline.
    It is NOT the final ML model.
    """

    # ------------------------------------------
    # Supporting evidence
    # ------------------------------------------

    supporting_confidence = 0.0

    for evidence in supporting_evidence:

        signal = (
            evidence.reliability
            *
            evidence.strength
        )

        signal = max(
            0.0,
            min(1.0, signal)
        )

        supporting_confidence = (
            1
            -
            (
                (1 - supporting_confidence)
                *
                (1 - signal)
            )
        )

    # ------------------------------------------
    # Contradicting evidence
    # ------------------------------------------

    contradiction_strength = 0.0

    for evidence in contradicting_evidence:

        signal = (
            evidence.reliability
            *
            evidence.strength
        )

        signal = max(
            0.0,
            min(1.0, signal)
        )

        contradiction_strength = (
            1
            -
            (
                (1 - contradiction_strength)
                *
                (1 - signal)
            )
        )

    # ------------------------------------------
    # Apply contradictions
    # ------------------------------------------

    confidence = (
        supporting_confidence
        *
        (1 - contradiction_strength)
    )

    return round(
        max(
            0.0,
            min(1.0, confidence)
        ),
        4
    )


def assess_confidence(confidence):
    """
    Convert numerical confidence into
    an interpretable assessment.
    """

    if confidence >= 0.85:
        return "HIGH_CONFIDENCE"

    if confidence >= 0.65:
        return "MODERATE_CONFIDENCE"

    if confidence >= 0.40:
        return "POSSIBLE_MATCH"

    return "LOW_CONFIDENCE"