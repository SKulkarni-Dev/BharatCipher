from intelligence.models.observations import Observation

from intelligence.analysis.temporal import (
    compare_observation_times
)

from intelligence.analysis.temporal_evidence import (
    build_temporal_evidence
)


# ==========================================
# TEST 1 — TEMPORAL OVERLAP
# ==========================================

observations_a = [

    Observation(
        observation_id="OBS-A1",
        source="dataset_A",
        content="shadowX activity",
        observed_at="2026-08-28T10:00:00Z",
        source_reliability=0.90,
        entity_ids=["ENT-A"]
    ),

    Observation(
        observation_id="OBS-A2",
        source="dataset_A",
        content="shadowX activity",
        observed_at="2026-08-30T10:00:00Z",
        source_reliability=0.90,
        entity_ids=["ENT-A"]
    )
]


observations_b = [

    Observation(
        observation_id="OBS-B1",
        source="dataset_B",
        content="shadow_88 activity",
        observed_at="2026-08-29T10:00:00Z",
        source_reliability=0.85,
        entity_ids=["ENT-B"]
    )
]


temporal_result = compare_observation_times(
    observations_a,
    observations_b
)


print("TEMPORAL ANALYSIS")
print("-----------------")
print(
    f"Result: {temporal_result}"
)


temporal_evidence = build_temporal_evidence(
    "ENT-A",
    "ENT-B",
    observations_a,
    observations_b,
    temporal_result
)


print()
print("TEMPORAL EVIDENCE")
print("-----------------")
print(temporal_evidence)


# ==========================================
# TEST 2 — NON-OVERLAPPING ACTIVITY
# ==========================================

observations_c = [

    Observation(
        observation_id="OBS-C1",
        source="dataset_C",
        content="shadowX activity",
        observed_at="2026-08-01T10:00:00Z",
        source_reliability=0.90,
        entity_ids=["ENT-A"]
    )
]


observations_d = [

    Observation(
        observation_id="OBS-D1",
        source="dataset_D",
        content="shadow_88 activity",
        observed_at="2026-08-20T10:00:00Z",
        source_reliability=0.85,
        entity_ids=["ENT-B"]
    )
]


temporal_result_2 = compare_observation_times(
    observations_c,
    observations_d
)


print()
print("NON-OVERLAPPING TEST")
print("--------------------")
print(
    f"Result: {temporal_result_2}"
)


temporal_evidence_2 = build_temporal_evidence(
    "ENT-A",
    "ENT-B",
    observations_c,
    observations_d,
    temporal_result_2
)


print()
print("TEMPORAL EVIDENCE")
print("-----------------")
print(temporal_evidence_2)