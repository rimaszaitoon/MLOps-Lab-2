# Stage 1: Build dependencies
FROM python:3.14.10-slim-trixie AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt \
    && pip install --no-cache-dir --prefix=/install --upgrade \
    "msgpack==1.2.3" \
    "setuptools==84.1.0" \
    "urllib3==2.8.0"


# Stage 2: Runtime image
FROM python:3.14.10-slim-trixie AS runtime

WORKDIR /app
# Image traceability

ARG GIT_SHA=unknown
ARG IMAGE_TAG=unknown

ENV GIT_SHA=${GIT_SHA}
ENV IMAGE_TAG=${IMAGE_TAG}

# Update Debian security packages
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Remove pip and its bundled vulnerable dependencies
RUN rm -rf \
    /usr/local/lib/python3.14/site-packages/pip \
    /usr/local/lib/python3.14/site-packages/pip-*.dist-info \
    /usr/local/lib/python3.14/site-packages/setuptools \
    /usr/local/lib/python3.14/site-packages/setuptools-*.dist-info \
    /usr/local/lib/python3.14/site-packages/msgpack \
    /usr/local/lib/python3.14/site-packages/msgpack-*.dist-info \
    /usr/local/lib/python3.14/site-packages/urllib3 \
    /usr/local/lib/python3.14/site-packages/urllib3-*.dist-info

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Create a non-root user
RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid appuser --create-home appuser

# Copy application and trained model
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser artifacts/model.joblib ./model.joblib
COPY --chown=appuser:appuser artifacts/metadata.json ./metadata.json


# Run as non-root user
USER appuser

# Container health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)" || exit 1

# Start FastAPI
EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
