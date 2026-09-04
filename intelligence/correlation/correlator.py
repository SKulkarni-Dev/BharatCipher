from collections import defaultdict

from ..models.relationships import Relationship


# ==========================================
# Indicators that can mediate a correlation
# ==========================================

CORRELATION_INDICATOR_TYPES = {
    "pgp",
    "wallet",
    "domain"
}


def correlate_observations(observations, entities):
    """
    Correlate identities across observations using
    shared technical indicators.

    Example:

        Observation 1:
            shadowX + PGP-A

        Observation 2:
            shadow_88 + PGP-A

    Result:

        shadowX --SHARES_PGP--> shadow_88

    Important:
        - PGP, wallet and domain act as shared indicators.
        - Username is treated as an identity, not a
          correlation indicator.
        - Self-relationships are never created.
        - Duplicate relationships are removed.
        - Provenance is preserved.
    """

    # ==========================================
    # 1. Entity lookup
    # ==========================================

    entity_map = {
        entity.entity_id: entity
        for entity in entities
    }

    # ==========================================
    # 2. Find indicator occurrences
    # ==========================================

    indicator_observations = defaultdict(list)

    for observation in observations:

        for entity_id in observation.entity_ids:

            entity = entity_map.get(entity_id)

            if entity is None:
                continue

            entity_type = (
                entity.entity_type
                .lower()
                .strip()
            )

            # ----------------------------------
            # Only technical indicators mediate
            # cross-observation correlation.
            # ----------------------------------

            if entity_type not in CORRELATION_INDICATOR_TYPES:
                continue

            indicator_observations[
                entity.entity_id
            ].append(
                {
                    "observation": observation,
                    "entity": entity
                }
            )

    relationships = []

    # ==========================================
    # 3. Prevent duplicate relationships
    # ==========================================

    relationship_keys = set()

    relationship_counter = 1

    # ==========================================
    # 4. Process shared indicators
    # ==========================================

    for indicator_id, occurrences in (
        indicator_observations.items()
    ):

        if len(occurrences) < 2:
            continue

        shared_indicator = (
            entity_map.get(indicator_id)
        )

        if shared_indicator is None:
            continue

        # ======================================
        # Compare observation pairs
        # ======================================

        for i in range(len(occurrences)):

            for j in range(
                i + 1,
                len(occurrences)
            ):

                first = occurrences[i]
                second = occurrences[j]

                observation_a = (
                    first["observation"]
                )

                observation_b = (
                    second["observation"]
                )

                # ----------------------------------
                # Same observation is not a
                # cross-observation correlation.
                # ----------------------------------

                if (
                    observation_a.observation_id
                    ==
                    observation_b.observation_id
                ):
                    continue

                # ==================================
                # Get identity entities from A
                # ==================================

                entities_a = []

                for entity_id in (
                    observation_a.entity_ids
                ):

                    if entity_id == indicator_id:
                        continue

                    entity = entity_map.get(
                        entity_id
                    )

                    if entity is None:
                        continue

                    # We currently correlate
                    # identities such as usernames.
                    #
                    # Do not use another technical
                    # indicator as an endpoint.

                    if (
                        entity.entity_type.lower()
                        in CORRELATION_INDICATOR_TYPES
                    ):
                        continue

                    entities_a.append(entity)

                # ==================================
                # Get identity entities from B
                # ==================================

                entities_b = []

                for entity_id in (
                    observation_b.entity_ids
                ):

                    if entity_id == indicator_id:
                        continue

                    entity = entity_map.get(
                        entity_id
                    )

                    if entity is None:
                        continue

                    if (
                        entity.entity_type.lower()
                        in CORRELATION_INDICATOR_TYPES
                    ):
                        continue

                    entities_b.append(entity)

                # ==================================
                # Create relationships
                # ==================================

                for entity_a in entities_a:

                    for entity_b in entities_b:

                        # --------------------------
                        # Never create self-links
                        # --------------------------

                        if (
                            entity_a.entity_id
                            ==
                            entity_b.entity_id
                        ):
                            continue

                        # --------------------------
                        # Normalize direction
                        # so A→B and B→A are
                        # treated as the same pair.
                        # --------------------------

                        endpoint_pair = tuple(
                            sorted(
                                [
                                    entity_a.entity_id,
                                    entity_b.entity_id
                                ]
                            )
                        )

                        relationship_key = (
                            endpoint_pair[0],
                            endpoint_pair[1],
                            shared_indicator.entity_id
                        )

                        # --------------------------
                        # Remove duplicates
                        # --------------------------

                        if (
                            relationship_key
                            in relationship_keys
                        ):
                            continue

                        relationship_keys.add(
                            relationship_key
                        )

                        # ==================================
                        # Build relationship
                        # ==================================

                        relationship = Relationship(

                            relationship_id=(
                                f"REL-"
                                f"{relationship_counter:03d}"
                            ),

                            source_entity_id=(
                                entity_a.entity_id
                            ),

                            target_entity_id=(
                                entity_b.entity_id
                            ),

                            relationship_type=(
                                f"SHARES_"
                                f"{shared_indicator.entity_type.upper()}"
                            ),

                            strength=1.0,

                            evidence_ids=[],

                            source=(
                                "indicator_mediated_correlation"
                            ),

                            metadata={

                                "shared_indicator": (
                                    shared_indicator.value
                                ),

                                "shared_indicator_id": (
                                    shared_indicator.entity_id
                                ),

                                "observation_ids": [
                                    observation_a.observation_id,
                                    observation_b.observation_id
                                ],

                                "sources": list(
                                    dict.fromkeys(
                                        [
                                            observation_a.source,
                                            observation_b.source
                                        ]
                                    )
                                )
                            }
                        )

                        relationships.append(
                            relationship
                        )

                        relationship_counter += 1

    return relationships


def correlate_entities(entities):
    """
    Simple direct entity-to-entity correlation.

    Unlike correlate_observations(), this works on a flat
    list of entities with no observation context. Entities
    that share the same entity_type and the same normalized
    value (but have different entity_id) are linked.

    Used by the lightweight intelligence/pipeline.py flow
    (raw text -> extraction -> entities -> correlation).
    """

    groups = defaultdict(list)

    for entity in entities:

        key = (
            entity.entity_type.lower().strip(),
            entity.value.lower().strip()
        )

        groups[key].append(entity)

    relationships = []

    relationship_keys = set()

    relationship_counter = 1

    for (entity_type, _value), group in groups.items():

        if len(group) < 2:
            continue

        for i in range(len(group)):

            for j in range(i + 1, len(group)):

                entity_a = group[i]
                entity_b = group[j]

                if entity_a.entity_id == entity_b.entity_id:
                    continue

                endpoint_pair = tuple(
                    sorted([entity_a.entity_id, entity_b.entity_id])
                )

                if endpoint_pair in relationship_keys:
                    continue

                relationship_keys.add(endpoint_pair)

                relationships.append(
                    Relationship(
                        relationship_id=f"REL-{relationship_counter:03d}",
                        source_entity_id=endpoint_pair[0],
                        target_entity_id=endpoint_pair[1],
                        relationship_type=f"SAME_{entity_type.upper()}",
                        strength=1.0,
                        evidence_ids=[],
                        source="direct_entity_correlation",
                        metadata={
                            "shared_value": entity_a.value
                        }
                    )
                )

                relationship_counter += 1

    return relationships