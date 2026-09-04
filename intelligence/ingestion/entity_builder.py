from ..extraction.extractor import extract_entities
from ..models.entity_factory import create_entities


def attach_entities_to_observation(
    observation,
    source=None
):
    """
    Extract entities from an observation's content
    and attach their IDs to the observation.
    """

    extracted = extract_entities(
        observation.content
    )

    entities = create_entities(
        extracted,
        source=source or observation.source
    )

    observation.entity_ids = [
        entity.entity_id
        for entity in entities
    ]

    return entities