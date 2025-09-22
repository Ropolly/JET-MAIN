#!/bin/sh
set -e

# Replace environment variables in nginx config files
# Default values if not set
DOMAIN_NAME=${DOMAIN_NAME:-localhost}
BACKEND_HOST=${BACKEND_HOST:-backend}
BACKEND_PORT=${BACKEND_PORT:-8000}
FRONTEND_HOST=${FRONTEND_HOST:-frontend}
FRONTEND_PORT=${FRONTEND_PORT:-80}

echo "Configuring nginx with:"
echo "  DOMAIN_NAME: ${DOMAIN_NAME}"
echo "  BACKEND: ${BACKEND_HOST}:${BACKEND_PORT}"
echo "  FRONTEND: ${FRONTEND_HOST}:${FRONTEND_PORT}"

# Create config from template
for template in /etc/nginx/conf.d/*.template; do
    if [ -f "$template" ]; then
        output="${template%.template}"
        echo "Processing template: $template -> $output"
        envsubst '${DOMAIN_NAME} ${BACKEND_HOST} ${BACKEND_PORT} ${FRONTEND_HOST} ${FRONTEND_PORT}' < "$template" > "$output"
    fi
done

# Check if SSL certificates exist
SSL_CERT="/etc/letsencrypt/live/${DOMAIN_NAME}/fullchain.pem"
SSL_KEY="/etc/letsencrypt/live/${DOMAIN_NAME}/privkey.pem"

if [ -f "$SSL_CERT" ] && [ -f "$SSL_KEY" ]; then
    echo "SSL certificates found, enabling HTTPS configuration"
    # Enable SSL configuration
    if [ -f "/etc/nginx/conf.d/jeticu-ssl.conf.disabled" ]; then
        mv /etc/nginx/conf.d/jeticu-ssl.conf.disabled /etc/nginx/conf.d/jeticu-ssl.conf
    fi
else
    echo "SSL certificates not found, using HTTP only"
    # Disable SSL configuration
    if [ -f "/etc/nginx/conf.d/jeticu-ssl.conf" ]; then
        mv /etc/nginx/conf.d/jeticu-ssl.conf /etc/nginx/conf.d/jeticu-ssl.conf.disabled
    fi
fi

# Test nginx configuration
nginx -t

# Execute the main command
exec "$@"