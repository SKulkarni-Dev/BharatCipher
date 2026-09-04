from intelligence.models.observations import Observation
from intelligence.models.entities import Entity

from intelligence.analysis.infrastructure import (
    find_shared_infrastructure
)

from intelligence.analysis.infrastructure_evidence import (
    build_infrastructure_evidence
)


# ==========================================
# TEST DATA
# ==========================================

domain = Entity(
    entity_id="ENT-DOMAIN",
    entity_type="domain",
    value="shared-example.onion",
    source="dataset_A",
    metadata={}
)


wallet = Entity(
    entity_id="ENT-WALLET",
    entity_type="wallet",
    value="WALLET-001",
    source="dataset_A",
    metadata={}
)


observation_a = Observation(
    observation_id="OBS-A",
    source="dataset_A",
    content="shadowX used shared infrastructure.",
    observed_at="2026-08-28T10:00:00Z",
    source_reliability=0.90,
    entity_ids=[
        "ENT-A",
        "ENT-DOMAIN",
        "ENT-WALLET"
    ]
)


observation_b = Observation(
    observation_id="OBS-B",
    source="dataset_B",
    content="shadow_88 used shared infrastructure.",
    observed_at="2026-08-29T10:00:00Z",
    source_reliability=0.80,
    entity_ids=[
        "ENT-B",
        "ENT-DOMAIN",
        "ENT-WALLET"
    ]
)


# ==========================================
# FIND SHARED INFRASTRUCTURE
# ==========================================

shared = find_shared_infrastructure(

    [observation_a],

    [observation_b],

    [
        domain,
        wallet
    ]
)


print("INFRASTRUCTURE ANALYSIS")
print("-----------------------")

for item in shared:

    print(
        f"{item.entity_type}: "
        f"{item.value}"
    )


# ==========================================
# BUILD EVIDENCE
# ==========================================

evidence = build_infrastructure_evidence(

    "ENT-A",

    "ENT-B",

    [observation_a],

    [observation_b],

    shared
)


print()
print("INFRASTRUCTURE EVIDENCE")
print("-----------------------")

for item in evidence:

    print(item)