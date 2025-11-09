# CloudMind AI Dockerfile
# Multi-stage build for optimized production image

FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install CA certificates for SSL
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/
COPY cloudmind_api.py .
COPY cloudmind_cli.py .
COPY .env.example .

# Set PYTHONPATH
ENV PYTHONPATH=/app/src:$PYTHONPATH
ENV PATH=/root/.local/bin:$PATH

# Create .env from example if it doesn't exist
RUN if [ ! -f .env ]; then cp .env.example .env; fi

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Default command - run API server
CMD ["python", "cloudmind_api.py"]
