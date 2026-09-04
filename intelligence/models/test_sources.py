from intelligence.models.sources import IntelligenceSource


source = IntelligenceSource(
    source_id="SRC-001",

    name="Public CTI Dataset",

    source_type="DATASET",

    reliability=0.90,

    last_updated="2026-08-30T18:30:00Z"
)


print("INTELLIGENCE SOURCE")
print("-------------------")
print(source)