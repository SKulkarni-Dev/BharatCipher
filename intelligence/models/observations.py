from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Observation:
    """
    Represents a single piece of collected intelligence
    from a specific source at a specific point in time.

    Provenance fields describe where the observation came from,
    how it was collected, and whether its integrity/authenticity
    has been established.
    """

    observation_id: str

    source: str

    content: str

    observed_at: Optional[str] = None

    source_reliability: float = 0.0

    # Provenance
    source_type: str = "unknown"

    collection_method: str = "unknown"

    collection_time: Optional[str] = None

    source_reference: Optional[str] = None

    original_timestamp: Optional[str] = None

    # Integrity
    content_hash: Optional[str] = None

    integrity_status: str = "UNVERIFIED"

    metadata: Dict = field(default_factory=dict)

    entity_ids: list[str] = field(default_factory=list)