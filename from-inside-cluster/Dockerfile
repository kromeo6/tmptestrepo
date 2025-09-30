FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY fetch_california_data.py .
COPY feature_store.yaml .

# Create feature_repo directory structure
RUN mkdir -p feature_repo

# Copy feature repository files
COPY feature_repo/ feature_repo/

# Set environment variables for cross-namespace MinIO access
ENV AWS_ACCESS_KEY_ID=minio
ENV AWS_SECRET_ACCESS_KEY=minio123
ENV FEAST_S3_ENDPOINT_URL=http://minio-service.kubeflow.svc.cluster.local:9000

# Default command
CMD ["python", "fetch_california_data.py"] 