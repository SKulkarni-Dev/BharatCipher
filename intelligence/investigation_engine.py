from .ingestion.loader import load_json
from .ingestion.validator import validate_records
from .ingestion.observation_builder import build_observations
from .ingestion.entity_builder import attach_entities_to_observation
from .correlation.correlator import correlate_observations
from intelligence.ml.profile import compare_actor_profiles
from intelligence.ml.evidence import build_ml_evidence
from .evidence.evidence_builder import build_evidence

from .attribution.hypotheses import Hypothesis
from .attribution.scorer import (
    calculate_confidence,
    assess_confidence
)
from .attribution.contradictions import (
    find_contradictions
)

from .analysis.temporal import (
    compare_observation_times
)

from .analysis.temporal_evidence import (
    build_temporal_evidence
)

from .analysis.infrastructure import (
    find_shared_infrastructure
)

from .analysis.infrastructure_evidence import (
    build_infrastructure_evidence
)
def investigate_dataset(
    dataset_path,
    source_reliability=0.85
):
    """
    Run the complete SIH26151 intelligence pipeline.

    Dataset
        ↓
    Validation
        ↓
    Observations
        ↓
    Entity Extraction
        ↓
    Entity Factory
        ↓
    Cross-Source Correlation
        ↓
    Relationships
        ↓
    Evidence
        ↓
    Temporal Analysis
        ↓
    Hypothesis
        ↓
    Supporting / Contradicting Evidence
        ↓
    Confidence
        ↓
    Assessment
    """

    # ==========================================
    # 1. LOAD DATASET
    # ==========================================

    records = load_json(
        dataset_path
    )

    # ==========================================
    # 2. VALIDATE DATASET
    # ==========================================

    valid_records, errors = validate_records(
        records
    )

    # ==========================================
    # 3. BUILD OBSERVATIONS
    # ==========================================

    observations = build_observations(
        valid_records,
        source_reliability=source_reliability
    )

    # ==========================================
    # 4. EXTRACT ENTITIES
    # ==========================================

    all_entities = []

    for observation in observations:

        entities = attach_entities_to_observation(
            observation
        )

        all_entities.extend(
            entities
        )

    # ==========================================
    # 5. REMOVE DUPLICATE ENTITIES
    # ==========================================

    unique_entities = {}

    for entity in all_entities:

        unique_entities[
            entity.entity_id
        ] = entity

    all_entities = list(
        unique_entities.values()
    )

    # ==========================================
    # 6. CROSS-SOURCE CORRELATION
    # ==========================================

    relationships = correlate_observations(
        observations,
        all_entities
    )

    # ==========================================
    # 7. NORMAL EVIDENCE GENERATION
    # ==========================================

    evidence = []

    for relationship in relationships:

        item = build_evidence(
            relationship,
            observations,
            all_entities
        )

        evidence.append(
            item
        )

    # ==========================================
    # Observation lookup
    # ==========================================

    observation_map = {
        observation.observation_id: observation
        for observation in observations
    }

    # ==========================================
    # 8. TEMPORAL EVIDENCE
    # ==========================================

    temporal_evidence = []

    for relationship in relationships:

        entity_a_id = relationship.source_entity_id
        entity_b_id = relationship.target_entity_id
    

        # --------------------------------------
        # Get ALL observations for each entity
        # --------------------------------------

        observations_a = [
            observation
            for observation in observations
            if entity_a_id in observation.entity_ids
        ]

        observations_b = [
            observation
            for observation in observations
            if entity_b_id in observation.entity_ids
        ]

        # Need observations for both identities
        if not observations_a or not observations_b:
            continue

        # --------------------------------------
        # Compare complete activity timelines
        # --------------------------------------

        temporal_result = (
            compare_observation_times(
                observations_a,
                observations_b
            )
        )

        # --------------------------------------
        # Convert temporal result to evidence
        # --------------------------------------

        item = build_temporal_evidence(
            entity_a_id,
            entity_b_id,
            observations_a,
            observations_b,
            temporal_result
        )

        if item:

            temporal_evidence.append(
                item
            )

    # ==========================================
    # Add temporal evidence
    # ==========================================

    evidence.extend(
        temporal_evidence
    )
        # ==========================================
    # 9. INFRASTRUCTURE EVIDENCE
    # ==========================================

    infrastructure_evidence = []

    for relationship in relationships:

        entity_a_id = relationship.source_entity_id
        entity_b_id = relationship.target_entity_id

        # --------------------------------------
        # Get ALL observations for each entity
        # --------------------------------------

        observations_a = [
            observation
            for observation in observations
            if entity_a_id in observation.entity_ids
        ]

        observations_b = [
            observation
            for observation in observations
            if entity_b_id in observation.entity_ids
        ]

        if not observations_a or not observations_b:
            continue

        # --------------------------------------
        # Find shared infrastructure
        # --------------------------------------

        shared_infrastructure = (
            find_shared_infrastructure(
                observations_a,
                observations_b,
                all_entities
            )
        )

        if not shared_infrastructure:
            continue

        # --------------------------------------
        # Convert to evidence
        # --------------------------------------

        items = build_infrastructure_evidence(
            entity_a_id,
            entity_b_id,
            observations_a,
            observations_b,
            shared_infrastructure
        )

        infrastructure_evidence.extend(
            items
        )

    # ==========================================
    # Add infrastructure evidence
    # ==========================================

    evidence.extend(
        infrastructure_evidence
    )
        # ==========================================
    # 10. ML PROFILE EVIDENCE
    # ==========================================

    ml_evidence = []

    for relationship in relationships:

        entity_a_id = relationship.source_entity_id
        entity_b_id = relationship.target_entity_id

        observations_a = [
            observation
            for observation in observations
            if entity_a_id in observation.entity_ids
        ]

        observations_b = [
            observation
            for observation in observations
            if entity_b_id in observation.entity_ids
        ]

        if not observations_a or not observations_b:
            continue

        profile_a_observations = [
            {
                "source": observation.source,
                "observed_at": observation.observed_at,
                "content": observation.content
            }
            for observation in observations_a
        ]

        profile_b_observations = [
            {
                "source": observation.source,
                "observed_at": observation.observed_at,
                "content": observation.content
            }
            for observation in observations_b
        ]

        comparison = compare_actor_profiles(
            profile_a_observations,
            profile_b_observations
        )

        items = build_ml_evidence(
            entity_a_id,
            entity_b_id,
            comparison
        )

        ml_evidence.extend(items)

    evidence.extend(
        ml_evidence
    )
    # ==========================================
    # 11. BUILD HYPOTHESES
    # ==========================================

    hypotheses = []

    for index, relationship in enumerate(
        relationships,
        start=1
    ):

        hypothesis = Hypothesis(

            hypothesis_id=(
                f"HYP-{index:03d}"
            ),

            description=(
                f"Entities "
                f"{relationship.source_entity_id} "
                f"and "
                f"{relationship.target_entity_id} "
                f"may belong to the same actor."
            ),

            entity_ids=[
                relationship.source_entity_id,
                relationship.target_entity_id
            ]
        )

        # ======================================
        # Supporting evidence
        # ======================================

        supporting_evidence = [

            item

            for item in evidence

            if set(
                hypothesis.entity_ids
            ).issubset(
                set(item.entity_ids)
            )

            and item.evidence_type.upper()
            not in {
                "CONTRADICTION",
                "CONFLICT",
                "DIFFERENT_INFRASTRUCTURE",
                "TEMPORAL_CONFLICT",
                "BEHAVIOR_CONFLICT"
            }
        ]

        # ======================================
        # Contradicting evidence
        # ======================================

        contradicting_evidence = (
            find_contradictions(
                hypothesis,
                evidence
            )
        )

         # ======================================
        # Calculate confidence
        # ======================================
        #
        # ML_STYLOMETRY and ML_BEHAVIOR are
        # explanatory components of ML_PROFILE.
        # Only ML_PROFILE contributes to the
        # attribution confidence to avoid
        # double-counting the same ML signal.
        # ======================================

        confidence_evidence = [
            item
            for item in supporting_evidence
            if item.evidence_type.upper()
            not in {
                "ML_STYLOMETRY",
                "ML_BEHAVIOR"
            }
        ]

        confidence = calculate_confidence(
            confidence_evidence,
            contradicting_evidence
        )

        assessment = assess_confidence(
            confidence
        )

        # ======================================
        # Update hypothesis
        # ======================================

        hypothesis.supporting_evidence_ids = [

            item.evidence_id

            for item in supporting_evidence
        ]

        hypothesis.contradicting_evidence_ids = [

            item.evidence_id

            for item in contradicting_evidence
        ]

        hypothesis.confidence = (
            confidence
        )

        hypothesis.assessment = (
            assessment
        )

        hypotheses.append(
            hypothesis
        )

    # ==========================================
    # 12. RETURN COMPLETE INVESTIGATION
    # ==========================================

    return {

        "records": records,

        "valid_records": valid_records,

        "validation_errors": errors,

        "observations": observations,

        "entities": all_entities,

        "relationships": relationships,

        "evidence": evidence,

        "hypotheses": hypotheses
    }


