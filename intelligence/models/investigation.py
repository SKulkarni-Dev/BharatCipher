from dataclasses import dataclass, field
from typing import Dict, List

from .entities import Entity, Actor
from .relationships import Relationship
from .evidence import Evidence

@dataclass
class Investigation:
    """
    Represents the complete intelligence state of a case.
    """

    investigation_id: str

    lead: str

    actors: Dict[str, Actor] = field(default_factory=dict)

    entities: Dict[str, Entity] = field(default_factory=dict)

    relationships: Dict[str, Relationship] = field(default_factory=dict)

    evidence: Dict[str, Evidence] = field(default_factory=dict)

    def add_actor(self, actor: Actor):
        self.actors[actor.actor_id] = actor

    def add_entity(self, entity: Entity):
        self.entities[entity.entity_id] = entity

    def add_relationship(self, relationship: Relationship):
        self.relationships[
            relationship.relationship_id
        ] = relationship

    def add_evidence(self, evidence: Evidence):
        self.evidence[
            evidence.evidence_id
        ] = evidence

    def summary(self):
        return {
            "investigation_id": self.investigation_id,
            "lead": self.lead,
            "actors": len(self.actors),
            "entities": len(self.entities),
            "relationships": len(self.relationships),
            "evidence": len(self.evidence)
        }
        