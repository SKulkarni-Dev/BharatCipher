from intelligence.models.evidence import Evidence


evidence = Evidence(
    evidence_id="EVID-001",

    evidence_type="PGP_MATCH",

    description="Same PGP fingerprint observed across two identities.",

    source="controlled_dataset",

    observed_at="2026-08-30T10:30:00Z",

    entity_ids=[
        "ENT-001",
        "ENT-002"
    ],

    reliability=0.95,

    strength=0.90
)


print("EVIDENCE")
print(evidence)