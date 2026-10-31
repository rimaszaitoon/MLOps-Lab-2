from fastapi.testclient import TestClient

from src.app.main import app, model

client = TestClient(app)


# Test 1: API contract
def test_api_contract():
    # Check health endpoint
    health_response = client.get("/health")

    assert health_response.status_code == 200
    assert health_response.json()["status"] == "ok"
    assert health_response.json()["model_loaded"] is True

    # Check prediction endpoint
    prediction_response = client.post(
        "/predict",
        json={
            "tenure_months": 9,
            "monthly_charges": 89.9,
            "contract": "month-to-month",
            "internet_service": "fiber",
            "support_calls": 7,
        },
    )

    assert prediction_response.status_code == 200
    assert "churn_probability" in prediction_response.json()


# Test 2: Model loading
def test_model_loads():
    assert model is not None
    assert hasattr(model, "predict_proba")


# Test 3: Input schema validation
def test_invalid_input():
    response = client.post(
        "/predict",
        json={
            "tenure_months": -5,
            "monthly_charges": 89.9,
            "contract": "month-to-month",
            "internet_service": "fiber",
            "support_calls": 7,
        },
    )

    assert response.status_code == 422


# Test 4: Edge case
def test_zero_values():
    response = client.post(
        "/predict",
        json={
            "tenure_months": 0,
            "monthly_charges": 0,
            "contract": "two-year",
            "internet_service": "none",
            "support_calls": 0,
        },
    )

    assert response.status_code == 200

    probability = response.json()["churn_probability"]

    assert 0 <= probability <= 1


# Test 5: Deterministic prediction
def test_deterministic_prediction():
    customer = {
        "tenure_months": 9,
        "monthly_charges": 89.9,
        "contract": "month-to-month",
        "internet_service": "fiber",
        "support_calls": 7,
    }

    first_response = client.post("/predict", json=customer)
    second_response = client.post("/predict", json=customer)

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    assert (
        first_response.json()["churn_probability"]
        == second_response.json()["churn_probability"]
    )
