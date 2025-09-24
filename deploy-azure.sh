#!/bin/bash

# JET ICU Operations - Azure Deployment Script
# Deploy containers with Azure PostgreSQL backend

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOMAIN_NAME=""
EMAIL=""
PROJECT_DIR="/opt/jeticu"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Check if running with correct permissions
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Please run as a regular user with sudo privileges."
   exit 1
fi

print_header "JET ICU Operations - Azure Deployment"

# Check if domain and email are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    print_error "Usage: $0 <domain.com> <admin@email.com>"
    print_error "Example: $0 jeticu.com admin@jeticu.com"
    exit 1
fi

DOMAIN_NAME="$1"
EMAIL="$2"

print_status "Deploying JET ICU Operations for domain: $DOMAIN_NAME"

# Verify prerequisites
print_status "Checking prerequisites..."

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if nginx is installed
if ! command -v nginx &> /dev/null; then
    print_warning "Nginx is not installed. Installing nginx..."
    sudo apt update
    sudo apt install -y nginx
fi

# Check if certbot is installed
if ! command -v certbot &> /dev/null; then
    print_warning "Certbot is not installed. Installing certbot..."
    sudo apt update
    sudo apt install -y certbot python3-certbot-nginx
fi

# Create project directory if it doesn't exist
if [ ! -d "$PROJECT_DIR" ]; then
    print_status "Creating project directory: $PROJECT_DIR"
    sudo mkdir -p "$PROJECT_DIR"
    sudo chown $USER:$USER "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# Update environment file
print_status "Configuring environment file..."
if [ ! -f ".env.azure" ]; then
    print_error ".env.azure file not found. Please create it with your Azure PostgreSQL credentials."
    exit 1
fi

# Update domain in environment file
sed -i "s/DOMAIN_NAME=.*/DOMAIN_NAME=$DOMAIN_NAME/" .env.azure
sed -i "s/SSL_EMAIL=.*/SSL_EMAIL=$EMAIL/" .env.azure

# Update nginx configuration with actual domain
print_status "Updating nginx configuration..."
sudo cp nginx/jeticu.conf /etc/nginx/sites-available/jeticu.conf
sudo sed -i "s/your-domain.com/$DOMAIN_NAME/g" /etc/nginx/sites-available/jeticu.conf

# Create nginx sites-enabled symlink
if [ ! -L "/etc/nginx/sites-enabled/jeticu.conf" ]; then
    sudo ln -sf /etc/nginx/sites-available/jeticu.conf /etc/nginx/sites-enabled/
fi

# Remove default nginx site
if [ -L "/etc/nginx/sites-enabled/default" ]; then
    sudo rm /etc/nginx/sites-enabled/default
fi

# Test nginx configuration
print_status "Testing nginx configuration..."
sudo nginx -t

# Start/restart nginx
print_status "Starting nginx..."
sudo systemctl enable nginx
sudo systemctl restart nginx

# Verify domain DNS
print_status "Verifying domain DNS..."
DOMAIN_IP=$(dig +short $DOMAIN_NAME)
SERVER_IP=$(curl -s ifconfig.me)

if [ "$DOMAIN_IP" != "$SERVER_IP" ]; then
    print_warning "Domain $DOMAIN_NAME does not point to this server ($SERVER_IP)."
    print_warning "Current DNS points to: $DOMAIN_IP"
    print_warning "Please update your DNS records before proceeding with SSL."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Obtain SSL certificate
print_status "Obtaining SSL certificate..."
sudo mkdir -p /var/www/certbot

# Try to obtain certificate
if sudo certbot certonly --webroot --webroot-path=/var/www/certbot --email $EMAIL --agree-tos --no-eff-email -d $DOMAIN_NAME -d www.$DOMAIN_NAME; then
    print_status "SSL certificate obtained successfully"
else
    print_warning "SSL certificate could not be obtained. Continuing with HTTP only."
    # Use HTTP-only nginx config
    sudo sed -i 's/listen 443 ssl http2/listen 443 ssl http2; return 444/' /etc/nginx/sites-available/jeticu.conf
    sudo systemctl reload nginx
fi

# Test Azure PostgreSQL connection
print_status "Testing Azure PostgreSQL connection..."
source .env.azure

python3 -c "
import psycopg2
import os
import sys

try:
    conn = psycopg2.connect(
        host='$DB_HOST',
        port='$DB_PORT',
        database='$DB_NAME',
        user='$DB_USER',
        password='$DB_PASSWORD',
        sslmode='require'
    )
    print('✅ Azure PostgreSQL connection successful')
    conn.close()
except Exception as e:
    print(f'❌ Azure PostgreSQL connection failed: {e}')
    sys.exit(1)
" || {
    print_error "Azure PostgreSQL connection failed. Please check your credentials in .env.azure"
    exit 1
}

# Pull latest code (if git repo)
if [ -d ".git" ]; then
    print_status "Pulling latest code..."
    git pull
fi

# Build and start containers
print_status "Building Docker containers..."
docker-compose build --no-cache

print_status "Starting containers..."
docker-compose up -d

# Wait for containers to be healthy
print_status "Waiting for containers to be healthy..."
sleep 30

# Check container health
print_status "Checking container health..."
docker-compose ps

# Check if backend is responding
if curl -f http://localhost:8000/api/health/ >/dev/null 2>&1; then
    print_status "✅ Backend container is healthy"
else
    print_error "❌ Backend container is not responding"
    docker-compose logs backend
fi

# Check if frontend is responding
if curl -f http://localhost:3000/health >/dev/null 2>&1; then
    print_status "✅ Frontend container is healthy"
else
    print_error "❌ Frontend container is not responding"
    docker-compose logs frontend
fi

# Setup automatic SSL renewal
print_status "Setting up automatic SSL renewal..."
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet && /usr/bin/systemctl reload nginx") | crontab -

# Setup container restart on reboot
print_status "Setting up container auto-start..."
(crontab -l 2>/dev/null; echo "@reboot cd $PROJECT_DIR && /usr/local/bin/docker-compose up -d") | crontab -

# Setup log rotation
print_status "Setting up log rotation..."
sudo tee /etc/logrotate.d/jeticu << EOF
/var/log/nginx/jeticu_*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload nginx > /dev/null 2>&1 || true
    endscript
}
EOF

print_header "Deployment Complete!"
print_status "Application should be available at:"
print_status "  HTTP:  http://$DOMAIN_NAME"
print_status "  HTTPS: https://$DOMAIN_NAME (if SSL was successful)"
print_status ""
print_status "Container status:"
docker-compose ps
print_status ""
print_status "To view logs:"
print_status "  Backend:  docker-compose logs -f backend"
print_status "  Frontend: docker-compose logs -f frontend"
print_status ""
print_status "To restart services:"
print_status "  docker-compose restart"
print_status ""
print_warning "Next steps:"
print_warning "1. Test your application thoroughly"
print_warning "2. Set up monitoring and alerting"
print_warning "3. Configure your Azure PostgreSQL firewall rules"
print_warning "4. Set up database backups in Azure"

exit 0