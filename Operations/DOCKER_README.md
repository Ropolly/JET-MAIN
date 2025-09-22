# JET ICU Operations Platform - Docker Setup Guide

## Overview

This guide explains how to run the JET ICU Operations platform using Docker, both for local development and production deployment.

## Prerequisites

- Docker Engine 20.10+ and Docker Compose 2.0+
- 4GB+ RAM available for Docker
- Ports 8001 (backend), 5173 (frontend), 5432 (PostgreSQL) available

## Quick Start (Docker Development)

1. **Clone and setup environment:**
```bash
# Copy environment template
cp .env.docker .env

# Optional: Edit .env if you need custom settings
```

2. **Start all services:**
```bash
# Build and start all containers
docker-compose up --build

# Or run in background
docker-compose up -d
```

3. **Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8001/api
- Django Admin: http://localhost:8001/admin (admin/admin123)

## Development Workflows

### Option 1: Full Docker Development
Use Docker for everything (PostgreSQL, Django, Vue):
```bash
docker-compose up
```

### Option 2: Hybrid Development
Use Docker only for PostgreSQL, run Django/Vue locally:
```bash
# Start only PostgreSQL
docker-compose up postgres

# Run Django locally
cd backend
python manage.py runserver 8001

# Run Vue locally
cd frontend
npm run dev
```

### Option 3: Traditional Development (No Docker)
Continue using your existing setup - Docker is optional!

## Service Management

### Individual Services
```bash
# Start specific service
docker-compose up backend
docker-compose up frontend
docker-compose up postgres

# Rebuild specific service
docker-compose build backend
docker-compose up backend --build
```

### Database Operations
```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access Django shell
docker-compose exec backend python manage.py shell

# Database shell
docker-compose exec postgres psql -U postgres -d jeticu_dev
```

### Logs and Debugging
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Access container shell
docker-compose exec backend sh
docker-compose exec frontend sh
```

## Production Deployment

### Build for Production
```bash
# Build production images
docker build -t jeticu/backend:latest -f backend/Dockerfile ./backend
docker build -t jeticu/frontend:latest -f frontend/Dockerfile ./frontend
```

### Deploy with Azure Database
```bash
# Use production compose file (no local PostgreSQL)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Environment Variables
Production requires `.env.production` with:
- Azure Database for PostgreSQL credentials
- Azure Key Vault configuration
- Production API keys
- SSL/TLS settings

See `.env.production.example` for full template.

## Azure Deployment

### Azure Container Instances
```bash
# Push to Azure Container Registry
az acr build --registry jeticuacr --image backend:v1 ./backend
az acr build --registry jeticuacr --image frontend:v1 ./frontend

# Deploy containers
az container create \
  --resource-group jeticu-rg \
  --name jeticu-app \
  --image jeticuacr.azurecr.io/backend:v1 \
  --environment-variables-file .env.production
```

### Azure App Service
```bash
# Deploy to App Service (Web App for Containers)
az webapp create \
  --resource-group jeticu-rg \
  --plan jeticu-plan \
  --name jeticu-backend \
  --deployment-container-image-name jeticu/backend:latest
```

## File Structure

```
Operations/
├── docker-compose.yml          # Local development setup
├── docker-compose.prod.yml     # Production overrides
├── .env.example               # Environment template
├── .env.docker                # Docker dev environment
├── .env.production.example    # Production template
├── .dockerignore
│
├── backend/
│   ├── Dockerfile             # Production image
│   ├── Dockerfile.dev         # Development image
│   ├── entrypoint.sh         # Production startup
│   ├── entrypoint.dev.sh     # Dev startup
│   └── requirements.txt
│
└── frontend/
    ├── Dockerfile             # Production image
    ├── Dockerfile.dev         # Development image
    └── nginx.conf            # Nginx config for production
```

## Troubleshooting

### Port Conflicts
```bash
# Check what's using ports
lsof -i :8001
lsof -i :5173
lsof -i :5432

# Stop all containers
docker-compose down
```

### Database Issues
```bash
# Reset database
docker-compose down -v  # Warning: Deletes data!
docker-compose up postgres
```

### Build Issues
```bash
# Clean rebuild
docker-compose down
docker system prune -f
docker-compose build --no-cache
docker-compose up
```

### Permission Issues
```bash
# Fix permissions on Linux/Mac
sudo chown -R $USER:$USER .
```

## Security Notes

- **Never commit** `.env`, `.env.production`, or any file with secrets
- Use Azure Key Vault for production secrets
- Rotate encryption keys regularly
- Enable SSL/TLS in production
- Keep Docker images updated

## Useful Commands

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: Deletes data)
docker-compose down -v

# View running containers
docker ps

# Clean up unused resources
docker system prune -af

# Check resource usage
docker stats

# Export database
docker-compose exec postgres pg_dump -U postgres jeticu_dev > backup.sql

# Import database
docker-compose exec -T postgres psql -U postgres jeticu_dev < backup.sql
```

## Support

For issues or questions:
- Check logs: `docker-compose logs`
- Verify environment: `docker-compose config`
- Ensure ports are free
- Check Docker daemon is running

## Next Steps

1. Copy `.env.docker` to `.env`
2. Run `docker-compose up`
3. Access http://localhost:5173
4. Start developing!

Remember: Docker is optional - you can continue using your existing local setup!