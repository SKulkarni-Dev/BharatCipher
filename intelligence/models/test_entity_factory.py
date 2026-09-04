from intelligence.models.entity_factory import create_entities


extracted_data = {

    "username": [
        "shadowX",
        "shadow_88"
    ],

    "pgp": [
        "PGP-ABC123"
    ],

    "wallet": [
        "WALLET-001"
    ],

    "domain": [
        "dark-example.onion"
    ]
}


entities = create_entities(
    extracted_data,
    source="controlled_dataset"
)


print("CREATED ENTITIES")
print("-----------------")

for entity in entities:

    print(
        f"{entity.entity_id} | "
        f"{entity.entity_type} | "
        f"{entity.value} | "
        f"{entity.source}"
    )