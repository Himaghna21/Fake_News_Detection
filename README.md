# 🛡️ Fake News Detector

An AI-powered web application that classifies news articles as **FAKE** or **REAL** using Natural Language Processing and Machine Learning. 

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![Tailwind](https://img.shields.io/badge/TailwindCSS-3-38B2AC?logo=tailwind-css)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?logo=scikit-learn)

---

## 📖 Overview

This project trains a supervised machine learning model on the [Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset) from Kaggle, exposes predictions through a REST API, and provides a modern, premium web interface for real-time news verification.

### Key Features

- **ML-Powered Classification** — Logistic Regression, Passive Aggressive, and Naive Bayes models compared and evaluated.
- **TF-IDF Vectorization** — Extracts meaning using n-grams (up to bigrams) and a 50k vocabulary limit.
- **FastAPI Backend** — High-performance REST API for asynchronous, real-time predictions.
- **Premium User Interface** — A highly polished, Elvaris-inspired UI featuring deep blacks, neon purple/blue glow effects, and a custom **Light/Dark Mode toggle**.
- **Confidence Scoring** — Visual progress bars indicating the AI's certainty for every prediction.

---

## 🏗️ Architecture

```
fake-news-detector/
├── data/                   # Dataset files (Fake.csv, True.csv) required for training
├── training/
│   ├── train_model.py      # Full ML pipeline: load → clean → train → evaluate → save
│   └── evaluate_model.py   # Load saved artifacts to print a metrics report
├── model/                  # Generated model artifacts (model.pkl, vectorizer.pkl)
├── backend/
│   ├── main.py             # FastAPI entry point with CORS and /predict endpoint
│   ├── preprocess.py       # Text cleaning logic matching the training phase
│   └── predict.py          # Model loading, inference, and confidence calculation
├── frontend/
│   ├── src/
│   │   ├── components/     # UI Components: Hero, NewsInput, ResultCard, ThemeToggle
│   │   ├── App.jsx         # Main React application layout
│   │   └── index.css       # Premium CSS design system (neon glows, styling)
│   └── tailwind.config.js
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 📊 Dataset & ML Pipeline

The project relies on the **Fake and Real News Dataset** from Kaggle, consisting of over 44,000 articles.

### Pipeline Steps:
1. **Data Loading & Cleaning** — Merge CSVs, assign labels (`1` for Real, `0` for Fake), drop duplicates/nulls, and combine title + text.
2. **Preprocessing** — Lowercasing, removal of punctuation/URLs/stopwords, and semantic lemmatization using NLTK.
3. **Feature Engineering** — Text mapped to numerical features via `TfidfVectorizer` (ngram_range=(1,2)).
4. **Training & Evaluation** — Models trained, compared via metrics (Accuracy, Precision, Recall, F1), and the best performer saved via `joblib`.

---

## 🚀 Setup & Execution Instructions

### Prerequisites
- Python 3.8+
- Node.js 18+ and npm

### 1. Clone & Install Dependencies

**Backend / ML:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 2. Download the Dataset
Download the dataset from [Kaggle](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset). Extract and place `Fake.csv` and `True.csv` inside the `data/` folder:
```
fake-news-detector/
└── data/
    ├── Fake.csv
    └── True.csv
```

### 3. Train the Model
*This must be run first to generate `model.pkl` and `vectorizer.pkl`.*
```bash
python training/train_model.py
```

### 4. Start the Backend API
Start the FastAPI server on port 8000:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
*API Documentation available at: http://localhost:8000/docs*

### 5. Start the Frontend UI
Start the React development server:
```bash
cd frontend
npm run dev
```
*Open http://localhost:5173 in your browser to use the application.*

---

## 📡 API Reference

### `POST /predict`
Submit an article for classification.
```json
// Request Body
{
  "text": "BREAKING: Scientists have discovered a new element..."
}

// Response
{
  "prediction": "FAKE",
  "confidence": 0.8501
}
```

---

## 📄 License
MIT License. Built for educational and portfolio purposes.
