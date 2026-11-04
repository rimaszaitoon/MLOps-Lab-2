# MLOps Assignment 2 – Churn Prediction API

[![CI](https://github.com/rimaszaitoon/MLOps-Lab-2/actions/workflows/ci.yml/badge.svg)](https://github.com/rimaszaitoon/MLOps-Lab-2/actions/workflows/ci.yml)

A containerized machine learning API for customer churn prediction, built with FastAPI and Docker, and automatically tested, scanned, and published using GitHub Actions.

## Project Overview

This project packages a Logistic Regression churn prediction model as a REST API.

The application:

* Loads a trained machine learning model.
* Provides a health check endpoint.
* Accepts customer data and returns a churn probability.
* Validates incoming data using Pydantic.
* Runs inside a Docker container as a non-root user.
* Uses automated testing and security scanning through GitHub Actions.

## Model Information

* **Algorithm:** Logistic Regression
* **Training samples:** 960
* **Testing samples:** 240
* **F1 Score:** 0.512
* **ROC AUC:** 0.783

The model uses customer information including tenure, monthly charges, support calls, contract type, and internet service.

## Run with Docker

Pull and run the published image:

```
docker run --rm -p 8000:8000 ghcr.io/rimaszaitoon/mlops-lab-2:60408986aa879c49a35e1ad693e981d1a778c8d1
```


The API will be available at:

* Health check: http://localhost:8000/health
* API documentation: http://localhost:8000/docs

## API Endpoints

### GET /health

Checks whether the API is running and the model is loaded.

Example response:

```
{
  "status": "ok",
  "model_loaded": true
}
```

### POST /predict

Accepts customer information and returns the predicted churn probability.

Example request:

```
{
  "tenure_months": 9,
  "monthly_charges": 89.9,
  "support_calls": 3,
  "contract": "month-to-month",
  "internet_service": "fiber"
}
```

Example response:

```
{
  "churn_probability": 0.954
}
```

## Run Tests Locally

Install development dependencies:

```
pip install -r requirements-dev.txt
```

Run linting:

```
ruff check src/ tests/
```

Run the test suite:

```
python -m pytest tests/ -v
```

The test suite includes API contract, model loading, input validation, edge case, and deterministic prediction tests.

## CI/CD Pipeline

GitHub Actions automates the project workflow:

1. Runs linting and automated tests on pull requests.
2. Builds the Docker image when changes are pushed to the main branch.
3. Scans the image for security vulnerabilities using Trivy.
4. Publishes the image to GitHub Container Registry (GHCR).

## Docker Image

**Image:**

```
ghcr.io/rimaszaitoon/mlops-lab-2
```

**Published tag:**

```
60408986aa879c49a35e1ad693e981d1a778c8d1

```

## Repository

GitHub: https://github.com/rimaszaitoon/MLOps-Lab-2
