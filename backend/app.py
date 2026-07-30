from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"message": "FakeRadar Backend Running"}

@app.route("/test")
def test():
    return {"status": "working"}

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    article = data.get("text", "")

    return jsonify({
        "verdict": "Unverified",
        "confidence": 75,
        "message": f"Analysis completed for: {article[:50]}"
    })

if __name__ == "__main__":
    app.run(debug=True)