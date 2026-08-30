FakeRadar -- AI-Powered Fake News Detection System

FakeRadar is an AI-powered fake news detection system developed to help
users assess whether a news article is likely to be Fake, Real,
or Uncertain.

Features

Enter or paste a news article for analysis

Preprocess news text

Detect potentially fake or real news using a machine-learning model

Generate prediction and confidence/probability information

Display results through a web interface

Store and track analysis information

User authentication support

Dataset-based model training

TF-IDF text vectorization

Separate React frontend and Python backend

Project Structure

FakeRadar/
├── backend/
│   ├── app.py
│   ├── auth.py
│   ├── create_admin.py
│   ├── database.py
│   ├── tracker.py
│   └── claims.json
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── App.css
├── dataset/
│   ├── Fake.csv
│   └── True.csv
├── ml_model/
│   ├── fake_news_model.pkl
│   ├── tfidf_vectorizer.pkl
│   ├── test_model.py
│   ├── test_real_article.py
│   └── train_model.py
├── fake_news_model.pkl
├── tfidf_vectorizer.pkl
├── train_model.py
└── README.md

System Workflow

News Article / Claim
        ↓
Text Preprocessing
        ↓
TF-IDF Vectorization
        ↓
Machine-Learning Model
        ↓
Fake / Real Prediction
        ↓
Confidence / Probability
        ↓
Result Display & Tracking

Technologies

Frontend - React - JavaScript / JSX - CSS

Backend - Python - Python-based backend application - JSON and
database handling

Machine Learning - Python - TF-IDF text vectorization - Trained
classification model - CSV datasets

Database - SQLite/database support

Installation

1. Clone the repository

git clone https://github.com/Raheha-Fazie/fakeradar.git
cd fakeradar

2. Create a Python virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate

Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate

3. Install backend dependencies

If requirements.txt is available:

pip install -r requirements.txt

4. Install frontend dependencies

cd frontend
npm install

Running the Project

Backend

From the backend directory, run the project's backend entry point:

python app.py

Frontend

From the frontend directory:

npm run dev

The terminal will show the local development address.

Machine Learning

The project uses TF-IDF text vectorization and a trained classification
model. Training and testing scripts are included in the ml_model
directory and the project root.

Training data:

dataset/Fake.csv
dataset/True.csv

Model files:

fake_news_model.pkl
tfidf_vectorizer.pkl

The general pipeline is:

Load the news dataset.

Preprocess the text.

Convert text into TF-IDF features.

Train the classification model.

Save the trained model and vectorizer.

Use them to classify new articles.

Database and Authentication

Database functionality is implemented through backend/database.py.

Authentication functionality is implemented through backend/auth.py,
with user/admin setup support in backend/create_admin.py.

Analysis tracking is handled through backend/tracker.py.

Testing

Testing covers the major components of the system, including:

News article input

Text preprocessing

ML prediction

Fake/Real classification

Confidence/probability output

Frontend/backend communication

Database functionality

Authentication

Analysis tracking

ML testing scripts include:

ml_model/test_model.py
ml_model/test_real_article.py

Important Note

FakeRadar provides an AI-assisted assessment and should not be
treated as definitive proof that information is true or false. Important
claims should be verified using reliable sources and independent
fact-checking.

GitHub Repository

https://github.com/Raheha-Fazie/fakeradar

Future Improvements

Improve model accuracy using larger and more diverse datasets

Add additional ML/deep-learning models

Improve text preprocessing

Add explainable AI

Add external fact-checking/source verification

Improve accessibility and user experience

Deploy the application to the cloud

Expand analysis history and reporting

Academic Project

Project: FakeRadar -- AI-Powered Fake News Detection System

This project demonstrates the integration of web development, machine
learning, natural language/text processing, database management,
authentication, analysis tracking, and software t
