from intelligence.models.entities import Entity, Actor
from intelligence.models.relationships import Relationship
from intelligence.models.evidence import Evidence
from intelligence.models.investigation import Investigation


# -----------------------------------------
# Create investigation
# -----------------------------------------

investigation = Investigation(
    investigation_id="INV-001",
    lead="shadowX"
)


# -----------------------------------------
# Create entities
# -----------------------------------------

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


# -----------------------------------------
# Create actor
# -----------------------------------------

actor = Actor(
    actor_id="ACTOR-001",
    name="Suspected Actor",
    entity_ids=[
        "ENT-001",
        "ENT-002"
    ]
)


# -----------------------------------------
# Create evidence
# -----------------------------------------

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


# -----------------------------------------
# Create relationship
# -----------------------------------------

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


# -----------------------------------------
# Add everything
# -----------------------------------------

investigation.add_entity(username)
investigation.add_entity(pgp)

investigation.add_actor(actor)

investigation.add_evidence(evidence)

investigation.add_relationship(relationship)


# -----------------------------------------
# Print result
# -----------------------------------------

print("INVESTIGATION SUMMARY")

print(
    investigation.summary()
)