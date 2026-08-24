from flask import Flask, request, jsonify
from flask_cors import CORS

from tracker import add_claim, get_all_claims


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "FakeRadar Backend Running"
    })


@app.route("/test")
def test():
    return jsonify({
        "message": "Working"
    })


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    article = data.get("text", "").strip()

    if not article:
        return jsonify({
            "error": "Please provide news text"
        }), 400

    # Temporary analysis
    # Later this will be replaced by our trained ML model
    verdict = "Unverified"
    confidence = 75
    message = f"Analysis completed for: {article[:50]}"

    # Temporary keyword detection
    # Later this can be replaced with ML/NLP-based detection
    suspicious_keywords = [
        "breaking",
        "shocking",
        "urgent",
        "secret",
        "miracle",
        "fake",
        "scandal"
    ]

    article_lower = article.lower()

    keywords_detected = [
        keyword
        for keyword in suspicious_keywords
        if keyword in article_lower
    ]

    # Save the analysis to the Claim Evaluation Tracker
    claim = add_claim(
        text=article,
        verdict=verdict,
        confidence=confidence,
        message=message
    )

    return jsonify({
        "verdict": verdict,
        "confidence": confidence,
        "message": message,
        "keywords_detected": keywords_detected,
        "claim": claim
    })


@app.route("/claims", methods=["GET"])
def get_claims():
    claims = get_all_claims()

    return jsonify({
        "claims": claims
    })


if __name__ == "__main__":
    app.run(debug=True)