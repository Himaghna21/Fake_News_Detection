"""
Fake News Detection - Model Training Script
============================================
Trains and compares multiple ML models on the Fake and Real News Dataset.
Saves the best model and TF-IDF vectorizer for production use.
"""

import os
import re
import string
import sys
import time

import joblib
import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# ------------------------------------------------------------------ #
# NLTK DATA
# ------------------------------------------------------------------ #
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

STOP_WORDS = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)


# ------------------------------------------------------------------ #
# 1. DATA LOADING
# ------------------------------------------------------------------ #
def load_data():
    """Load and merge Fake.csv & True.csv, adding labels."""
    fake_path = os.path.join(DATA_DIR, "Fake.csv")
    true_path = os.path.join(DATA_DIR, "True.csv")

    if not os.path.exists(fake_path) or not os.path.exists(true_path):
        print("ERROR: Fake.csv and/or True.csv not found in data/ directory.")
        print(f"Expected location: {DATA_DIR}")
        print(
            "Download from: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset"
        )
        sys.exit(1)

    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)

    fake_df["label"] = 0  # Fake
    true_df["label"] = 1  # Real

    df = pd.concat([fake_df, true_df], ignore_index=True)
    print(f"[INFO] Loaded {len(fake_df)} fake + {len(true_df)} real = {len(df)} total articles")
    return df


# ------------------------------------------------------------------ #
# 2. DATA CLEANING
# ------------------------------------------------------------------ #
def clean_data(df):
    """Drop nulls, duplicates, and combine title + text."""
    initial = len(df)
    df = df.dropna(subset=["title", "text"])
    df = df.drop_duplicates(subset=["title", "text"])
    print(f"[INFO] Cleaned: {initial} -> {len(df)} articles (removed {initial - len(df)})")

    df["content"] = df["title"] + " " + df["text"]
    return df


# ------------------------------------------------------------------ #
# 3. TEXT PREPROCESSING
# ------------------------------------------------------------------ #
def preprocess_text(text):
    """Lowercase, remove punctuation/stopwords, lemmatize."""
    text = text.lower()
    text = re.sub(r"^.*?\(reuters\)\s*-\s*", "", text)
    text = text.replace("reuters", "")
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"<.*?>+", "", text)
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\w*\d\w*", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))

    tokens = text.split()
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in STOP_WORDS]
    return " ".join(tokens)


def preprocess_column(df):
    """Apply preprocessing to the content column."""
    print("[INFO] Preprocessing text (this may take a minute)...")
    t0 = time.time()
    df["clean_text"] = df["content"].apply(preprocess_text)
    print(f"[INFO] Preprocessing complete in {time.time() - t0:.1f}s")
    return df


# ------------------------------------------------------------------ #
# 4. FEATURE ENGINEERING
# ------------------------------------------------------------------ #
def build_tfidf(X_train, X_test, max_features=50_000):
    """Fit TF-IDF vectorizer on training data and transform both splits."""
    vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    print(f"[INFO] TF-IDF: vocabulary size = {len(vectorizer.vocabulary_)}")
    return vectorizer, X_train_tfidf, X_test_tfidf


# ------------------------------------------------------------------ #
# 5. MODEL TRAINING & 6. EVALUATION
# ------------------------------------------------------------------ #
def evaluate_model(name, model, X_test, y_test):
    """Compute and print evaluation metrics."""
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print(f"\n{'='*50}")
    print(f"  {name}")
    print(f"{'='*50}")
    print(f"  Accuracy:  {acc:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall:    {rec:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    print(f"  Confusion Matrix:\n{cm}")
    print(f"{'='*50}")
    return acc, {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1}


def train_models(X_train, y_train, X_test, y_test):
    """Train multiple models, evaluate, and return the best one."""
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, C=1.0, random_state=42),
        "PassiveAggressiveClassifier": PassiveAggressiveClassifier(max_iter=1000, random_state=42),
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.1),
    }

    results = {}
    best_acc = 0
    best_model = None
    best_name = ""

    for name, model in models.items():
        print(f"\n[INFO] Training {name}...")
        model.fit(X_train, y_train)
        acc, metrics = evaluate_model(name, model, X_test, y_test)
        results[name] = metrics

        if acc > best_acc:
            best_acc = acc
            best_model = model
            best_name = name

    print(f"\n* Best model: {best_name} with accuracy {best_acc:.4f}")
    return best_model, best_name, results


# ------------------------------------------------------------------ #
# 7. MODEL PERSISTENCE
# ------------------------------------------------------------------ #
def save_artifacts(model, vectorizer, model_name, results):
    """Save model, vectorizer, and metadata."""
    model_path = os.path.join(MODEL_DIR, "model.pkl")
    vec_path = os.path.join(MODEL_DIR, "vectorizer.pkl")
    meta_path = os.path.join(MODEL_DIR, "metadata.pkl")

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)
    joblib.dump({"model_name": model_name, "results": results}, meta_path)

    print(f"\n[INFO] Saved model      -> {model_path}")
    print(f"[INFO] Saved vectorizer -> {vec_path}")
    print(f"[INFO] Saved metadata   -> {meta_path}")


# ------------------------------------------------------------------ #
# MAIN
# ------------------------------------------------------------------ #
def main():
    print("=" * 60)
    print("  FAKE NEWS DETECTION — MODEL TRAINING")
    print("=" * 60)

    # 1. Load
    df = load_data()

    # 2. Clean
    df = clean_data(df)

    # 3. Preprocess
    df = preprocess_column(df)

    # 4. Split
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )
    print(f"[INFO] Train: {len(X_train)} | Test: {len(X_test)}")

    # 5. TF-IDF
    vectorizer, X_train_tfidf, X_test_tfidf = build_tfidf(X_train, X_test)

    # 6. Train & Evaluate
    best_model, best_name, results = train_models(
        X_train_tfidf, y_train, X_test_tfidf, y_test
    )

    # 7. Save
    save_artifacts(best_model, vectorizer, best_name, results)

    print("\n✅ Training complete!")


if __name__ == "__main__":
    main()
