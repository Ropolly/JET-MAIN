# Multi-stage Dockerfile for JET ICU Operations - Frontend + Backend
FROM node:18-alpine as frontend-builder

# Build arguments for frontend
ARG VITE_APP_API_URL=/api

# Install build dependencies
RUN apk add --no-cache python3 make g++

# Set work directory for frontend
WORKDIR /app/frontend

# Copy frontend package files
COPY Operations/frontend/package*.json ./

# Install frontend dependencies (including dev dependencies for build)
RUN npm ci

# Copy frontend source
COPY Operations/frontend/ ./

# Set build environment variables
ENV VITE_APP_API_URL=$VITE_APP_API_URL

# Build the Vue application
RUN npm run build

# Python backend builder stage
FROM python:3.10-slim as backend-builder

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy backend requirements and build wheels
COPY Operations/backend/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final production stage
FROM python:3.10-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    netcat-traditional \
    curl \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Create application user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set work directory
WORKDIR /app

# Copy Python wheels and install
COPY --from=backend-builder /app/wheels /wheels
COPY --from=backend-builder /app/requirements.txt .
RUN pip install --no-cache /wheels/* \
    && pip install gunicorn==21.2.0 \
    && rm -rf /wheels

# Copy backend application
COPY --chown=appuser:appuser Operations/backend/ ./backend/

# Copy built frontend from frontend-builder
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# Copy nginx configuration
COPY Operations/frontend/nginx.conf /etc/nginx/sites-available/default
RUN rm -f /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Create necessary directories
RUN mkdir -p /app/backend/static /app/backend/media /app/backend/documents /app/backend/logs \
    && mkdir -p /var/log/supervisor \
    && chown -R appuser:appuser /app/backend/static /app/backend/media /app/backend/documents /app/backend/logs \
    && chown -R appuser:appuser /usr/share/nginx/html

# Copy entrypoint and supervisor configuration
COPY --chown=appuser:appuser Operations/backend/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy supervisor and startup configurations
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY start-django.sh /app/start-django.sh
RUN chmod +x /app/start-django.sh

# Update nginx configuration to proxy to localhost instead of backend service
RUN sed -i 's/proxy_pass http:\/\/backend:8000;/proxy_pass http:\/\/127.0.0.1:8000;/' /etc/nginx/sites-available/default

# Expose ports
EXPOSE 80 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=backend.settings

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost/ && curl -f http://localhost/api/health/ || exit 1

# Start supervisor to manage both services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
