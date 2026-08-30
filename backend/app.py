from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

from database import initialize_database

from tracker import (
    add_claim,
    get_all_claims,
    delete_claim,
    get_claim_statistics
)


# ============================================================
# CREATE FLASK APP
# ============================================================

app = Flask(__name__)

CORS(app)


# ============================================================
# DIRECTORY PATHS
# ============================================================

# Location of backend folder
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# Main FakeRadar project folder
PROJECT_DIR = os.path.dirname(
    BASE_DIR
)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()


# ============================================================
# LOAD MACHINE LEARNING MODEL
# ============================================================

# Model files are located in:
#
# FakeRadar/
#     ml_model/
#         fake_news_model.pkl
#         tfidf_vectorizer.pkl

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "ml_model",
    "fake_news_model.pkl"
)

VECTORIZER_PATH = os.path.join(
    PROJECT_DIR,
    "ml_model",
    "tfidf_vectorizer.pkl"
)


# Default values
model = None
vectorizer = None


try:

    model = joblib.load(
        MODEL_PATH
    )

    vectorizer = joblib.load(
        VECTORIZER_PATH
    )

    print(
        "=========================================="
    )

    print(
        "Machine learning model loaded successfully."
    )

    print(
        "Model:",
        MODEL_PATH
    )

    print(
        "Vectorizer:",
        VECTORIZER_PATH
    )

    print(
        "=========================================="
    )


except Exception as error:

    print(
        "=========================================="
    )

    print(
        "ERROR LOADING ML MODEL"
    )

    print(
        error
    )

    print(
        "Model path:",
        MODEL_PATH
    )

    print(
        "Vectorizer path:",
        VECTORIZER_PATH
    )

    print(
        "=========================================="
    )


# ============================================================
# HOME
# ============================================================

@app.route(
    "/",
    methods=["GET"]
)
def home():

    return jsonify({

        "message": "FakeRadar API is running.",

        "model_loaded": (
            model is not None
        ),

        "vectorizer_loaded": (
            vectorizer is not None
        )

    })


# ============================================================
# ANALYZE NEWS
# ============================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze_news():

    try:

        # ----------------------------------------------------
        # CHECK REQUEST DATA
        # ----------------------------------------------------

        data = request.get_json()

        if not data:

            return jsonify({

                "error": "No data received."

            }), 400


        # ----------------------------------------------------
        # GET ARTICLE TEXT
        # ----------------------------------------------------

        text = data.get(
            "text",
            ""
        ).strip()


        # ----------------------------------------------------
        # VALIDATE INPUT
        # ----------------------------------------------------

        if not text:

            return jsonify({

                "error": "Please enter a news article."

            }), 400


        if len(text) < 20:

            return jsonify({

                "error": (
                    "Please enter a longer "
                    "news article."
                )

            }), 400


        # ----------------------------------------------------
        # CHECK ML MODEL
        # ----------------------------------------------------

        if (
            model is None
            or vectorizer is None
        ):

            return jsonify({

                "error": (
                    "Machine learning model "
                    "is not available."
                )

            }), 500


        # ----------------------------------------------------
        # CONVERT TEXT INTO TF-IDF FEATURES
        # ----------------------------------------------------

        text_vector = vectorizer.transform(
            [text]
        )


        # ----------------------------------------------------
        # GET MODEL PREDICTION
        # ----------------------------------------------------

        prediction = model.predict(
            text_vector
        )[0]


        # ----------------------------------------------------
        # GET CONFIDENCE
        # ----------------------------------------------------

        probabilities = model.predict_proba(
            text_vector
        )[0]


        confidence = float(
            max(probabilities) * 100
        )


        # ----------------------------------------------------
        # CONVERT PREDICTION INTO VERDICT
        # ----------------------------------------------------

        prediction_text = str(
            prediction
        ).lower().strip()


        if prediction_text == "fake":

            verdict = "Fake"


        elif prediction_text == "real":

            verdict = "Real"


        else:

            # ------------------------------------------------
            # HANDLE NUMERIC MODEL LABELS
            # ------------------------------------------------

            try:

                numeric_prediction = int(
                    prediction
                )

                if numeric_prediction == 0:

                    verdict = "Fake"

                else:

                    verdict = "Real"


            except (
                ValueError,
                TypeError
            ):

                verdict = str(
                    prediction
                )


        # ----------------------------------------------------
        # UNCERTAIN LOGIC
        # ----------------------------------------------------

        UNCERTAIN_THRESHOLD = 60.0


        if confidence < UNCERTAIN_THRESHOLD:

            verdict = "Uncertain"

            message = (
                "The model is not confident enough "
                "to classify this article as Fake "
                "or Real. "
                f"Confidence: {confidence:.2f}%."
            )


        else:

            message = (
                "The model classified this news "
                f"article as {verdict} with "
                f"{confidence:.2f}% confidence."
            )


        # ----------------------------------------------------
        # SAVE CLAIM TO DATABASE
        # ----------------------------------------------------

        add_claim(

            text=text,

            verdict=verdict,

            confidence=round(
                confidence,
                2
            ),

            message=message

        )


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return jsonify({

            "verdict": verdict,

            "confidence": round(
                confidence,
                2
            ),

            "message": message

        })


    except Exception as error:

        print(
            "Analysis error:",
            error
        )

        return jsonify({

            "error": "Analysis failed.",

            "details": str(error)

        }), 500


# ============================================================
# GET CLAIM HISTORY
# ============================================================

@app.route(
    "/claims",
    methods=["GET"]
)
def claims():

    try:

        claims_data = get_all_claims()

        return jsonify({

            "claims": claims_data

        })


    except Exception as error:

        print(
            "Get claims error:",
            error
        )

        return jsonify({

            "error": (
                "Could not load "
                "claim history."
            ),

            "details": str(error)

        }), 500


# ============================================================
# ADMIN DASHBOARD STATISTICS
# ============================================================

@app.route(
    "/admin/stats",
    methods=["GET"]
)
def admin_stats():

    try:

        statistics = get_claim_statistics()

        return jsonify({

            "statistics": statistics

        })


    except Exception as error:

        print(
            "Admin statistics error:",
            error
        )

        return jsonify({

            "error": (
                "Could not load "
                "admin statistics."
            ),

            "details": str(error)

        }), 500


# ============================================================
# DELETE CLAIM
# ============================================================

@app.route(
    "/claims/<int:claim_id>",
    methods=["DELETE"]
)
def remove_claim(claim_id):

    try:

        deleted = delete_claim(
            claim_id
        )


        if not deleted:

            return jsonify({

                "error": "Claim not found."

            }), 404


        return jsonify({

            "message": (
                "Claim deleted successfully."
            )

        })


    except Exception as error:

        print(
            "Delete claim error:",
            error
        )

        return jsonify({

            "error": (
                "Could not delete claim."
            ),

            "details": str(error)

        }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("")

    print(
        "=========================================="
    )

    print(
        "Starting FakeRadar backend..."
    )

    print(
        "=========================================="
    )

    print(
        "Project:",
        PROJECT_DIR
    )

    print(
        "Database:",
        os.path.join(
            BASE_DIR,
            "fakeradar.db"
        )
    )

    print(
        "Model:",
        MODEL_PATH
    )

    print(
        "Vectorizer:",
        VECTORIZER_PATH
    )

    print(
        "Model loaded:",
        model is not None
    )

    print(
        "Vectorizer loaded:",
        vectorizer is not None
    )

    print(
        "=========================================="
    )

    print("")


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )