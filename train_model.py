import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# =========================================================
# 1. FILE PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FAKE_FILE = os.path.join(BASE_DIR, "dataset", "Fake.csv")
TRUE_FILE = os.path.join(BASE_DIR, "dataset", "True.csv")

MODEL_FILE = os.path.join(BASE_DIR, "fake_news_model.pkl")
VECTORIZER_FILE = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")


# =========================================================
# 2. CHECK DATASET FILES
# =========================================================

if not os.path.exists(FAKE_FILE):
    print("ERROR: Fake.csv was not found.")
    print("Expected location:", FAKE_FILE)
    exit()

if not os.path.exists(TRUE_FILE):
    print("ERROR: True.csv was not found.")
    print("Expected location:", TRUE_FILE)
    exit()


# =========================================================
# 3. LOAD DATASET
# =========================================================

print("Loading datasets...")

fake = pd.read_csv(FAKE_FILE)
true = pd.read_csv(TRUE_FILE)

print("Fake articles:", len(fake))
print("Real articles:", len(true))


# =========================================================
# 4. ADD LABELS
# =========================================================

fake["label"] = 0
true["label"] = 1


# =========================================================
# 5. COMBINE DATASETS
# =========================================================

data = pd.concat([fake, true], ignore_index=True)

print("Total articles:", len(data))


# =========================================================
# 6. CLEAN TEXT
# =========================================================

data["title"] = data["title"].fillna("")
data["text"] = data["text"].fillna("")

data["content"] = (
    data["title"].astype(str)
    + " "
    + data["text"].astype(str)
)

# Remove empty articles
data = data[data["content"].str.strip() != ""]


# =========================================================
# 7. INPUT AND OUTPUT
# =========================================================

X = data["content"]
y = data["label"]


# =========================================================
# 8. SPLIT DATA
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print()
print("Training articles:", len(X_train))
print("Testing articles:", len(X_test))


# =========================================================
# 9. TF-IDF
# =========================================================

print()
print("Creating TF-IDF features...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_df=0.7,
    max_features=50000,
    ngram_range=(1, 2)
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("TF-IDF training shape:", X_train_tfidf.shape)


# =========================================================
# 10. TRAIN LOGISTIC REGRESSION
# =========================================================

print()
print("Training Logistic Regression model...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train_tfidf, y_train)


# =========================================================
# 11. TEST MODEL
# =========================================================

print()
print("Testing model...")

predictions = model.predict(X_test_tfidf)


# =========================================================
# 12. ACCURACY
# =========================================================

accuracy = accuracy_score(y_test, predictions)

print()
print("==========================================")
print("MODEL PERFORMANCE")
print("==========================================")

print(f"Accuracy: {accuracy * 100:.2f}%")


# =========================================================
# 13. CLASSIFICATION REPORT
# =========================================================

print()
print("Classification Report:")
print()

print(
    classification_report(
        y_test,
        predictions,
        target_names=["Fake", "Real"]
    )
)


# =========================================================
# 14. CONFUSION MATRIX
# =========================================================

matrix = confusion_matrix(y_test, predictions)

print()
print("Confusion Matrix:")
print(matrix)

print()
print("Format:")
print("[[Fake predicted Fake, Fake predicted Real]")
print(" [Real predicted Fake, Real predicted Real]]")


# =========================================================
# 15. SAVE MODEL
# =========================================================

joblib.dump(model, MODEL_FILE)
joblib.dump(vectorizer, VECTORIZER_FILE)

print()
print("==========================================")
print("MODEL SAVED SUCCESSFULLY")
print("==========================================")

print("Model:", MODEL_FILE)
print("Vectorizer:", VECTORIZER_FILE)

print()
print("Training completed successfully!")