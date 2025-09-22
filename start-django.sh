#!/bin/bash
set -e

cd /app/backend

# Wait for database
if [ "$AZURE_DB_HOST" ]; then
    echo "Waiting for Azure Database at $AZURE_DB_HOST:$AZURE_DB_PORT..."
    while ! nc -z "$AZURE_DB_HOST" "${AZURE_DB_PORT:-5432}"; do
        echo "Database is unavailable - sleeping"
        sleep 2
    done
    echo "Azure Database is ready!"
elif [ "$DB_HOST" ]; then
    echo "Waiting for database at $DB_HOST:$DB_PORT..."
    while ! nc -z "$DB_HOST" "${DB_PORT:-5432}"; do
        echo "Database is unavailable - sleeping"
        sleep 2
    done
    echo "Database is ready!"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if specified
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser if it doesn't exist..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='$DJANGO_SUPERUSER_EMAIL',
        password='$DJANGO_SUPERUSER_PASSWORD'
    )
    print('Superuser created.')
else:
    print('Superuser already exists.')
END
fi

# Load initial data if specified
if [ "$LOAD_INITIAL_DATA" = "true" ]; then
    echo "Loading initial data..."
    python manage.py loaddata initial_data.json || echo "No initial data to load"
fi

# Run setup commands
if [ "$RUN_SETUP_COMMANDS" = "true" ]; then
    echo "Running setup commands..."
    python manage.py setup_permissions || echo "Permissions setup skipped"
fi

echo "Starting Gunicorn server..."
exec gunicorn backend.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 4 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
