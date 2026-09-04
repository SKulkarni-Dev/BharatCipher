import re
from difflib import SequenceMatcher


def normalize(value):
    """
    Normalize a digital identifier before comparison.
    """

    if value is None:
        return ""

    value = str(value).lower().strip()

    # Remove common separators
    value = re.sub(r"[\s_.-]+", "", value)

    return value


def string_similarity(value_a, value_b):
    """
    Calculate similarity between two strings.
    """

    a = normalize(value_a)
    b = normalize(value_b)

    if not a or not b:
        return 0.0

    return SequenceMatcher(
        None,
        a,
        b
    ).ratio()


def exact_match(value_a, value_b):
    """
    Check whether two indicators match exactly
    after normalization.
    """

    a = normalize(value_a)
    b = normalize(value_b)

    if not a or not b:
        return False

    return a == b


def resolve_identity(candidate_a, candidate_b):
    """
    Compare two candidate identities using available
    digital indicators.

    Returns an explainable resolution assessment.
    """

    signals = []
    supporting = []
    contradicting = []

    # --------------------------------------------------
    # Username
    # --------------------------------------------------

    username_a = candidate_a.get("username")
    username_b = candidate_b.get("username")

    username_score = string_similarity(
        username_a,
        username_b
    )

    if username_score >= 0.90:

        supporting.append({
            "signal": "username_similarity",
            "score": round(username_score, 3),
            "reason": "Very similar usernames."
        })

    elif username_score >= 0.70:

        supporting.append({
            "signal": "username_similarity",
            "score": round(username_score, 3),
            "reason": "Moderately similar usernames."
        })

    signals.append({
        "name": "username_similarity",
        "score": username_score
    })

    # --------------------------------------------------
    # PGP
    # --------------------------------------------------

    pgp_a = candidate_a.get("pgp")
    pgp_b = candidate_b.get("pgp")

    if exact_match(pgp_a, pgp_b):

        supporting.append({
            "signal": "pgp_match",
            "score": 1.0,
            "reason": "Same PGP identifier."
        })

        pgp_score = 1.0

    else:

        pgp_score = 0.0

    signals.append({
        "name": "pgp_match",
        "score": pgp_score
    })

    # --------------------------------------------------
    # Wallet
    # --------------------------------------------------

    wallet_a = candidate_a.get("wallet")
    wallet_b = candidate_b.get("wallet")

    if exact_match(wallet_a, wallet_b):

        supporting.append({
            "signal": "wallet_match",
            "score": 1.0,
            "reason": "Same wallet identifier."
        })

        wallet_score = 1.0

    else:

        wallet_score = 0.0

    signals.append({
        "name": "wallet_match",
        "score": wallet_score
    })

    # --------------------------------------------------
    # Domain / Infrastructure
    # --------------------------------------------------

    domain_a = candidate_a.get("domain")
    domain_b = candidate_b.get("domain")

    if exact_match(domain_a, domain_b):

        supporting.append({
            "signal": "domain_match",
            "score": 1.0,
            "reason": "Same infrastructure domain."
        })

        domain_score = 1.0

    else:

        domain_score = 0.0

    signals.append({
        "name": "domain_match",
        "score": domain_score
    })

    # --------------------------------------------------
    # Weighted score
    # --------------------------------------------------

    weights = {
        "username_similarity": 0.20,
        "pgp_match": 0.35,
        "wallet_match": 0.25,
        "domain_match": 0.20
    }

    score = (
        username_score * weights["username_similarity"]
        +
        pgp_score * weights["pgp_match"]
        +
        wallet_score * weights["wallet_match"]
        +
        domain_score * weights["domain_match"]
    )

    # --------------------------------------------------
    # Assessment
    # --------------------------------------------------

    if score >= 0.75:

        assessment = "STRONG_CANDIDATE"

    elif score >= 0.50:

        assessment = "POSSIBLE_MATCH"

    elif score >= 0.30:

        assessment = "WEAK_ASSOCIATION"

    else:

        assessment = "INSUFFICIENT_EVIDENCE"

    return {
        "score": round(score, 4),
        "assessment": assessment,
        "signals": signals,
        "supporting_evidence": supporting,
        "contradicting_evidence": contradicting
    }