from database import add_claim as database_add_claim
from database import get_all_claims as database_get_all_claims
from database import delete_claim as database_delete_claim


# ============================================================
# ADD CLAIM
# ============================================================

def add_claim(text, verdict, confidence, message):
    """
    Save a claim using the SQLite database.
    """

    return database_add_claim(
        text=text,
        verdict=verdict,
        confidence=confidence,
        message=message
    )


# ============================================================
# GET ALL CLAIMS
# ============================================================

def get_all_claims():
    """
    Get all claims from the SQLite database.
    """

    return database_get_all_claims()


# ============================================================
# DELETE CLAIM
# ============================================================

def delete_claim(claim_id):
    """
    Delete a claim using its ID.
    """

    return database_delete_claim(claim_id)


# ============================================================
# GET CLAIM STATISTICS
# ============================================================

def get_claim_statistics():
    """
    Calculate statistics for the Admin Dashboard.
    """

    claims = database_get_all_claims()

    total = len(claims)

    fake = sum(
        1
        for claim in claims
        if str(
            claim.get("verdict", "")
        ).lower() == "fake"
    )

    real = sum(
        1
        for claim in claims
        if str(
            claim.get("verdict", "")
        ).lower() == "real"
    )

    uncertain = sum(
        1
        for claim in claims
        if str(
            claim.get("verdict", "")
        ).lower() == "uncertain"
    )

    return {
        "total": total,
        "fake": fake,
        "real": real,
        "uncertain": uncertain
    }