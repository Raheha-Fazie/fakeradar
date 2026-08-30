import joblib

# Load trained model
model = joblib.load("fake_news_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

print("Model loaded successfully.")

# Test article
article = """
NASA scientists have reported that parts of Earth's upper atmosphere
are gradually cooling and contracting. Researchers used data from
three NASA satellites to study long-term changes in the mesosphere,
a layer of the atmosphere located roughly 30 to 50 miles above Earth's
surface. The scientists found that the mesosphere is cooling and
contracting, a trend that has been predicted in connection with
increasing human-made greenhouse gas emissions.
"""

# Convert text to TF-IDF
article_tfidf = vectorizer.transform([article])

# Prediction
prediction = model.predict(article_tfidf)[0]

# Probability
probabilities = model.predict_proba(article_tfidf)[0]

print()
print("==============================")
print("MODEL TEST")
print("==============================")

print("Prediction:", prediction)

print("Fake probability:", round(probabilities[0] * 100, 2), "%")
print("Real probability:", round(probabilities[1] * 100, 2), "%")

if prediction == 0:
    print("VERDICT: Fake")
else:
    print("VERDICT: Real")