# JET ICU Operations - Unified Docker Setup

This repository now includes a unified Docker setup that runs both the frontend (Vue.js) and backend (Django) in a single container using supervisord to manage both processes.

## Architecture

- **Frontend**: Vue.js application served by Nginx on port 80
- **Backend**: Django API served by Gunicorn on port 8000 (internal)
- **Reverse Proxy**: Nginx proxies `/api/*` requests to the Django backend
- **Process Management**: Supervisord manages both Nginx and Gunicorn processes
- **Database**: PostgreSQL (separate container)

## Quick Start

### Production Deployment

```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

The application will be available at:
- **Frontend**: http://localhost
- **API**: http://localhost/api/
- **Admin**: http://localhost/api/admin/

### Development Deployment

```bash
# Use the development compose file
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

The development setup includes:
- Source code mounting for live development
- Debug mode enabled
- Different database (jeticu_dev)
- Frontend on port 3000, API accessible via /api/

## Environment Variables

### Database Configuration
- `DB_HOST`: Database host (default: db)
- `DB_PORT`: Database port (default: 5432)
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password

### Django Configuration
- `DJANGO_SETTINGS_MODULE`: Django settings module
- `DJANGO_SECRET_KEY`: Django secret key
- `DJANGO_DEBUG`: Debug mode (True/False)
- `DJANGO_ALLOWED_HOSTS`: Comma-separated allowed hosts

### Superuser Creation
- `DJANGO_SUPERUSER_USERNAME`: Admin username
- `DJANGO_SUPERUSER_EMAIL`: Admin email
- `DJANGO_SUPERUSER_PASSWORD`: Admin password

### Setup Flags
- `LOAD_INITIAL_DATA`: Load initial data fixtures (true/false)
- `RUN_SETUP_COMMANDS`: Run setup management commands (true/false)

## Build Arguments

- `VITE_APP_API_URL`: Frontend API URL (default: /api)

## Volumes

- `static_volume`: Django static files
- `media_volume`: User uploaded media files
- `documents_volume`: Generated PDF documents
- `postgres_data`: PostgreSQL data

## Health Checks

The container includes health checks for both services:
- **Frontend**: HTTP check on port 80
- **Backend**: HTTP check on `/api/health/`
- **Database**: PostgreSQL ready check

## Logs

View logs for specific services:

```bash
# All services
docker-compose logs -f

# Application container only
docker-compose logs -f app

# Database only
docker-compose logs -f db

# Inside the container - supervisord logs
docker-compose exec app tail -f /var/log/supervisor/supervisord.log
docker-compose exec app tail -f /var/log/supervisor/nginx.out.log
docker-compose exec app tail -f /var/log/supervisor/django.out.log
```

## Development Workflow

### Making Changes

1. **Frontend Changes**: 
   - Make changes in `Operations/frontend/`
   - Rebuild the container: `docker-compose build app`
   - Restart: `docker-compose up -d`

2. **Backend Changes**:
   - In development mode, changes are live-mounted
   - In production, rebuild: `docker-compose build app`

### Database Operations

```bash
# Run Django management commands
docker-compose exec app python /app/backend/manage.py migrate
docker-compose exec app python /app/backend/manage.py collectstatic
docker-compose exec app python /app/backend/manage.py createsuperuser

# Access database directly
docker-compose exec db psql -U jeticu -d jeticu
```

### Debugging

```bash
# Access container shell
docker-compose exec app /bin/bash

# Check supervisord status
docker-compose exec app supervisorctl status

# Restart individual services
docker-compose exec app supervisorctl restart nginx
docker-compose exec app supervisorctl restart django
```

## Production Considerations

1. **Security**: Update default passwords and secret keys
2. **SSL**: Add SSL termination (nginx or load balancer)
3. **Scaling**: Use external database and file storage
4. **Monitoring**: Add application monitoring and logging
5. **Backups**: Implement database backup strategy

## Troubleshooting

### Common Issues

1. **Port Conflicts**: Change ports in docker-compose.yml if 80/8000 are in use
2. **Database Connection**: Ensure database is ready before Django starts
3. **Static Files**: Run `collectstatic` if static files are missing
4. **Permissions**: Check file permissions in mounted volumes

### Useful Commands

```bash
# Check container status
docker-compose ps

# View resource usage
docker-compose top

# Restart services
docker-compose restart

# Clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## Migration from Separate Containers

If migrating from separate frontend/backend containers:

1. **Backup Data**: Export database and media files
2. **Update Environment**: Use new environment variables
3. **Test**: Run in development mode first
4. **Deploy**: Use production docker-compose.yml
5. **Restore Data**: Import database and media files

## Support

For issues with the Docker setup, check:
1. Container logs: `docker-compose logs -f`
2. Supervisord status: `docker-compose exec app supervisorctl status`
3. Health checks: `docker-compose ps`
4. Resource usage: `docker stats`
