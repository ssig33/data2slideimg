FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements
COPY pyproject.toml ./
COPY uv.lock ./

# Install Python dependencies
RUN pip install --no-cache-dir fastapi pillow matplotlib uvicorn click

# Copy application code
COPY src/ ./src/

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose port
EXPOSE $PORT

# Run the application
CMD uvicorn src.main:app --host 0.0.0.0 --port $PORT