from intelligence.extraction.extractor import extract_entities


text = """
User shadowX was observed using shadow_88.
The same PGP fingerprint PGP-ABC123 was associated
with both identities.
Wallet WALLET-001 was also observed.
Domain dark-example.onion was referenced.
"""


results = extract_entities(text)


print("EXTRACTED ENTITIES")

for entity_type, values in results.items():

    print(f"\n{entity_type.upper()}")

    for value in values:

        print(f"  {value}")