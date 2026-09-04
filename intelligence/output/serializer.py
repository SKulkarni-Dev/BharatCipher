def entity_to_dict(entity):
    return {
        "entity_id": entity.entity_id,
        "entity_type": entity.entity_type,
        "value": entity.value,
        "source": entity.source,
        "first_seen": entity.first_seen,
        "last_seen": entity.last_seen,
        "metadata": entity.metadata
    }


def observation_to_dict(observation):
    return {
        "observation_id": observation.observation_id,
        "source": observation.source,
        "content": observation.content,
        "observed_at": observation.observed_at,
        "source_reliability": observation.source_reliability,
        "entity_ids": observation.entity_ids,
        "metadata": observation.metadata
    }


def relationship_to_dict(relationship):
    return {
        "relationship_id": relationship.relationship_id,
        "source_entity_id": relationship.source_entity_id,
        "target_entity_id": relationship.target_entity_id,
        "relationship_type": relationship.relationship_type,
        "strength": relationship.strength,
        "evidence_ids": relationship.evidence_ids,
        "source": relationship.source,
        "metadata": relationship.metadata
    }


def evidence_to_dict(evidence):
    return {
        "evidence_id": evidence.evidence_id,
        "evidence_type": evidence.evidence_type,
        "description": evidence.description,
        "source": evidence.source,
        "observed_at": evidence.observed_at,
        "entity_ids": evidence.entity_ids,
        "reliability": evidence.reliability,
        "strength": evidence.strength,
        "metadata": evidence.metadata
    }


def hypothesis_to_dict(hypothesis):
    return {
        "hypothesis_id": hypothesis.hypothesis_id,
        "description": hypothesis.description,
        "entity_ids": hypothesis.entity_ids,
        "supporting_evidence_ids": (
            hypothesis.supporting_evidence_ids
        ),
        "contradicting_evidence_ids": (
            hypothesis.contradicting_evidence_ids
        ),
        "confidence": hypothesis.confidence,
        "assessment": hypothesis.assessment,
        "metadata": hypothesis.metadata
    }


def investigation_to_dict(result):
    """
    Convert the complete investigation result
    into JSON-compatible Python dictionaries.
    """

    return {
        "records": result["records"],

        "valid_records": result[
            "valid_records"
        ],

        "validation_errors": result[
            "validation_errors"
        ],

        "observations": [
            observation_to_dict(item)
            for item in result["observations"]
        ],

        "entities": [
            entity_to_dict(item)
            for item in result["entities"]
        ],

        "relationships": [
            relationship_to_dict(item)
            for item in result["relationships"]
        ],

        "evidence": [
            evidence_to_dict(item)
            for item in result["evidence"]
        ],

        "hypotheses": [
            hypothesis_to_dict(item)
            for item in result["hypotheses"]
        ]
    }