# ==============================================
# COMMAND-LINE EXECUTION
# ==============================================

if __name__ == "__main__":

    DATASET_PATH = (
    "ingestion/test_temporal_dataset.json"
)

    result = investigate_dataset(
        DATASET_PATH
    )

    print()
    print("======================================")
    print("SIH26151 INVESTIGATION ENGINE")
    print("======================================")

    # ------------------------------------------
    # Records
    # ------------------------------------------

    print()
    print("RECORDS")
    print("-------")

    print(
        f"Total: "
        f"{len(result['records'])}"
    )

    print(
        f"Valid: "
        f"{len(result['valid_records'])}"
    )

    print(
        f"Invalid: "
        f"{len(result['validation_errors'])}"
    )

    # ------------------------------------------
    # Observations
    # ------------------------------------------

    print()
    print("OBSERVATIONS")
    print("------------")

    for observation in result[
        "observations"
    ]:

        print(
            f"{observation.observation_id} | "
            f"{observation.source} | "
            f"{observation.entity_ids}"
        )

    # ------------------------------------------
    # Entities
    # ------------------------------------------

    print()
    print("ENTITIES")
    print("--------")

    for entity in result[
        "entities"
    ]:

        print(
            f"{entity.entity_id} | "
            f"{entity.entity_type} | "
            f"{entity.value}"
        )

    # ------------------------------------------
    # Relationships
    # ------------------------------------------

    print()
    print("RELATIONSHIPS")
    print("-------------")

    if not result["relationships"]:

        print(
            "No relationships found."
        )

    else:

        for relationship in result[
            "relationships"
        ]:

            print(
                f"{relationship.source_entity_id} "
                f"--[{relationship.relationship_type}]--> "
                f"{relationship.target_entity_id}"
            )

            print(
                f"Shared indicator: "
                f"{relationship.metadata.get('shared_indicator')}"
            )

    # ------------------------------------------
    # Evidence
    # ------------------------------------------

    print()
    print("EVIDENCE")
    print("--------")

    if not result["evidence"]:

        print(
            "No evidence generated."
        )

    else:

        for item in result[
            "evidence"
        ]:

            print(
                f"{item.evidence_id} | "
                f"{item.evidence_type} | "
                f"Reliability: "
                f"{item.reliability} | "
                f"Strength: "
                f"{item.strength}"
            )

    # ------------------------------------------
    # Hypotheses
    # ------------------------------------------

    print()
    print("HYPOTHESES")
    print("----------")

    if not result["hypotheses"]:

        print(
            "No hypotheses generated."
        )

    else:

        for hypothesis in result[
            "hypotheses"
        ]:

            print(
                f"{hypothesis.hypothesis_id} | "
                f"{hypothesis.assessment} | "
                f"{hypothesis.confidence}"
            )

            print(
                f"Supporting evidence: "
                f"{hypothesis.supporting_evidence_ids}"
            )

            print(
                f"Contradicting evidence: "
                f"{hypothesis.contradicting_evidence_ids}"
            )