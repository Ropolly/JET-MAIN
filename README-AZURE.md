# JET ICU Operations - Azure Deployment Guide

## Clean Container Architecture with Azure PostgreSQL

This setup provides a production-ready deployment with:
- **Backend Container**: Django API with Gunicorn
- **Frontend Container**: Vue.js SPA with Nginx
- **Host Nginx**: SSL termination and reverse proxy
- **Azure PostgreSQL**: Managed database service

## Architecture Overview

```
Internet → Host Nginx (SSL) → Backend Container (Django API:8000)
                           ↘ Frontend Container (Vue.js:3000)
                           ↘ Azure PostgreSQL (managed)
```

## Quick Deployment

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx and Certbot
sudo apt install -y nginx certbot python3-certbot-nginx

# Clone repository
cd /opt
sudo mkdir jeticu && sudo chown $USER:$USER jeticu
cd jeticu
git clone https://github.com/your-username/JET-MAIN.git .
```

### 2. Configure Environment

```bash
# Copy and edit environment file
cp .env.azure .env.production
nano .env.production
```

**Required Settings in `.env.production`:**

```bash
# Domain
DOMAIN_NAME=yourdomain.com

# Django
DJANGO_SECRET_KEY=your-super-secret-key-change-this
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Azure PostgreSQL
DB_HOST=your-server.postgres.database.azure.com
DB_USER=your-db-user@your-server
DB_PASSWORD=your-secure-password
DB_NAME=jeticu_prod

# HIPAA Encryption
ENCRYPTION_KEY=your-32-byte-base64-key

# Email
EMAIL_HOST=smtp.yourmailserver.com
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
```

### 3. Deploy

```bash
# Make deployment script executable
chmod +x deploy-azure.sh

# Deploy (replace with your domain and email)
./deploy-azure.sh yourdomain.com admin@yourdomain.com
```

## Manual Steps

If you prefer manual deployment:

### 1. Configure Nginx

```bash
# Copy nginx configuration
sudo cp nginx/jeticu.conf /etc/nginx/sites-available/
sudo ln -sf /etc/nginx/sites-available/jeticu.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Update domain in config
sudo sed -i 's/your-domain.com/yourdomain.com/g' /etc/nginx/sites-available/jeticu.conf

# Test and restart
sudo nginx -t
sudo systemctl restart nginx
```

### 2. Obtain SSL Certificate

```bash
# Create webroot directory
sudo mkdir -p /var/www/certbot

# Obtain certificate
sudo certbot certonly --webroot --webroot-path=/var/www/certbot \
  --email admin@yourdomain.com --agree-tos --no-eff-email \
  -d yourdomain.com -d www.yourdomain.com
```

### 3. Start Containers

```bash
# Build and start
docker-compose build
docker-compose up -d

# Check status
docker-compose ps
```

## Azure PostgreSQL Setup

### 1. Create Database Server

```bash
# Create resource group
az group create --name jeticu-rg --location eastus

# Create PostgreSQL server
az postgres server create \
  --resource-group jeticu-rg \
  --name jeticu-db-server \
  --location eastus \
  --admin-user jeticu_admin \
  --admin-password YourSecurePassword123! \
  --sku-name GP_Gen5_2 \
  --version 13

# Create database
az postgres db create \
  --resource-group jeticu-rg \
  --server-name jeticu-db-server \
  --name jeticu_prod
```

### 2. Configure Firewall

```bash
# Allow your server IP
az postgres server firewall-rule create \
  --resource-group jeticu-rg \
  --server jeticu-db-server \
  --name AllowServerIP \
  --start-ip-address YOUR_SERVER_IP \
  --end-ip-address YOUR_SERVER_IP
```

### 3. Test Connection

```bash
# Install PostgreSQL client
sudo apt install -y postgresql-client

# Test connection
psql "host=jeticu-db-server.postgres.database.azure.com port=5432 dbname=jeticu_prod user=jeticu_admin@jeticu-db-server password=YourSecurePassword123! sslmode=require"
```

## File Structure

```
/opt/jeticu/
├── docker-compose.yml           # 2-container setup
├── .env.azure                   # Environment template
├── .env.production              # Your actual config
├── deploy-azure.sh              # Deployment script
├── nginx/
│   └── jeticu.conf              # Host nginx config
└── Operations/
    ├── backend/
    │   ├── Dockerfile
    │   └── entrypoint.sh
    └── frontend/
        ├── Dockerfile
        └── nginx.conf
```

## Management Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart

# Update application
git pull
docker-compose build
docker-compose up -d

# Database operations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic

# Shell access
docker-compose exec backend python manage.py shell
docker-compose exec backend bash
```

## Monitoring

### Container Health
```bash
# Check container status
docker-compose ps

# Check resource usage
docker stats

# Check nginx status
sudo systemctl status nginx
```

### Application Health
```bash
# Backend health
curl -f https://yourdomain.com/api/health/

# Frontend health
curl -f https://yourdomain.com/health

# SSL certificate
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

## Troubleshooting

### Common Issues

1. **SSL Certificate Issues**
   ```bash
   # Check certificate status
   sudo certbot certificates

   # Renew certificate
   sudo certbot renew
   ```

2. **Database Connection Issues**
   ```bash
   # Check Azure PostgreSQL firewall
   # Verify connection string in .env.production
   # Test connection manually
   ```

3. **Container Issues**
   ```bash
   # Check logs
   docker-compose logs backend

   # Rebuild containers
   docker-compose build --no-cache
   ```

### Log Locations

- **Nginx**: `/var/log/nginx/jeticu_*.log`
- **Container**: `docker-compose logs [service]`
- **System**: `journalctl -u nginx`

## Security Features

- **HTTPS/TLS**: Let's Encrypt SSL certificates
- **HIPAA Headers**: Security headers for compliance
- **Rate Limiting**: API and general request limiting
- **Firewall**: Azure PostgreSQL firewall rules
- **Container Security**: Non-root users in containers
- **Input Validation**: File upload restrictions

## Backup Strategy

Since you're using Azure PostgreSQL:

1. **Automatic Backups**: Enabled by default in Azure
2. **Point-in-time Recovery**: Available for 7-35 days
3. **Manual Backups**: Use Azure portal or CLI
4. **Media Files**: Consider Azure Blob Storage

## Production Checklist

- [ ] Domain DNS points to server
- [ ] SSL certificate obtained and working
- [ ] Azure PostgreSQL firewall configured
- [ ] Environment variables set correctly
- [ ] Database migrations run
- [ ] Static files collected
- [ ] Superuser account created
- [ ] Email/SMS notifications configured
- [ ] Monitoring set up
- [ ] Backup strategy confirmed

## Support

- **Logs**: Check container and nginx logs
- **Database**: Use Azure portal for database monitoring
- **SSL**: Use certbot for certificate management
- **Updates**: Standard git pull + docker-compose workflow