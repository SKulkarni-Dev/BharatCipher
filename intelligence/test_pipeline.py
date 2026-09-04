from intelligence.pipeline import investigate


text = """
User shadowX was observed using shadow_88.
The same PGP fingerprint PGP-ABC123 was associated
with both identities.
Wallet WALLET-001 was also observed.
Domain dark-example.onion was referenced.
"""


result = investigate(
    text,
    source="controlled_dataset"
)


print("================================")
print("SIH26151 INTELLIGENCE PIPELINE")
print("================================")


print("\nEXTRACTED")
print("---------")

for entity_type, values in result["extracted"].items():

    print(
        entity_type.upper(),
        "→",
        values
    )


print("\nENTITIES")
print("--------")

for entity in result["entities"]:

    print(
        f"{entity.entity_id} | "
        f"{entity.entity_type} | "
        f"{entity.value}"
    )


print("\nRELATIONSHIPS")
print("-------------")

for relationship in result["relationships"]:

    print(
        f"{relationship.source_entity_id} "
        f"--[{relationship.relationship_type}]--> "
        f"{relationship.target_entity_id}"
    )