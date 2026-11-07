import json
import os
from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "model.joblib"
METADATA_PATH = PROJECT_ROOT / "artifacts" / "metadata.json"

if not METADATA_PATH.exists():
    METADATA_PATH = PROJECT_ROOT / "metadata.json"

with open(METADATA_PATH, "r") as f:
    model_metadata = json.load(f)

# Features expected by the model
FEATURES = [
    "tenure_months",
    "monthly_charges",
    "support_calls",
    "contract",
    "internet_service",
]


# Load trained model
model = joblib.load(MODEL_PATH)


# API input validation
class CustomerInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenure_months: int = Field(ge=0)
    monthly_charges: float = Field(ge=0)
    support_calls: int = Field(ge=0)

    contract: Literal[
        "month-to-month",
        "one-year",
        "two-year",
    ]

    internet_service: Literal[
        "fiber",
        "dsl",
        "none",
    ]


# API response validation
class PredictionResponse(BaseModel):
    churn_probability: float


# Create FastAPI application
app = FastAPI(
    title="AI381 Customer Churn API",
    description="Predict customer churn probability.",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "model_version": model_metadata["model_version"],
        "model": model_metadata["model"],
        "mlflow_run_id": model_metadata["mlflow_run_id"],
        "git_sha": os.getenv("GIT_SHA", "unknown"),
        "image_tag": os.getenv("IMAGE_TAG", "unknown"),

    }


@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerInput):

    # Convert validated input into DataFrame
    customer_data = pd.DataFrame(
        [customer.model_dump()],
        columns=FEATURES,
    )

    # Predict churn probability
    probability = float(
        model.predict_proba(customer_data)[0, 1]
    )

    return {
        "churn_probability": round(probability, 3)
    }

