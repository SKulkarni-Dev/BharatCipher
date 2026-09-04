import re


# ------------------------------------------
# Specific indicators
# ------------------------------------------

PGP_PATTERN = r"\bPGP-[A-Z0-9-]+\b"

WALLET_PATTERN = r"\bWALLET-[A-Z0-9-]+\b"

DOMAIN_PATTERN = (
    r"\b[a-zA-Z0-9-]+"
    r"(?:\.[a-zA-Z0-9-]+)*"
    r"\.onion\b"
)


# ------------------------------------------
# Username patterns
# ------------------------------------------

USERNAME_EXPLICIT_PATTERN = (
    r"\b(?:username|user|account|alias)\s*[:=]\s*"
    r"([A-Za-z0-9_][A-Za-z0-9_-]{2,31})"
)


USERNAME_CONTEXT_PATTERNS = [

    # Example:
    # User shadowX
    r"\b(?:User|Username|Account|Alias)\s+"
    r"([A-Za-z0-9_][A-Za-z0-9_-]{2,31})",

    # Example:
    # shadow_88 was associated with PGP-A
    r"\b([A-Za-z0-9_][A-Za-z0-9_-]{2,31})"
    r"\s+was\s+associated\s+with\b",

    # Example:
    # shadowX was observed
    r"\b([A-Za-z0-9_][A-Za-z0-9_-]{2,31})"
    r"\s+was\s+observed\b"
]


# ------------------------------------------
# Entity extraction
# ------------------------------------------

def extract_entities(text):
    """
    Extract structured digital indicators
    from investigation text.

    Supported entity types:

        username
        pgp
        wallet
        domain
    """

    if not text:
        return {}

    results = {}

    # --------------------------------------
    # PGP
    # --------------------------------------

    pgps = re.findall(
        PGP_PATTERN,
        text,
        re.IGNORECASE
    )

    if pgps:
        results["pgp"] = list(
            dict.fromkeys(pgps)
        )

    # --------------------------------------
    # Wallet
    # --------------------------------------

    wallets = re.findall(
        WALLET_PATTERN,
        text,
        re.IGNORECASE
    )

    if wallets:
        results["wallet"] = list(
            dict.fromkeys(wallets)
        )

    # --------------------------------------
    # Domain
    # --------------------------------------

    domains = re.findall(
        DOMAIN_PATTERN,
        text,
        re.IGNORECASE
    )

    if domains:
        results["domain"] = list(
            dict.fromkeys(domains)
        )

    # --------------------------------------
    # Username
    # --------------------------------------

    usernames = []

    # Context-based extraction
    for pattern in USERNAME_CONTEXT_PATTERNS:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        usernames.extend(matches)

    # Explicit extraction
    explicit_matches = re.findall(
        USERNAME_EXPLICIT_PATTERN,
        text,
        re.IGNORECASE
    )

    usernames.extend(explicit_matches)

    # --------------------------------------
    # Remove obvious non-usernames
    # --------------------------------------

    stopwords = {
        "the",
        "same",
        "user",
        "username",
        "account",
        "alias",
        "was",
        "using",
        "observed",
        "associated",
        "with",
        "both",
        "domain",
        "wallet",
        "pgp",
        "fingerprint"
    }

    usernames = [
        username
        for username in usernames
        if username.lower() not in stopwords
        and not username.upper().startswith(
            ("PGP-", "WALLET-")
        )
    ]

    # --------------------------------------
    # Remove duplicates
    # --------------------------------------

    usernames = list(
        dict.fromkeys(usernames)
    )

    if usernames:
        results["username"] = usernames

    # --------------------------------------
    # Return results
    # --------------------------------------

    return results