def generate_report(result):
    lines = []

    lines.append("")
    lines.append("======================================")
    lines.append("SIH26151 INVESTIGATION REPORT")
    lines.append("======================================")

    # -------------------------
    # CASE SUMMARY
    # -------------------------

    lines.append("")
    lines.append("CASE SUMMARY")
    lines.append("------------")

    lines.append(
        f"Records analysed: {len(result['records'])}"
    )

    lines.append(
        f"Valid records: {len(result['valid_records'])}"
    )

    lines.append(
        f"Invalid records: {len(result['validation_errors'])}"
    )

    lines.append(
        f"Entities identified: {len(result['entities'])}"
    )

    lines.append(
        f"Relationships found: {len(result['relationships'])}"
    )

    lines.append(
        f"Evidence items: {len(result['evidence'])}"
    )

    # -------------------------
    # IDENTITIES
    # -------------------------

    lines.append("")
    lines.append("IDENTITIES")
    lines.append("----------")

    if not result["entities"]:
        lines.append("No identities identified.")
    else:
        for entity in result["entities"]:
            lines.append(
                f"- {entity.value} "
                f"({entity.entity_type})"
            )

    # -------------------------
    # POSSIBLE CONNECTIONS
    # -------------------------

    lines.append("")
    lines.append("POSSIBLE CONNECTIONS")
    lines.append("--------------------")

    if not result["relationships"]:
        lines.append(
            "No connections were identified."
        )
    else:
        for relationship in result["relationships"]:

            source_entity = next(
                (
                    entity
                    for entity in result["entities"]
                    if entity.entity_id
                    == relationship.source_entity_id
                ),
                None
            )

            target_entity = next(
                (
                    entity
                    for entity in result["entities"]
                    if entity.entity_id
                    == relationship.target_entity_id
                ),
                None
            )

            source_name = (
                source_entity.value
                if source_entity
                else relationship.source_entity_id
            )

            target_name = (
                target_entity.value
                if target_entity
                else relationship.target_entity_id
            )

            lines.append(
                f"- {source_name} ↔ {target_name}"
            )

            shared_indicator = (
                relationship.metadata.get(
                    "shared_indicator"
                )
            )

            if shared_indicator:
                lines.append(
                    f"  Shared indicator: "
                    f"{shared_indicator}"
                )

    # -------------------------
    # EVIDENCE
    # -------------------------

    lines.append("")
    lines.append("EVIDENCE")
    lines.append("--------")

    if not result["evidence"]:
        lines.append("No evidence generated.")
    else:
        for evidence in result["evidence"]:

            lines.append(
                f"- {evidence.evidence_type}"
            )

            lines.append(
                f"  {evidence.description}"
            )

            lines.append(
                f"  Strength: "
                f"{evidence.strength:.0%}"
            )

            lines.append(
                f"  Reliability: "
                f"{evidence.reliability:.0%}"
            )

    # -------------------------
    # ASSESSMENT
    # -------------------------

    lines.append("")
    lines.append("ASSESSMENT")
    lines.append("----------")

    if not result["hypotheses"]:
        lines.append(
            "No attribution assessment generated."
        )
    else:
        for hypothesis in result["hypotheses"]:

            lines.append(
                f"Assessment: "
                f"{hypothesis.assessment}"
            )

            lines.append(
                f"Confidence: "
                f"{hypothesis.confidence:.2%}"
            )

            # Find readable entity names
            entity_names = []

            for entity_id in hypothesis.entity_ids:
                entity = next(
                    (
                        e
                        for e in result["entities"]
                        if e.entity_id == entity_id
                    ),
                    None
                )

                if entity:
                    entity_names.append(
                        entity.value
                    )

            # Create human-readable explanation
            if len(entity_names) >= 2:
                explanation = (
                    f"{entity_names[0]} and "
                    f"{entity_names[1]} may belong "
                    f"to the same actor."
                )
            else:
                explanation = hypothesis.description

            lines.append(
                f"Explanation: {explanation}"
            )

            if hypothesis.contradicting_evidence_ids:
                lines.append(
                    "Contradicting evidence: "
                    f"{len(hypothesis.contradicting_evidence_ids)}"
                )
            else:
                lines.append(
                    "Contradicting evidence: None found"
                )

    # -------------------------
    # IMPORTANT NOTICE
    # -------------------------

    lines.append("")
    lines.append("IMPORTANT")
    lines.append("---------")

    lines.append(
        "This is an analytical assessment based "
        "on the available evidence."
    )

    lines.append(
        "A high-confidence result does not by "
        "itself prove the real-world identity "
        "of an individual."
    )

    return "\n".join(lines)