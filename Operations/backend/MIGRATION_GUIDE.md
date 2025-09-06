# Django Backend Refactoring Migration Guide

This guide outlines the steps to migrate from the monolithic `api/` app structure to the new modular Django app architecture.

## Overview

The refactoring breaks down the monolithic `api/` app into focused domain apps:
- `users/` - Authentication, roles, permissions, profiles
- `contacts/` - Contact management, FBOs, Ground services
- `airports/` - Airport data and weather services
- `aircraft/` - Aircraft management and maintenance
- `operations/` - Trip operations, quotes, passengers, patients
- `documents/` - Document management, agreements, templates
- `finance/` - Transactions, invoices, payment methods
- `common/` - Shared utilities, base models, permissions

## Migration Steps

### Phase 1: Preparation
1. **Backup Database**
   ```bash
   python manage.py dumpdata > backup_before_refactor.json
   ```

2. **Install New Apps**
   - Update `INSTALLED_APPS` in settings.py with new apps
   - Ensure all new app directories are created with proper structure

3. **Create Initial Migrations**
   ```bash
   python manage.py makemigrations users
   python manage.py makemigrations contacts
   python manage.py makemigrations airports
   python manage.py makemigrations aircraft
   python manage.py makemigrations operations
   python manage.py makemigrations documents
   python manage.py makemigrations finance
   python manage.py makemigrations common
   ```

### Phase 2: Data Migration Scripts

#### 2.1 User Data Migration
```python
# management/commands/migrate_users.py
from django.core.management.base import BaseCommand
from api.models import UserProfile, Role, Permission, Department  # Old models
from users.models import UserProfile as NewUserProfile, Role as NewRole, Permission as NewPermission, Department as NewDepartment

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Migrate Roles
        for old_role in Role.objects.all():
            NewRole.objects.get_or_create(
                name=old_role.name,
                defaults={
                    'description': old_role.description,
                    'is_active': old_role.is_active
                }
            )
        
        # Migrate Permissions
        for old_perm in Permission.objects.all():
            NewPermission.objects.get_or_create(
                name=old_perm.name,
                defaults={
                    'description': old_perm.description,
                    'resource': old_perm.resource,
                    'action': old_perm.action
                }
            )
        
        # Migrate UserProfiles
        for old_profile in UserProfile.objects.all():
            new_profile, created = NewUserProfile.objects.get_or_create(
                user=old_profile.user,
                defaults={
                    'phone_number': old_profile.phone_number,
                    'address': old_profile.address,
                    'emergency_contact': old_profile.emergency_contact,
                    'hire_date': old_profile.hire_date,
                    'is_active': old_profile.is_active
                }
            )
            # Migrate many-to-many relationships
            new_profile.roles.set([NewRole.objects.get(name=role.name) for role in old_profile.roles.all()])
            new_profile.permissions.set([NewPermission.objects.get(name=perm.name) for perm in old_profile.permissions.all()])
```

#### 2.2 Contact Data Migration
```python
# management/commands/migrate_contacts.py
from django.core.management.base import BaseCommand
from api.models import Contact, FBO, Ground  # Old models
from contacts.models import Contact as NewContact, FBO as NewFBO, Ground as NewGround

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Migrate Contacts
        for old_contact in Contact.objects.all():
            NewContact.objects.get_or_create(
                id=old_contact.id,
                defaults={
                    'first_name': old_contact.first_name,
                    'last_name': old_contact.last_name,
                    'email': old_contact.email,
                    'phone': old_contact.phone,
                    'company': old_contact.company,
                    'title': old_contact.title,
                    'address': old_contact.address,
                    'notes': old_contact.notes,
                    'contact_type': old_contact.contact_type,
                    'is_active': old_contact.is_active
                }
            )
        
        # Similar migrations for FBO and Ground models...
```

#### 2.3 Airport Data Migration
```python
# management/commands/migrate_airports.py
from django.core.management.base import BaseCommand
from api.models import Airport, WeatherData  # Old models
from airports.models import Airport as NewAirport, WeatherData as NewWeatherData

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Migrate Airports
        for old_airport in Airport.objects.all():
            NewAirport.objects.get_or_create(
                icao_code=old_airport.icao_code,
                defaults={
                    'iata_code': old_airport.iata_code,
                    'name': old_airport.name,
                    'city': old_airport.city,
                    'state': old_airport.state,
                    'country': old_airport.country,
                    'latitude': old_airport.latitude,
                    'longitude': old_airport.longitude,
                    'elevation': old_airport.elevation,
                    'timezone': old_airport.timezone,
                    'is_active': old_airport.is_active
                }
            )
```

