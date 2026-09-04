from typing import Dict, List

from intelligence.models.evidence import Evidence


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def build_ml_evidence(
    entity_a_id: str,
    entity_b_id: str,
    comparison: Dict,
) -> List[Evidence]:
    """
    Convert ML profile comparison results into explainable
    Evidence objects.

    ML similarity is treated as supporting evidence only.
    It does not by itself establish attribution.
    """

    evidence = []

    stylometric_score = _clamp(
        comparison.get(
            "stylometric_similarity",
            0.0
        )
    )

    behavioral_score = _clamp(
        comparison.get(
            "behavioral_similarity",
            0.0
        )
    )

    overall_score = _clamp(
        comparison.get(
            "overall_ml_similarity",
            0.0
        )
    )

    # -------------------------------------------------
    # Stylometric evidence
    # -------------------------------------------------

    stylometric_evidence = Evidence(
        evidence_id="",
        evidence_type="ML_STYLOMETRY",
        description=(
            f"Stylometric comparison between "
            f"{entity_a_id} and {entity_b_id} produced "
            f"a similarity score of "
            f"{stylometric_score:.4f}."
        ),
        source="ml_stylometry",
        observed_at=None,
        entity_ids=[
            entity_a_id,
            entity_b_id
        ],
        reliability=0.70,
        strength=stylometric_score,
        metadata={
            "similarity": stylometric_score,
            "assessment": comparison.get(
                "stylometric_assessment",
                "UNASSESSED"
            ),
            "components": comparison.get(
                "stylometric_component_scores",
                []
            ),
        }
    )

    evidence.append(
        stylometric_evidence
    )

    # -------------------------------------------------
    # Behavioral evidence
    # -------------------------------------------------

    behavioral_evidence = Evidence(
        evidence_id="",
        evidence_type="ML_BEHAVIOR",
        description=(
            f"Behavioral comparison between "
            f"{entity_a_id} and {entity_b_id} produced "
            f"a similarity score of "
            f"{behavioral_score:.4f}."
        ),
        source="ml_behavioral",
        observed_at=None,
        entity_ids=[
            entity_a_id,
            entity_b_id
        ],
        reliability=0.70,
        strength=behavioral_score,
        metadata={
            "similarity": behavioral_score,
            "assessment": comparison.get(
                "behavioral_assessment",
                "UNASSESSED"
            ),
            "components": comparison.get(
                "behavioral_component_scores",
                {}
            ),
        }
    )

    evidence.append(
        behavioral_evidence
    )

    # -------------------------------------------------
    # Combined ML evidence
    # -------------------------------------------------

    combined_evidence = Evidence(
        evidence_id="",
        evidence_type="ML_PROFILE",
        description=(
            f"Combined stylometric and behavioral "
            f"analysis between {entity_a_id} and "
            f"{entity_b_id} produced an overall "
            f"similarity score of "
            f"{overall_score:.4f}."
        ),
        source="ml_profile",
        observed_at=None,
        entity_ids=[
            entity_a_id,
            entity_b_id
        ],
        reliability=0.70,
        strength=overall_score,
        metadata={
            "overall_similarity": overall_score,
            "stylometric_similarity": stylometric_score,
            "behavioral_similarity": behavioral_score,
            "assessment": comparison.get(
                "overall_assessment",
                "UNASSESSED"
            ),
        }
    )

    evidence.append(
        combined_evidence
    )

    return evidence