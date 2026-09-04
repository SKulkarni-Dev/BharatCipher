from intelligence.models.evidence import Evidence

from intelligence.attribution.hypotheses import Hypothesis
from intelligence.attribution.scorer import (
    calculate_confidence,
    assess_confidence
)


# ==========================================
# HYPOTHESIS
# ==========================================

hypothesis = Hypothesis(

    hypothesis_id="HYP-CONTRA-001",

    description=(
        "alphaOne and betaTwo may belong "
        "to the same actor."
    ),

    entity_ids=[
        "ENT-ALPHA",
        "ENT-BETA"
    ]
)


# ==========================================
# SUPPORTING EVIDENCE
# ==========================================

supporting_evidence = [

    Evidence(

        evidence_id="EVID-PGP",

        evidence_type="SHARES_PGP",

        description=(
            "Both identities were observed "
            "using PGP-X."
        ),

        source="dataset_A + dataset_B",

        observed_at="2026-08-29T10:00:00Z",

        entity_ids=[
            "ENT-ALPHA",
            "ENT-BETA"
        ],

        reliability=0.85,

        strength=1.0
    ),

    Evidence(

        evidence_id="EVID-TEMPORAL",

        evidence_type="TEMPORAL_OVERLAP",

        description=(
            "The activity periods of the two "
            "identities overlap."
        ),

        source="temporal_analysis",

        observed_at="2026-08-29T10:00:00Z",

        entity_ids=[
            "ENT-ALPHA",
            "ENT-BETA"
        ],

        reliability=0.85,

        strength=0.60
    )
]


# ==========================================
# CONTRADICTING EVIDENCE
# ==========================================

contradicting_evidence = [

    Evidence(

        evidence_id="EVID-INFRA-CONFLICT",

        evidence_type="DIFFERENT_INFRASTRUCTURE",

        description=(
            "The two identities were observed "
            "using different infrastructure."
        ),

        source="infrastructure_analysis",

        observed_at="2026-08-30T10:00:00Z",

        entity_ids=[
            "ENT-ALPHA",
            "ENT-BETA"
        ],

        reliability=0.80,

        strength=0.70
    )
]


# ==========================================
# CALCULATE WITHOUT CONTRADICTION
# ==========================================

confidence_without_contradiction = calculate_confidence(
    supporting_evidence,
    []
)


# ==========================================
# CALCULATE WITH CONTRADICTION
# ==========================================

confidence_with_contradiction = calculate_confidence(
    supporting_evidence,
    contradicting_evidence
)


# ==========================================
# ASSESSMENTS
# ==========================================

assessment_without_contradiction = assess_confidence(
    confidence_without_contradiction
)

assessment_with_contradiction = assess_confidence(
    confidence_with_contradiction
)


# ==========================================
# DISPLAY
# ==========================================

print()
print("======================================")
print("CONTRADICTION TEST")
print("======================================")

print()

print("WITHOUT CONTRADICTING EVIDENCE")
print("------------------------------")

print(
    f"Confidence: "
    f"{confidence_without_contradiction}"
)

print(
    f"Assessment: "
    f"{assessment_without_contradiction}"
)

print()

print("WITH CONTRADICTING EVIDENCE")
print("---------------------------")

print(
    f"Confidence: "
    f"{confidence_with_contradiction}"
)

print(
    f"Assessment: "
    f"{assessment_with_contradiction}"
)

print()

print("CHANGE IN CONFIDENCE")
print("--------------------")

print(
    f"{confidence_without_contradiction}"
    f" -> "
    f"{confidence_with_contradiction}"
)