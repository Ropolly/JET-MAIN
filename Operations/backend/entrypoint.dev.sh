#!/bin/sh

# Development entrypoint script for Django

set -e

echo "Starting JET ICU Backend (Development)..."

# Wait for PostgreSQL to be ready
if [ "$DB_HOST" ]; then
    echo "Waiting for PostgreSQL at $DB_HOST:${DB_PORT:-5432}..."
    while ! nc -z "$DB_HOST" "${DB_PORT:-5432}"; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 1
    done
    echo "PostgreSQL is ready!"
fi

# Run migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create cache table if using database cache
python manage.py createcachetable 2>/dev/null || true

# Create superuser for development if it doesn't exist
echo "Creating development superuser if needed..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@jeticu.local',
        password='admin123'
    )
    print('Development superuser created: admin/admin123')
else:
    print('Superuser already exists.')
END

# Collect static files (for admin and other static resources)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Load sample data if specified
if [ "$LOAD_SAMPLE_DATA" = "true" ]; then
    echo "Loading sample data..."
    python manage.py loaddata sample_data.json 2>/dev/null || echo "No sample data found"
fi

echo "Starting Django development server..."

# Execute the command passed to the container
exec "$@"