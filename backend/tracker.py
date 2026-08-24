import json
import os
from datetime import datetime

CLAIMS_FILE = os.path.join(
    os.path.dirname(__file__),
    "claims.json"
)


def load_claims():
    if not os.path.exists(CLAIMS_FILE):
        return []

    try:
        with open(CLAIMS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_claims(claims):
    with open(CLAIMS_FILE, "w", encoding="utf-8") as file:
        json.dump(claims, file, indent=4)


def add_claim(text, verdict, confidence, message=""):
    claims = load_claims()

    claim = {
        "id": len(claims) + 1,
        "claim": text,
        "verdict": verdict,
        "confidence": confidence,
        "message": message,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    claims.append(claim)
    save_claims(claims)

    return claim


def get_all_claims():
    return load_claims()