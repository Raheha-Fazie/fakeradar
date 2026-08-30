import pandas as pd
import joblib

# Load model
model = joblib.load("fake_news_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Load REAL dataset
true = pd.read_csv("dataset/True.csv")

# Take one real article directly from the dataset
article = true.iloc[0]["title"] + " " + true.iloc[0]["text"]

print("\n==============================")
print("ARTICLE FROM True.csv")
print("==============================")
print(article[:1000])

# Convert to TF-IDF
article_tfidf = vectorizer.transform([article])

# Predict
prediction = model.predict(article_tfidf)[0]
probabilities = model.predict_proba(article_tfidf)[0]

print("\n==============================")
print("MODEL PREDICTION")
print("==============================")

print("Prediction:", prediction)
print("Fake probability:", round(probabilities[0] * 100, 2), "%")
print("Real probability:", round(probabilities[1] * 100, 2), "%")

if prediction == 0:
    print("VERDICT: Fake")
else:
    print("VERDICT: Real")

print("==============================")