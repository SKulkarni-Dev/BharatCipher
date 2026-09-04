from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Entity:
    """Represents a digital entity associated with an investigation."""

    entity_id: str
    entity_type: str
    value: str

    source: Optional[str] = None
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None

    metadata: Dict = field(default_factory=dict)


@dataclass
class Actor:
    """Represents a suspected threat actor.An actor can be associated with multiple digital entities."""

    actor_id: str
    name: Optional[str] = None

    entity_ids: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)