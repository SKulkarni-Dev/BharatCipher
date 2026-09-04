from intelligence.models.entities import Entity, Actor


username = Entity(
    entity_id="ENT-001",
    entity_type="username",
    value="shadowX",
    source="controlled_dataset"
)

pgp = Entity(
    entity_id="ENT-002",
    entity_type="pgp",
    value="PGP-ABC123",
    source="controlled_dataset"
)

actor = Actor(
    actor_id="ACTOR-001",
    name="Suspected Actor",
    entity_ids=[
        username.entity_id,
        pgp.entity_id
    ]
)


print("ENTITY")
print(username)

print("\nACTOR")
print(actor)