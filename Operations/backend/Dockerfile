# Production Dockerfile for Django backend
FROM python:3.10-slim as builder

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.10-slim

# Create non-root user for security
RUN groupadd -r django && useradd -r -g django django

# Install runtime dependencies including postgresql-client for Azure DB
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    postgresql-client \
    netcat-traditional \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy wheels from builder and install
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/* \
    && pip install gunicorn[gevent]==21.2.0 \
    && rm -rf /wheels

# Copy entrypoint script first and set permissions
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy project files
COPY --chown=django:django . .

# Create necessary directories with proper permissions
RUN mkdir -p /app/static /app/media /app/documents /app/logs \
    && chown -R django:django /app

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=backend.settings

# Health check with improved timing
HEALTHCHECK --interval=30s --timeout=10s --start-period=45s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Run entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Optimized Gunicorn command for production
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--worker-class", "gevent", "--worker-connections", "1000", "--timeout", "120", "--max-requests", "1000", "--max-requests-jitter", "100", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info"]
