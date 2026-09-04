from .extraction.extractor import extract_entities
from .models.entity_factory import create_entities
from .correlation.correlator import correlate_entities


def investigate(text, source="unknown"):
    """
    Run raw intelligence through the initial
    intelligence pipeline.

    Pipeline:

        Raw Text
            ↓
        Extraction
            ↓
        Entity Creation
            ↓
        Correlation
    """

    # ------------------------------------------
    # 1. Extract indicators
    # ------------------------------------------

    extracted = extract_entities(text)

    # ------------------------------------------
    # 2. Convert indicators into Entity objects
    # ------------------------------------------

    entities = create_entities(
        extracted,
        source=source
    )

    # ------------------------------------------
    # 3. Find direct correlations
    # ------------------------------------------

    relationships = correlate_entities(
        entities
    )

    # ------------------------------------------
    # Return structured result
    # ------------------------------------------

    return {
        "extracted": extracted,

        "entities": entities,

        "relationships": relationships
    }