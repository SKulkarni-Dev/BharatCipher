from intelligence.models.observations import Observation


observation = Observation(
    observation_id="OBS-001",

    source="controlled_dataset_A",

    content="shadowX was associated with PGP-ABC123.",

    observed_at="2026-08-30T09:30:00Z",

    source_reliability=0.90
    
)


print("OBSERVATION")
print("-----------")

print(observation)