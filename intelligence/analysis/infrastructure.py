from collections import defaultdict


INFRASTRUCTURE_TYPES = {
    "domain",
    "wallet"
}


def find_shared_infrastructure(
    observations_a,
    observations_b,
    entities
):
    """
    Find technical infrastructure indicators
    shared between two identities.

    Currently supported:
        - domain
        - wallet

    Returns a list of shared infrastructure
    entity objects.
    """

    entity_map = {
        entity.entity_id: entity
        for entity in entities
    }

    indicators_a = {}
    indicators_b = {}

    # ------------------------------------------
    # Collect infrastructure for entity A
    # ------------------------------------------

    for observation in observations_a:

        for entity_id in observation.entity_ids:

            entity = entity_map.get(entity_id)

            if entity is None:
                continue

            if (
                entity.entity_type.lower()
                not in INFRASTRUCTURE_TYPES
            ):
                continue

            normalized = (
                entity.value.lower().strip()
            )

            indicators_a[normalized] = entity

    # ------------------------------------------
    # Collect infrastructure for entity B
    # ------------------------------------------

    for observation in observations_b:

        for entity_id in observation.entity_ids:

            entity = entity_map.get(entity_id)

            if entity is None:
                continue

            if (
                entity.entity_type.lower()
                not in INFRASTRUCTURE_TYPES
            ):
                continue

            normalized = (
                entity.value.lower().strip()
            )

            indicators_b[normalized] = entity

    # ------------------------------------------
    # Find intersection
    # ------------------------------------------

    shared_values = (
        set(indicators_a.keys())
        &
        set(indicators_b.keys())
    )

    return [
        indicators_a[value]
        for value in sorted(shared_values)
    ]