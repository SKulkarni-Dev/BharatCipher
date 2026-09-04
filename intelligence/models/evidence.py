from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Evidence:
    """
    Represents a piece of evidence collected during
    a threat-actor investigation.
    """

    evidence_id: str

    evidence_type: str

    description: str

    source: str

    observed_at: Optional[str] = None

    entity_ids: List[str] = field(default_factory=list)

    reliability: float = 0.0

    strength: float = 0.0

    metadata: Dict = field(default_factory=dict)