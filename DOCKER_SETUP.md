# JET ICU Operations - Docker Production Setup

## Streamlined Two-Container Architecture

This setup provides a clean, production-ready environment with:
- **Backend**: Django API with Gunicorn + PostgreSQL
- **Frontend**: Vue.js SPA served by Nginx with API proxy

## Quick Start

1. **Configure Environment**:
   ```bash
   cp .env.production .env.prod
   # Edit .env.prod with your actual values
   ```

2. **Update Key Settings** in `.env.prod`:
   - `DJANGO_SECRET_KEY`: Generate a secure key
   - `AZURE_DB_*`: Your Azure PostgreSQL connection details
   - `DOMAIN_NAME`: Your production domain
   - `ENCRYPTION_KEY`: Generate a 32-byte key for HIPAA encryption

3. **Build and Run**:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

4. **Check Status**:
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   docker-compose -f docker-compose.prod.yml logs -f
   ```

## Services

### Backend (port 8000)
- Django REST API with Gunicorn
- Automatic migrations and static file collection
- Health check endpoint: `/api/health/`
- Optimized for production with gevent workers

### Frontend (port 80)
- Vue.js SPA built with Vite
- Served by Nginx with optimized caching
- API proxy to backend container
- Health check endpoint: `/health`

## File Structure

```
/JET-MAIN/
├── docker-compose.prod.yml     # Main production compose file
├── .env.production             # Environment template
├── .env.prod                   # Your actual env file (gitignored)
└── Operations/
    ├── backend/
    │   ├── Dockerfile          # Optimized Django image
    │   └── entrypoint.sh       # Production startup script
    └── frontend/
        ├── Dockerfile          # Nginx + Vue build
        └── nginx.conf          # Proxy configuration
```

## Environment Variables

### Required Variables
- `DJANGO_SECRET_KEY`: Django secret key
- `AZURE_DB_HOST`: Database host
- `AZURE_DB_USER`: Database username
- `AZURE_DB_PASSWORD`: Database password
- `ENCRYPTION_KEY`: HIPAA encryption key

### Optional Variables
- `DOMAIN_NAME`: Production domain
- `EMAIL_*`: SMTP configuration
- `TWILIO_*`: SMS notifications
- `SENTRY_DSN`: Error tracking

## Deployment Commands

```bash
# Build and start
docker-compose -f docker-compose.prod.yml up --build -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Stop services
docker-compose -f docker-compose.prod.yml down

# Update and restart
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up --build -d

# Execute commands in running containers
docker-compose -f docker-compose.prod.yml exec backend python manage.py shell
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

## Scaling

Scale individual services:
```bash
# Scale backend to 3 instances
docker-compose -f docker-compose.prod.yml up --scale backend=3 -d

# Scale frontend to 2 instances
docker-compose -f docker-compose.prod.yml up --scale frontend=2 -d
```

## Troubleshooting

### Common Issues

1. **Database connection fails**:
   - Check `AZURE_DB_*` variables in `.env.prod`
   - Verify Azure PostgreSQL firewall settings
   - Ensure database exists

2. **Frontend can't reach backend**:
   - Check docker network: `docker network ls`
   - Verify both containers are on `jeticu-network`
   - Check nginx logs: `docker-compose -f docker-compose.prod.yml logs frontend`

3. **Permission errors**:
   - Ensure entrypoint.sh is executable
   - Check volume mounts and permissions

### Health Checks

- Backend: `curl http://localhost:8000/api/health/`
- Frontend: `curl http://localhost/health`
- Combined: `curl http://localhost/api/health/`

### Monitoring

```bash
# Container stats
docker stats

# System resource usage
docker system df

# Container details
docker-compose -f docker-compose.prod.yml top
```

## Security

- Non-root users in containers
- HIPAA-compliant encryption enabled
- Security headers configured in Nginx
- Secrets managed via environment variables
- HTTPS ready (add SSL certificates to nginx config)

## Azure Deployment

This setup is optimized for Azure:
- Azure Database for PostgreSQL
- Azure Container Instances
- Azure App Service (Docker Compose)
- Azure Storage (optional for media files)