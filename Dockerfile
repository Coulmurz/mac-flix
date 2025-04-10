# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*

# Copy pinned requirements
COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt -r requirements-dev.txt

# Copy app code, planning docs, and tests
COPY app/ app/
COPY planning/ planning/
COPY tests/ tests/
COPY README.md .

# Expose FastAPI and Streamlit ports
EXPOSE 8000 8501

# Default command: run both FastAPI and Streamlit
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run app/frontend.py --server.port 8501 --server.address 0.0.0.0
