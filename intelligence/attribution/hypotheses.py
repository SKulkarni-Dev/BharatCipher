from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Hypothesis:
    """
    Represents a possible attribution explanation.

    A hypothesis is NOT a confirmed attribution.
    It is a candidate explanation that can be
    supported or challenged by evidence.
    """

    hypothesis_id: str

    description: str

    entity_ids: List[str] = field(
        default_factory=list
    )

    supporting_evidence_ids: List[str] = field(
        default_factory=list
    )

    contradicting_evidence_ids: List[str] = field(
        default_factory=list
    )

    confidence: float = 0.0

    assessment: str = "UNASSESSED"

    metadata: Dict = field(
        default_factory=dict
    )