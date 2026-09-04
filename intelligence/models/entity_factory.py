import hashlib

from .entities import Entity


def generate_entity_id(entity_type, value):
    """
    Generate a stable entity ID from the entity type
    and normalized value.
    """

    normalized = (
        f"{entity_type}:{value}"
        .lower()
        .strip()
    )

    digest = hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()[:12]

    return f"ENT-{digest.upper()}"


def create_entities(extracted_data, source=None):
    """
    Convert extracted indicator dictionaries into
    Entity objects.

    Input:
        {
            "username": ["shadowX", "shadow_88"],
            "pgp": ["PGP-ABC123"],
            "wallet": ["WALLET-001"],
            "domain": ["dark-example.onion"]
        }

    Output:
        List[Entity]
    """

    entities = []

    for entity_type, values in extracted_data.items():

        for value in values:

            entity = Entity(
                entity_id=generate_entity_id(
                    entity_type,
                    value
                ),

                entity_type=entity_type,

                value=value,

                source=source
            )

            entities.append(entity)

    return entities