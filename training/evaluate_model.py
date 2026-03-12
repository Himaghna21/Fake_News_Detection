"""
Fake News Detection - Model Evaluation Script
===============================================
Loads the saved model and vectorizer, evaluates on a fresh test split.
"""

import os
import sys

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

# Reuse preprocessing from train_model
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from train_model import clean_data, load_data, preprocess_column

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")


def main():
    # Load artifacts
    model_path = os.path.join(MODEL_DIR, "model.pkl")
    vec_path = os.path.join(MODEL_DIR, "vectorizer.pkl")
    meta_path = os.path.join(MODEL_DIR, "metadata.pkl")

    if not os.path.exists(model_path):
        print("ERROR: model.pkl not found. Run train_model.py first.")
        sys.exit(1)

    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    metadata = joblib.load(meta_path)

    print(f"Loaded model: {metadata['model_name']}")
    print(f"\nTraining results:")
    for name, metrics in metadata["results"].items():
        print(f"  {name}: Acc={metrics['accuracy']:.4f}, F1={metrics['f1']:.4f}")

    # Re-evaluate on data
    df = load_data()
    df = clean_data(df)
    df = preprocess_column(df)

    _, X_test, _, y_test = train_test_split(
        df["clean_text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )

    X_test_tfidf = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_tfidf)

    print("\n" + "=" * 50)
    print("  EVALUATION REPORT")
    print("=" * 50)
    print(f"  Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"  Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"  Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"  F1 Score:  {f1_score(y_test, y_pred):.4f}")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred, target_names=['FAKE', 'REAL'])}")
    print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")


if __name__ == "__main__":
    main()
