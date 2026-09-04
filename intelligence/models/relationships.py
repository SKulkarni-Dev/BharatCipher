from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Relationship:
    """
    Represents a relationship between two digital entities.
    """

    relationship_id: str

    source_entity_id: str
    target_entity_id: str

    relationship_type: str

    strength: float = 0.0

    evidence_ids: List[str] = field(default_factory=list)

    source: Optional[str] = None

    metadata: Dict = field(default_factory=dict)