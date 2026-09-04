from intelligence.resolution.resolver import resolve_identity


candidate_a = {
    "username": "shadowX",
    "pgp": "PGP-ABC123",
    "wallet": "WALLET-001",
    "domain": "dark-example.onion"
}


candidate_b = {
    "username": "shadow_88",
    "pgp": "PGP-ABC123",
    "wallet": "WALLET-002",
    "domain": "dark-example.onion"
}


result = resolve_identity(
    candidate_a,
    candidate_b
)


print("IDENTITY RESOLUTION")
print("-------------------")

print(
    f"Score: {result['score']}"
)

print(
    f"Assessment: {result['assessment']}"
)

print("\nSupporting Evidence:")

for evidence in result["supporting_evidence"]:

    print(
        f"+ {evidence['signal']}: "
        f"{evidence['reason']}"
    )

print("\nContradicting Evidence:")

for evidence in result["contradicting_evidence"]:

    print(
        f"- {evidence['signal']}: "
        f"{evidence['reason']}"
    )