import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ==================================================
# 1. LOAD DATASET
# ==================================================

fake = pd.read_csv("dataset/Fake.csv")
true = pd.read_csv("dataset/True.csv")

print("Fake articles:", len(fake))
print("Real articles:", len(true))


# ==================================================
# 2. ADD LABELS
# ==================================================

fake["label"] = 0
true["label"] = 1


# ==================================================
# 3. COMBINE DATA
# ==================================================

data = pd.concat([fake, true], ignore_index=True)

print("Total articles:", len(data))


# ==================================================
# 4. CLEAN DATA
# ==================================================

data["text"] = data["text"].fillna("")
data["title"] = data["title"].fillna("")

data["content"] = data["title"] + " " + data["text"]

# Remove empty articles
data = data[data["content"].str.strip() != ""]


# ==================================================
# 5. INPUT AND LABEL
# ==================================================

X = data["content"]
y = data["label"]


# ==================================================
# 6. TRAIN / TEST SPLIT
# ==================================================

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


# ==================================================
# 7. TF-IDF
# ==================================================

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

print("TF-IDF shape:", X_train_tfidf.shape)


# ==================================================
# 8. TRAIN MODEL
# ==================================================

print()
print("Training Logistic Regression...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train_tfidf, y_train)


# ==================================================
# 9. PREDICTIONS
# ==================================================

predictions = model.predict(X_test_tfidf)


# ==================================================
# 10. ACCURACY
# ==================================================

accuracy = accuracy_score(y_test, predictions)

print()
print("==========================================")
print("MODEL PERFORMANCE")
print("==========================================")

print(f"Accuracy: {accuracy * 100:.2f}%")


# ==================================================
# 11. CLASSIFICATION REPORT
# ==================================================

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


# ==================================================
# 12. CONFUSION MATRIX
# ==================================================

matrix = confusion_matrix(y_test, predictions)

print()
print("Confusion Matrix:")
print()

print(matrix)

print()
print("Matrix format:")
print("[[Fake predicted Fake, Fake predicted Real]")
print(" [Real predicted Fake, Real predicted Real]]")


# ==================================================
# 13. SAVE MODEL
# ==================================================

joblib.dump(model, "fake_news_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print()
print("==========================================")
print("MODEL SAVED SUCCESSFULLY")
print("==========================================")

print("fake_news_model.pkl")
print("tfidf_vectorizer.pkl")