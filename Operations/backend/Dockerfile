# Production Dockerfile for Django backend
FROM python:3.10-slim as builder

# Set build arguments
ARG PYTHON_VERSION=3.10

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

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    netcat-traditional \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy wheels from builder and install
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/* \
    && pip install gunicorn==21.2.0 \
    && rm -rf /wheels

# Copy project files
COPY --chown=django:django . .

# Create necessary directories
RUN mkdir -p /app/static /app/media /app/documents /app/logs \
    && chown -R django:django /app/static /app/media /app/documents /app/logs

# Copy and set permissions for entrypoint script
COPY --chown=django:django entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=backend.settings.production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Run entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]