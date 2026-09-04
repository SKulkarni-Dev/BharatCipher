from intelligence.models.entities import Entity
from intelligence.correlation.correlator import correlate_entities


entities = [

    Entity(
        entity_id="ENT-001",
        entity_type="username",
        value="shadowX",
        source="dataset-A"
    ),

    Entity(
        entity_id="ENT-002",
        entity_type="username",
        value="shadowX",
        source="dataset-B"
    ),

    Entity(
        entity_id="ENT-003",
        entity_type="pgp",
        value="PGP-ABC123",
        source="dataset-A"
    ),

    Entity(
        entity_id="ENT-004",
        entity_type="pgp",
        value="PGP-ABC123",
        source="dataset-B"
    ),

    Entity(
        entity_id="ENT-005",
        entity_type="wallet",
        value="WALLET-001",
        source="dataset-A"
    )
]


relationships = correlate_entities(
    entities
)


print("CORRELATION RESULTS")
print("-------------------")

for relationship in relationships:

    print(
        f"{relationship.source_entity_id} "
        f"--[{relationship.relationship_type}]--> "
        f"{relationship.target_entity_id}"
    )