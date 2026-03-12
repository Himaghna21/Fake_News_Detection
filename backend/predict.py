"""
Prediction module for the Fake News Detection backend.
Loads model/vectorizer once and provides prediction function.
"""

import os

import joblib
import numpy as np

from .preprocess import preprocess_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")

# Load model artifacts once at module level
_model = None
_vectorizer = None
_metadata = None


def _load_model():
    """Lazy-load model artifacts."""
    global _model, _vectorizer, _metadata

    model_path = os.path.join(MODEL_DIR, "model.pkl")
    vec_path = os.path.join(MODEL_DIR, "vectorizer.pkl")
    meta_path = os.path.join(MODEL_DIR, "metadata.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run training/train_model.py first."
        )

    _model = joblib.load(model_path)
    _vectorizer = joblib.load(vec_path)
    if os.path.exists(meta_path):
        _metadata = joblib.load(meta_path)

    print(f"[INFO] Model loaded: {_metadata.get('model_name', 'unknown') if _metadata else 'unknown'}")


def predict(text: str) -> dict:
    """
    Predict whether the given text is fake or real news.

    Returns:
        dict with 'prediction' (str) and 'confidence' (float)
    """
    global _model, _vectorizer

    if _model is None:
        _load_model()

    # Preprocess
    clean_text = preprocess_text(text)

    # Vectorize
    text_tfidf = _vectorizer.transform([clean_text])

    # Predict
    prediction = _model.predict(text_tfidf)[0]
    label = "REAL" if prediction == 1 else "FAKE"

    # Confidence score
    if hasattr(_model, "predict_proba"):
        proba = _model.predict_proba(text_tfidf)[0]
        confidence = float(np.max(proba))
    elif hasattr(_model, "decision_function"):
        decision = _model.decision_function(text_tfidf)[0]
        # Sigmoid to convert decision function to probability-like score
        confidence = float(1 / (1 + np.exp(-abs(decision))))
    else:
        confidence = 0.5

    return {
        "prediction": label,
        "confidence": round(confidence, 4),
    }
