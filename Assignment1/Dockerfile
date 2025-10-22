# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY assignment_1_3.py .
COPY assignment_2_2.py .
COPY nobel_prize_service_pb2.py .
COPY nobel_prize_service_pb2_grpc.py .

# Expose the gRPC port
EXPOSE 50051

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the server
CMD ["python", "assignment_2_2.py"]