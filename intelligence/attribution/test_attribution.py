from intelligence.models.evidence import Evidence

from intelligence.attribution.hypotheses import Hypothesis
from intelligence.attribution.scorer import (
    calculate_confidence,
    assess_confidence
)
from intelligence.attribution.contradictions import (
    find_contradictions
)


# ------------------------------------------
# Hypothesis
# ------------------------------------------

hypothesis = Hypothesis(

    hypothesis_id="HYP-001",

    description=(
        "shadowX and shadow_88 may belong "
        "to the same actor."
    ),

    entity_ids=[
        "ENT-DBCECA8B1A13",
        "ENT-E73C4E1171F6"
    ]
)


# ------------------------------------------
# Supporting evidence
# ------------------------------------------

supporting_evidence = [

    Evidence(

        evidence_id="EVID-001",

        evidence_type="PGP_MATCH",

        description=(
            "The same PGP identifier was "
            "observed across two identities."
        ),

        source="dataset_A + dataset_B",

        observed_at="2026-08-29T14:30:00Z",

        entity_ids=[
            "ENT-DBCECA8B1A13",
            "ENT-E73C4E1171F6"
        ],

        reliability=0.85,

        strength=0.90
    )
]


# ------------------------------------------
# Candidate contradicting evidence
# ------------------------------------------

contradicting_candidate = Evidence(

    evidence_id="EVID-002",

    evidence_type="DIFFERENT_INFRASTRUCTURE",

    description=(
        "The two identities were observed "
        "using unrelated infrastructure."
    ),

    source="dataset_C",

    observed_at="2026-08-30T10:00:00Z",

    entity_ids=[
        "ENT-DBCECA8B1A13",
        "ENT-E73C4E1171F6"
    ],

    reliability=0.70,

    strength=0.80
)


# ------------------------------------------
# Find contradictions
# ------------------------------------------

all_evidence = [
    *supporting_evidence,
    contradicting_candidate
]

contradicting_evidence = find_contradictions(
    hypothesis,
    all_evidence
)


# ------------------------------------------
# Calculate confidence
# ------------------------------------------

confidence = calculate_confidence(
    supporting_evidence,
    contradicting_evidence
)


assessment = assess_confidence(
    confidence
)


# ------------------------------------------
# Update hypothesis
# ------------------------------------------

hypothesis.supporting_evidence_ids = [
    evidence.evidence_id
    for evidence in supporting_evidence
]

hypothesis.contradicting_evidence_ids = [
    evidence.evidence_id
    for evidence in contradicting_evidence
]

hypothesis.confidence = confidence

hypothesis.assessment = assessment


# ------------------------------------------
# Display result
# ------------------------------------------

print("ATTRIBUTION ASSESSMENT")
print("----------------------")

print(
    f"Hypothesis: "
    f"{hypothesis.description}"
)

print(
    f"Confidence: "
    f"{hypothesis.confidence}"
)

print(
    f"Assessment: "
    f"{hypothesis.assessment}"
)

print(
    f"Supporting evidence: "
    f"{hypothesis.supporting_evidence_ids}"
)

print(
    f"Contradicting evidence: "
    f"{hypothesis.contradicting_evidence_ids}"
)