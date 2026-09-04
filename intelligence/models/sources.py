from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class IntelligenceSource:
    """
    Represents a source of intelligence used by an investigation.
    """

    source_id: str

    name: str

    source_type: str

    reliability: float = 0.0

    last_updated: Optional[str] = None

    metadata: Dict = field(default_factory=dict)