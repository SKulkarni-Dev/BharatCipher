from intelligence.ingestion.loader import load_json
from intelligence.ingestion.validator import validate_records
from intelligence.ingestion.observation_builder import build_observations
from intelligence.ingestion.entity_builder import attach_entities_to_observation

from intelligence.correlation.correlator import correlate_observations

from intelligence.evidence.evidence_builder import build_evidence

from intelligence.analysis.temporal import compare_observation_times
from intelligence.analysis.temporal_evidence import build_temporal_evidence

from intelligence.ml.profile import compare_actor_profiles
from intelligence.ml.evidence import build_ml_evidence

from intelligence.attribution.scorer import (
    calculate_confidence,
    assess_confidence
)


DATASET_PATH = (
    "intelligence/ingestion/attribution_evaluation.json"
)


def get_actor_observations(
    observations,
    entity_id
):
    return [
        observation
        for observation in observations
        if entity_id in observation.entity_ids
    ]


def convert_to_ml_profile(
    observations
):
    return [
        {
            "source": observation.source,
            "observed_at": observation.observed_at,
            "content": observation.content
        }
        for observation in observations
    ]


def run_evaluation():

    # ==========================================
    # LOAD
    # ==========================================

    records = load_json(
        DATASET_PATH
    )

    valid_records, errors = validate_records(
        records
    )

    # ==========================================
    # OBSERVATIONS
    # ==========================================

    observations = build_observations(
        valid_records,
        source_reliability=0.85
    )

    # ==========================================
    # ENTITIES
    # ==========================================

    all_entities = []

    for observation in observations:

        entities = attach_entities_to_observation(
            observation
        )

        all_entities.extend(
            entities
        )

    unique_entities = {}

    for entity in all_entities:

        unique_entities[
            entity.entity_id
        ] = entity

    entities = list(
        unique_entities.values()
    )

    # ==========================================
    # CORRELATION
    # ==========================================

    relationships = correlate_observations(
        observations,
        entities
    )

    # ==========================================
    # EVIDENCE
    # ==========================================

    evidence = []

    for relationship in relationships:

        item = build_evidence(
            relationship,
            observations,
            entities
        )

        evidence.append(
            item
        )

    # ==========================================
    # TEMPORAL EVIDENCE
    # ==========================================

    for relationship in relationships:

        entity_a_id = (
            relationship.source_entity_id
        )

        entity_b_id = (
            relationship.target_entity_id
        )

        observations_a = get_actor_observations(
            observations,
            entity_a_id
        )

        observations_b = get_actor_observations(
            observations,
            entity_b_id
        )

        if not observations_a or not observations_b:
            continue

        temporal_result = (
            compare_observation_times(
                observations_a,
                observations_b
            )
        )

        temporal_item = build_temporal_evidence(
            entity_a_id,
            entity_b_id,
            observations_a,
            observations_b,
            temporal_result
        )

        if temporal_item:

            evidence.append(
                temporal_item
            )

    # ==========================================
    # ML EVIDENCE
    # ==========================================

    ml_evidence = []

    for relationship in relationships:

        entity_a_id = (
            relationship.source_entity_id
        )

        entity_b_id = (
            relationship.target_entity_id
        )

        observations_a = get_actor_observations(
            observations,
            entity_a_id
        )

        observations_b = get_actor_observations(
            observations,
            entity_b_id
        )

        if not observations_a or not observations_b:
            continue

        profile_a = convert_to_ml_profile(
            observations_a
        )

        profile_b = convert_to_ml_profile(
            observations_b
        )

        comparison = compare_actor_profiles(
            profile_a,
            profile_b
        )

        items = build_ml_evidence(
            entity_a_id,
            entity_b_id,
            comparison
        )

        ml_evidence.extend(
            items
        )

    evidence.extend(
        ml_evidence
    )

    # ==========================================
    # HEADER
    # ==========================================

    print()
    print("======================================")
    print("ATTRIBUTION EVALUATION")
    print("======================================")

    print()
    print(
        f"Records: {len(records)}"
    )

    print(
        f"Valid records: {len(valid_records)}"
    )

    print(
        f"Relationships: {len(relationships)}"
    )

    print()

    # ==========================================
    # ENTITY MAP
    # ==========================================

    entity_map = {
        entity.entity_id: entity
        for entity in entities
    }

    # ==========================================
    # CORRELATED RELATIONSHIPS
    # ==========================================

    for index, relationship in enumerate(
        relationships,
        start=1
    ):

        entity_a = entity_map[
            relationship.source_entity_id
        ]

        entity_b = entity_map[
            relationship.target_entity_id
        ]

        related_evidence = [
            item
            for item in evidence
            if (
                set(
                    [
                        relationship.source_entity_id,
                        relationship.target_entity_id
                    ]
                ).issubset(
                    set(item.entity_ids)
                )
            )
        ]

        supporting = [
            item
            for item in related_evidence
            if item.evidence_type
            not in {
                "TEMPORAL_CONFLICT",
                "ML_STYLOMETRY",
                "ML_BEHAVIOR"
            }
        ]

        contradicting = [
            item
            for item in related_evidence
            if item.evidence_type
            in {
                "TEMPORAL_CONFLICT"
            }
        ]

        confidence = calculate_confidence(
            supporting,
            contradicting
        )

        assessment = assess_confidence(
            confidence
        )

        print(
            f"CASE {index}"
        )

        print(
            "-----"
        )

        print(
            f"{entity_a.value} "
            f"<-> "
            f"{entity_b.value}"
        )

        print(
            f"Relationship: "
            f"{relationship.relationship_type}"
        )

        print(
            "Evidence:"
        )

        for item in related_evidence:

            print(
                f"  - "
                f"{item.evidence_type} "
                f"(strength={item.strength}, "
                f"reliability={item.reliability})"
            )

        print(
            f"Confidence: "
            f"{confidence}"
        )

        print(
            f"Assessment: "
            f"{assessment}"
        )

        print()

    # ==========================================
    # CONTROLLED ML NON-MATCH
    # ==========================================

    print("======================================")
    print("CONTROLLED ML NON-MATCH")
    print("======================================")

    epsilon = None
    zeta = None

    for entity in entities:

        if entity.value == "epsilonFive":
            epsilon = entity

        if entity.value == "zetaSix":
            zeta = entity

    if epsilon is None or zeta is None:

        print(
            "Controlled pair not found."
        )

        return

    epsilon_observations = get_actor_observations(
        observations,
        epsilon.entity_id
    )

    zeta_observations = get_actor_observations(
        observations,
        zeta.entity_id
    )

    if not epsilon_observations or not zeta_observations:

        print(
            "Controlled pair has insufficient observations."
        )

        return

    epsilon_profile = convert_to_ml_profile(
        epsilon_observations
    )

    zeta_profile = convert_to_ml_profile(
        zeta_observations
    )

    non_match_comparison = compare_actor_profiles(
        epsilon_profile,
        zeta_profile
    )

    print()
    print(
        f"{epsilon.value} <-> {zeta.value}"
    )

    print(
        f"Stylometry: "
        f"{non_match_comparison['stylometric_similarity']:.4f}"
    )

    print(
        f"Behavior: "
        f"{non_match_comparison['behavioral_similarity']:.4f}"
    )

    print(
        f"Overall ML: "
        f"{non_match_comparison['overall_ml_similarity']:.4f}"
    )

    print(
        f"Assessment: "
        f"{non_match_comparison['overall_assessment']}"
    )

    print()

    print(
        "NOTE: This pair has no shared PGP relationship."
    )

    print(
        "ML similarity is evaluated independently."
    )


if __name__ == "__main__":

    run_evaluation()