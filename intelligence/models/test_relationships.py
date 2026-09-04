from intelligence.models.relationships import Relationship


relationship = Relationship(
    relationship_id="REL-001",

    source_entity_id="ENT-001",

    target_entity_id="ENT-002",

    relationship_type="SAME_PGP",

    strength=0.95,

    evidence_ids=[
        "EVID-001"
    ],

    source="controlled_dataset"
)


print("RELATIONSHIP")
print(relationship)