# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgomp1 \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

# Train the model before running the application, securely mounting the GCP credentials
RUN --mount=type=secret,id=gcp-credentials,target=/tmp/keys/gcp-key.json \
    export GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/gcp-key.json && \
    python pipeline/training_pipeline.py

# Expose the port
EXPOSE 5000

# Command to run the app
CMD ["python", "application.py"]