#### 2.4 Operations Data Migration
```python
# management/commands/migrate_operations.py
from django.core.management.base import BaseCommand
from api.models import Trip, Quote, Patient, Passenger  # Old models
from operations.models import Trip as NewTrip, Quote as NewQuote, Patient as NewPatient, Passenger as NewPassenger
from contacts.models import Contact
from airports.models import Airport
from aircraft.models import Aircraft

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Migrate Quotes
        for old_quote in Quote.objects.all():
            new_quote = NewQuote.objects.create(
                id=old_quote.id,
                quoted_amount=old_quote.quoted_amount,
                contact=Contact.objects.get(id=old_quote.contact_id),
                pickup_airport=Airport.objects.get(icao_code=old_quote.pickup_airport.icao_code),
                dropoff_airport=Airport.objects.get(icao_code=old_quote.dropoff_airport.icao_code),
                aircraft_type=old_quote.aircraft_type,
                estimated_flight_time=old_quote.estimated_flight_time,
                # ... other fields
            )
            # Handle many-to-many and foreign key relationships
        
        # Similar for other operations models...
```

### Phase 3: URL and Settings Updates

#### 3.1 Update Main URLs
```python
# backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/contacts/', include('contacts.urls')),
    path('api/airports/', include('airports.urls')),
    path('api/aircraft/', include('aircraft.urls')),
    path('api/operations/', include('operations.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/finance/', include('finance.urls')),
]
```

#### 3.2 Update Settings
```python
# backend/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # New modular apps
    'common',
    'users',
    'contacts',
    'airports',
    'aircraft',
    'operations',
    'documents',
    'finance',
    
    # Remove old 'api' app after migration
]
```

### Phase 4: Testing and Validation

#### 4.1 Run Migration Commands
```bash
# Run data migration commands
python manage.py migrate_users
python manage.py migrate_contacts
python manage.py migrate_airports
python manage.py migrate_aircraft
python manage.py migrate_operations
python manage.py migrate_documents
python manage.py migrate_finance

# Apply database migrations
python manage.py migrate
```

#### 4.2 Validate Data Integrity
```bash
# Run tests to ensure data integrity
python manage.py test users
python manage.py test contacts
python manage.py test airports
python manage.py test aircraft
python manage.py test operations
python manage.py test documents
python manage.py test finance
```

#### 4.3 API Endpoint Testing
```bash
# Test API endpoints
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/operations/trips/
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/contacts/contacts/
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/finance/transactions/
```

### Phase 5: Cleanup

#### 5.1 Remove Old API App
1. **Verify all data migrated successfully**
2. **Update any remaining references to old models**
3. **Remove `api` from INSTALLED_APPS**
4. **Delete `api/` directory**

#### 5.2 Update Documentation
1. **Update API documentation**
2. **Update deployment scripts**
3. **Update frontend integration points**

## Rollback Plan

If issues arise during migration:

1. **Stop the migration process**
2. **Restore from backup**
   ```bash
   python manage.py loaddata backup_before_refactor.json
   ```
3. **Revert settings and URL changes**
4. **Investigate and fix issues**
5. **Retry migration with fixes**

## Post-Migration Benefits

- **Modular Architecture**: Each app handles a specific domain
- **Better Code Organization**: Clear separation of concerns
- **Improved Maintainability**: Easier to locate and modify code
- **Enhanced Testing**: Focused test suites per app
- **Scalable Development**: Teams can work on different apps independently
- **Service Layer Pattern**: Business logic separated from models and views
- **Consistent API Structure**: RESTful endpoints with proper routing

## Environment Variables

Ensure these environment variables are set:
```bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_HOSTS=your-domain.com,localhost
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

## Monitoring and Logging

After migration, monitor:
- **API response times**
- **Database query performance**
- **Error rates and logs**
- **User authentication flows**
- **File upload/download operations**

This migration transforms the monolithic Django backend into a clean, modular architecture that supports scalable SaaS development.
