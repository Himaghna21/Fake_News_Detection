"""
Fake News Detection — FastAPI Backend
======================================
REST API for classifying news articles as FAKE or REAL.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .predict import predict

app = FastAPI(
    title="Fake News Detection API",
    description="ML-powered API to classify news articles as FAKE or REAL",
    version="1.0.0",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=10, description="News article text to classify")


class PredictResponse(BaseModel):
    prediction: str
    confidence: float


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
async def predict_endpoint(request: PredictRequest):
    """Classify a news article as FAKE or REAL."""
    try:
        result = predict(request.text)
        return PredictResponse(**result)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
