from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "churn_v1.csv"
MODEL_PATH = PROJECT_ROOT / "model.joblib"


# Features used by the model
NUMERIC_FEATURES = [
    "tenure_months",
    "monthly_charges",
    "support_calls",
]

CATEGORICAL_FEATURES = [
    "contract",
    "internet_service",
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "churn"


def train_model():
    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Validate required columns
    required_columns = FEATURES + [TARGET]
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Dataset is missing columns: {sorted(missing_columns)}"
        )

    # Check for missing values
    if df[required_columns].isnull().any().any():
        raise ValueError("Dataset contains missing values.")

    # Separate features and target
    X = df[FEATURES]
    y = df[TARGET]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # Preprocessing
    preprocessing = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    # Complete machine learning pipeline
    model = Pipeline(
        steps=[
            ("prep", preprocessing),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )

    # Train model
    model.fit(X_train, y_train)

    # Evaluate model
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = probabilities > 0.5

    f1 = f1_score(y_test, predictions)
    auc = roc_auc_score(y_test, probabilities)

    # Save trained model
    joblib.dump(model, MODEL_PATH)

    print("Training completed successfully!")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"F1 Score: {f1:.3f}")
    print(f"ROC AUC: {auc:.3f}")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
