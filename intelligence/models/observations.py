from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Observation:
    """
    Represents a single piece of collected intelligence
    from a specific source at a specific point in time.
    """

    observation_id: str

    source: str

    content: str

    observed_at: Optional[str] = None

    source_reliability: float = 0.0

    metadata: Dict = field(default_factory=dict)
    entity_ids: list[str] = field(default_factory=list)