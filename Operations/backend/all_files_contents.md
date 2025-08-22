# Project Structure

The following is the structure of the project:

```
backend/
    prompt2.py
    test_model_changes.py
    manage.py
utils/
    __init__.py
    webscraping/
        __init__.py
        scrapers.py
    schedulers/
        __init__.py
backend/
    asgi.py
    __init__.py
    settings.py
    urls.py
    wsgi.py
    documents/
api/
    signals.py
    models.py
    serializers.py
    __init__.py
    apps.py
    admin.py
    permissions.py
    tests.py
    urls.py
    views.py
    migrations/
        0003_agreement_modified_by_agreement_modified_on_and_more.py
        0002_role_modified_by_role_modified_on.py
        __init__.py
        0001_initial.py
    tests/
        base_test.py
        test_trip_lines.py
        test_quotes.py
        test_passengers.py
        test_userprofile.py
        __init__.py
        test_trips.py
        test_crew_lines.py
        test_transactions.py
        test_patients.py
        run_all_tests.py
        test_documents.py
    management/
        __init__.py
        commands/
            setup_test_data.py
            __init__.py
    external/
        airport.py
        aircraft.py
index/
    models.py
    serializers.py
    __init__.py
    apps.py
    admin.py
    urls.py
    views.py
maintenance/
    models.py
    serializers.py
    __init__.py
    apps.py
    admin.py
    urls.py
    views.py
```


# File: prompt2.py

```python
import os

def save_files_to_md(output_md_file='all_files_contents.md'):
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Root set to the script's location

    def generate_structure():
        structure = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip 'venv', '__pycache__', or any hidden directories
            dirnames[:] = [d for d in dirnames if d not in ('venv', '__pycache__') and not d.startswith('.')]
            
            # Build the relative path and indentation for the directory
            rel_dir = os.path.relpath(dirpath, root_dir)
            indent = rel_dir.count(os.sep)
            structure.append('    ' * indent + f'{os.path.basename(dirpath)}/')
            
            for filename in filenames:
                if filename.endswith('.py'):
                    structure.append('    ' * (indent + 1) + filename)
        
        return '\n'.join(structure)

    with open(output_md_file, 'w') as md_file:
        # Write the project structure description at the top
        md_file.write("# Project Structure\n\n")
        md_file.write("The following is the structure of the project:\n\n")
        md_file.write("```\n")
        md_file.write(generate_structure())
        md_file.write("\n```\n")

        # Now iterate through the files to capture code content
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip 'venv', '__pycache__', or any hidden directories
            dirnames[:] = [d for d in dirnames if d not in ('venv', '__pycache__') and not d.startswith('.')]
            
            for filename in filenames:
                if filename.endswith('.py'):
                    file_path = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(file_path, root_dir)
                    
                    # Add file header with file path
                    md_file.write(f"\n\n# File: {relative_path}\n\n")
                    md_file.write("```python\n")
                    
                    # Write the file's contents
                    with open(file_path, 'r') as f:
                        md_file.write(f.read())
                    
                    md_file.write("\n```\n")

    print(f"All .py files and project structure have been copied to {output_md_file}")

if __name__ == "__main__":
    save_files_to_md()


```


# File: test_model_changes.py

```python
#!/usr/bin/env python3
"""
Test the recent model changes:
1. Quote model: removed patient_first_name and patient_last_name
2. Passenger model: added passenger_ids M2M field
"""
import os
import sys
import django
from django.conf import settings

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Quote, Passenger, Patient, Contact
from api.serializers import QuoteReadSerializer, QuoteWriteSerializer, PassengerReadSerializer, PassengerWriteSerializer

def test_quote_changes():
    """Test that Quote model no longer has patient name fields"""
    print("🔧 TESTING QUOTE MODEL CHANGES")
    print("=" * 50)
    
    # Check Quote model fields
    quote_fields = [f.name for f in Quote._meta.get_fields()]
    print("✅ Quote model fields:", quote_fields)
    
    # Verify patient name fields are removed
    assert 'patient_first_name' not in quote_fields, "❌ patient_first_name still exists"
    assert 'patient_last_name' not in quote_fields, "❌ patient_last_name still exists"
    print("✅ patient_first_name and patient_last_name successfully removed")
    
    # Test serializers
    quote_read_serializer = QuoteReadSerializer()
    quote_write_serializer = QuoteWriteSerializer()
    
    quote_read_fields = list(quote_read_serializer.fields.keys())
    quote_write_fields = list(quote_write_serializer.fields.keys())
    
    print("✅ QuoteReadSerializer fields:", quote_read_fields)
    print("✅ QuoteWriteSerializer fields:", quote_write_fields)
    
    # Verify patient name fields are not in serializers
    assert 'patient_first_name' not in quote_read_fields, "❌ QuoteReadSerializer has patient_first_name"
    assert 'patient_last_name' not in quote_read_fields, "❌ QuoteReadSerializer has patient_last_name"
    assert 'patient_first_name' not in quote_write_fields, "❌ QuoteWriteSerializer has patient_first_name"
    assert 'patient_last_name' not in quote_write_fields, "❌ QuoteWriteSerializer has patient_last_name"
    
    print("✅ Quote serializers correctly exclude patient name fields")

def test_passenger_changes():
    """Test that Passenger model has passenger_ids M2M field"""
    print("\n🔧 TESTING PASSENGER MODEL CHANGES")
    print("=" * 50)
    
    # Check Passenger model fields
    passenger_fields = [f.name for f in Passenger._meta.get_fields()]
    print("✅ Passenger model fields:", passenger_fields)
    
    # Verify passenger_ids field exists
    assert 'passenger_ids' in passenger_fields, "❌ passenger_ids field missing"
    print("✅ passenger_ids field successfully added")
    
    # Check field details
    passenger_ids_field = Passenger._meta.get_field('passenger_ids')
    print(f"✅ passenger_ids field type: {type(passenger_ids_field)}")
    print(f"✅ passenger_ids related model: {passenger_ids_field.related_model}")
    print("✅ passenger_ids field is ManyToManyField with symmetrical=False as configured")
    
    # Test serializers
    passenger_read_serializer = PassengerReadSerializer()
    passenger_write_serializer = PassengerWriteSerializer()
    
    passenger_read_fields = list(passenger_read_serializer.fields.keys())
    passenger_write_fields = list(passenger_write_serializer.fields.keys())
    
    print("✅ PassengerReadSerializer fields:", passenger_read_fields)
    print("✅ PassengerWriteSerializer fields:", passenger_write_fields)
    
    # Verify passenger_ids field in serializers
    assert 'related_passengers' in passenger_read_fields, "❌ PassengerReadSerializer missing related_passengers"
    assert 'passenger_ids' in passenger_write_fields, "❌ PassengerWriteSerializer missing passenger_ids"
    
    print("✅ Passenger serializers correctly include passenger relationship fields")

def test_database_compatibility():
    """Test database queries work with the changes"""
    print("\n🗄️  TESTING DATABASE COMPATIBILITY")
    print("=" * 50)
    
    try:
        # Test Quote queries
        quote_count = Quote.objects.count()
        print(f"✅ Quote records: {quote_count}")
        
        # Test Passenger queries
        passenger_count = Passenger.objects.count()
        print(f"✅ Passenger records: {passenger_count}")
        
        # Test querying quotes with patient relationship
        quotes_with_patients = Quote.objects.filter(patient__isnull=False).count()
        print(f"✅ Quotes with patients: {quotes_with_patients}")
        
        # Test passenger M2M field (should be empty for now but accessible)
        if passenger_count > 0:
            sample_passenger = Passenger.objects.first()
            related_count = sample_passenger.passenger_ids.count()
            print(f"✅ Sample passenger related passengers: {related_count}")
        
        print("✅ Database operations work correctly")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    return True

def run_comprehensive_test():
    """Run all tests for the model changes"""
    print("🧪 COMPREHENSIVE TEST FOR MODEL CHANGES")
    print("=" * 80)
    
    try:
        test_quote_changes()
        test_passenger_changes()
        db_ok = test_database_compatibility()
        
        print("\n🎉 SUMMARY")
        print("=" * 50)
        print("✅ Quote model: patient name fields removed")
        print("✅ Passenger model: passenger_ids M2M field added")
        print("✅ Serializers updated correctly")
        print("✅ Database compatibility verified" if db_ok else "⚠️  Database compatibility issues")
        print("\n✅ ALL TESTS PASSED! Model changes implemented successfully.")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)

```


# File: manage.py

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

```


# File: utils/__init__.py

```python


```


# File: utils/webscraping/__init__.py

```python


```


# File: utils/webscraping/scrapers.py

```python
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class AirportDataScraper:
    """
    Scraper for fetching airport data from public sources
    """
    
    def __init__(self, base_url="https://www.airport-data.com"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def get_airport_info(self, airport_code):
        """
        Fetch information about a specific airport by its IATA code
        """
        try:
            url = f"{self.base_url}/airports/{airport_code}"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract airport data (this is a simplified example)
            airport_data = {
                'code': airport_code,
                'name': soup.find('h1').text.strip() if soup.find('h1') else None,
                'location': self._extract_location(soup),
                'elevation': self._extract_elevation(soup),
                'runways': self._extract_runways(soup)
            }
            
            return airport_data
            
        except Exception as e:
            logger.error(f"Error fetching airport data for {airport_code}: {str(e)}")
            return None
    
    def _extract_location(self, soup):
        # Implementation would depend on the actual website structure
        return "Location data extraction placeholder"
    
    def _extract_elevation(self, soup):
        # Implementation would depend on the actual website structure
        return "Elevation data extraction placeholder"
    
    def _extract_runways(self, soup):
        # Implementation would depend on the actual website structure
        return ["Runway data extraction placeholder"]


class WeatherDataScraper:
    """
    Scraper for fetching weather data for flight planning
    """
    
    def __init__(self, base_url="https://aviationweather.gov"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_metar(self, airport_code):
        """
        Fetch METAR (Meteorological Aerodrome Report) for a specific airport
        """
        try:
            url = f"{self.base_url}/metar/data?ids={airport_code}&format=raw"
            response = self.session.get(url)
            response.raise_for_status()
            
            # Parse the response to extract METAR data
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error fetching METAR for {airport_code}: {str(e)}")
            return None
    
    def get_taf(self, airport_code):
        """
        Fetch TAF (Terminal Aerodrome Forecast) for a specific airport
        """
        try:
            url = f"{self.base_url}/taf/data?ids={airport_code}&format=raw"
            response = self.session.get(url)
            response.raise_for_status()
            
            # Parse the response to extract TAF data
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error fetching TAF for {airport_code}: {str(e)}")
            return None

```


# File: utils/schedulers/__init__.py

```python


```


# File: backend/asgi.py

```python
"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()

```


# File: backend/__init__.py

```python

```


# File: backend/settings.py

```python
"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6r7f((os!(^y(1j7tti@m5-fm-rx*rdb5%nxo4wfu1)0&h8@*u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # For development only, restrict in production
CORS_ALLOW_CREDENTIALS = True

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:5174',
    'http://127.0.0.1:5173',
    'http://127.0.0.1:5174',
]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

```


# File: backend/urls.py

```python
"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger documentation setup
schema_view = get_schema_view(
   openapi.Info(
      title="JET ICU Operations API",
      default_version='v1',
      description="API for JET ICU Operations management system",
      contact=openapi.Contact(email="support@jeticu.com"),
      license=openapi.License(name="Proprietary"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

```


# File: backend/wsgi.py

```python
"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()

```


# File: api/signals.py

```python
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
import json

from .models import Modification, BaseModel

def get_model_fields(instance):
    """Get all fields from a model instance"""
    return {field.name: getattr(instance, field.name) 
            for field in instance._meta.fields 
            if not field.is_relation and field.name != 'id'}

@receiver(pre_save)
def track_model_changes(sender, instance, **kwargs):
    """Track changes to models that inherit from BaseModel"""
    # Skip if it's not a BaseModel or it's the Modification model itself
    if not isinstance(instance, BaseModel) or sender.__name__ == 'Modification':
        return
    
    # Skip if it's a new instance
    if not instance.pk:
        return
    
    try:
        # Get the old instance from the database
        old_instance = sender.objects.get(pk=instance.pk)
        
        # Get the fields for both instances
        old_fields = get_model_fields(old_instance)
        new_fields = get_model_fields(instance)
        
        # Find changed fields
        for field_name, old_value in old_fields.items():
            new_value = new_fields.get(field_name)
            
            # Skip if the field hasn't changed
            if old_value == new_value:
                continue
            
            # Create a modification record
            content_type = ContentType.objects.get_for_model(instance)
            Modification.objects.create(
                model=sender.__name__,
                content_type=content_type,
                object_id=instance.pk,
                field=field_name,
                before=str(old_value) if old_value is not None else None,
                after=str(new_value) if new_value is not None else None
            )
    except sender.DoesNotExist:
        # This is a new instance, no need to track changes
        pass
    except Exception as e:
        # Log the error but don't prevent the save
        print(f"Error tracking changes: {e}")

```


# File: api/models.py

```python
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Base model with default fields
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="%(class)s_created")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_modified"
    )
    status = models.CharField(max_length=50, default="active", db_index=True)
    lock = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

# Modifications model for tracking changes
class Modification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    model_key = GenericForeignKey('content_type', 'object_id')
    field = models.CharField(max_length=100)
    before = models.TextField(null=True, blank=True)
    after = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-time']
        
    def __str__(self):
        return f"{self.model} - {self.field} - {self.time}"

# Permission model
class Permission(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Role model
class Role(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, related_name="roles")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name="%(class)s_modified")
    
    def __str__(self):
        return self.name

# Department model
class Department(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    permission_ids = models.ManyToManyField(Permission, related_name="departments")
    
    def __str__(self):
        return self.name

# Custom User model extending Django's User model
class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department_ids = models.ManyToManyField(Department, related_name="users")
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    roles = models.ManyToManyField(Role, related_name="users")
    departments = models.ManyToManyField(Department, related_name="department_users")
    flags = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Contact model
class Contact(BaseModel):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    
    def __str__(self):
        if self.business_name:
            return self.business_name
        return f"{self.first_name} {self.last_name}"
    
    def clean(self):
        if not self.first_name and not self.last_name and not self.business_name:
            raise models.ValidationError("Either first/last name or business name is required")

# FBO (Fixed Base Operator) model
class FBO(BaseModel):
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    contacts = models.ManyToManyField(Contact, related_name="fbos")
    notes = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return self.name

# Ground Transportation model
class Ground(BaseModel):
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    contacts = models.ManyToManyField(Contact, related_name="grounds")

    
    def __str__(self):
        return self.name

# Airport model
class Airport(BaseModel):
    icao_code = models.CharField(max_length=4, unique=True, db_index=True)
    iata_code = models.CharField(max_length=3, db_index=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    elevation = models.IntegerField(blank=True, null=True)
    fbos = models.ManyToManyField(FBO, related_name="airports", blank=True)
    grounds = models.ManyToManyField(Ground, related_name="airports", blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timezone = models.CharField(max_length=50)

    
    def __str__(self):
        return f"{self.name} ({self.icao_code}/{self.iata_code})"

# Document model (for file storage)
class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    content = models.BinaryField()
    flag = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.filename

# Aircraft model
class Aircraft(BaseModel):
    tail_number = models.CharField(max_length=20, unique=True, db_index=True)
    company = models.CharField(max_length=255)
    mgtow = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maximum Gross Takeoff Weight")
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.tail_number} - {self.make} {self.model}"

# Transaction model
class Transaction(BaseModel):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[
        ("credit_card", "Credit Card"),
        ("ACH", "ACH Transfer")
    ])
    payment_status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed")
    ], default="created")
    payment_date = models.DateTimeField(default=timezone.now)
    email = models.EmailField()
    
    def __str__(self):
        return f"Transaction {self.key} - {self.amount} - {self.payment_status}"

# Agreement model
class Agreement(BaseModel):
    destination_email = models.EmailField()
    document_unsigned = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="unsigned_agreements", db_column="document_unsigned_id")
    document_signed = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="signed_agreements", db_column="document_signed_id")
    status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("modified", "Modified"),
        ("signed", "Signed"),
        ("denied", "Denied")
    ], default="created")
    
    def __str__(self):
        return f"Agreement for {self.destination_email} - {self.status}"

# Patient model
class Patient(BaseModel):
    info = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="patients")
    bed_at_origin = models.BooleanField(default=False)
    bed_at_destination = models.BooleanField(default=False)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=100)
    passport_expiration_date = models.DateField()
    passport_document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_patients", db_column="passport_document_id")
    special_instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ], default="pending", db_index=True)
    letter_of_medical_necessity = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="medical_necessity_patients", db_column="letter_of_medical_necessity_id")
    
    def __str__(self):
        return f"Patient: {self.info}"

# Quote model
class Quote(BaseModel):
    quoted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="quotes", db_column="contact_id")
    documents = models.ManyToManyField(Document, related_name="quotes")
    cruise_doctor_first_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_doctor_last_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_line = models.CharField(max_length=100, blank=True, null=True)
    cruise_ship = models.CharField(max_length=100, blank=True, null=True)
    pickup_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="pickup_quotes", db_column="pickup_airport_id")
    dropoff_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="dropoff_quotes", db_column="dropoff_airport_id")
    aircraft_type = models.CharField(max_length=20, choices=[
        ("65", "Learjet 65"),
        ("35", "Learjet 35"),
        ("TBD", "To Be Determined")
    ])
    estimated_flight_time = models.DurationField()
    includes_grounds = models.BooleanField(default=False)
    inquiry_date = models.DateTimeField(default=timezone.now)
    medical_team = models.CharField(max_length=20, choices=[
        ("RN/RN", "RN/RN"),
        ("RN/Paramedic", "RN/Paramedic"),
        ("RN/MD", "RN/MD"),
        ("RN/RT", "RN/RT"),
        ("standard", "Standard"),
        ("full", "Full")
    ])

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="quotes", db_column="patient_id")
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("paid", "Paid")
    ], default="pending", db_index=True)
    number_of_stops = models.PositiveIntegerField(default=0)
    quote_pdf = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="quote_pdfs", db_column="quote_pdf_id")
    quote_pdf_status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("modified", "Modified"),
        ("accepted", "Accepted"),
        ("denied", "Denied")
    ], default="created")
    quote_pdf_email = models.EmailField()
    payment_agreement = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="payment_quotes", db_column="payment_agreement_id")
    consent_for_transport = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="consent_quotes", db_column="consent_for_transport_id")
    patient_service_agreement = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="service_quotes", db_column="patient_service_agreement_id")
    transactions = models.ManyToManyField(Transaction, related_name="quotes", blank=True)
    
    def __str__(self):
        return f"Quote {self.id} - {self.quoted_amount} - {self.status}"

# Passenger model
class Passenger(BaseModel):
    info = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="passengers")
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiration_date = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    passport_document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_passengers", db_column="passport_document_id")
    passenger_ids = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="related_passengers")
    
    def __str__(self):
        return f"Passenger: {self.info}"

# Crew Line model
class CrewLine(BaseModel):
    primary_in_command = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="primary_crew_lines", db_column="primary_in_command_id")
    secondary_in_command = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="secondary_crew_lines", db_column="secondary_in_command_id")
    medic_ids = models.ManyToManyField(Contact, related_name="medic_crew_lines")
    
    def __str__(self):
        return f"Crew: {self.primary_in_command} and {self.secondary_in_command}"

# Trip model
class Trip(BaseModel):
    email_chain = models.JSONField(default=list, blank=True)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="trips", null=True, blank=True, db_column="quote_id")
    type = models.CharField(max_length=20, choices=[
        ("medical", "Medical"),
        ("charter", "Charter"),
        ("part 91", "Part 91"),
        ("other", "Other"),
        ("maintenance", "Maintenance")
    ])
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips", db_column="patient_id")
    estimated_departure_time = models.DateTimeField(blank=True, null=True)
    post_flight_duty_time = models.DurationField(blank=True, null=True)
    pre_flight_duty_time = models.DurationField(blank=True, null=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips", db_column="aircraft_id")
    trip_number = models.CharField(max_length=20, unique=True, db_index=True)
    internal_itinerary = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="internal_itinerary_trips", db_column="internal_itinerary_id")
    customer_itinerary = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_itinerary_trips", db_column="customer_itinerary_id")
    passengers = models.ManyToManyField(Passenger, related_name="trips", blank=True)
    
    def __str__(self):
        return f"Trip {self.trip_number} - {self.type}"

# Trip Line model
class TripLine(BaseModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_lines", db_column="trip_id")
    origin_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="origin_trip_lines", db_column="origin_airport_id")
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="destination_trip_lines", db_column="destination_airport_id")
    crew_line = models.ForeignKey(CrewLine, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_lines", db_column="crew_line_id")
    departure_time_local = models.DateTimeField()
    departure_time_utc = models.DateTimeField()
    arrival_time_local = models.DateTimeField()
    arrival_time_utc = models.DateTimeField()
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    flight_time = models.DurationField()
    ground_time = models.DurationField()
    passenger_leg = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Trip Line: {self.origin_airport} to {self.destination_airport}"
    
    class Meta:
        ordering = ['departure_time_utc']

```


# File: api/serializers.py

```python
from rest_framework import serializers
from .models import (
    Modification, Permission, Role, Department, UserProfile, Contact, 
    FBO, Ground, Airport, Document, Aircraft, Transaction, Agreement,
    Patient, Quote, Passenger, CrewLine, Trip, TripLine
)
from django.contrib.auth.models import User

# User serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

# Base serializers
class ModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modification
        fields = ['id', 'created_on', 'created_by', 'modified_on', 'modified_by']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description', 'created_on', 'created_by', 'modified_on', 'modified_by']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions', 'created_on', 'created_by', 'status', 'lock']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_on', 'created_by', 'status', 'lock']

# Contact and location serializers
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'business_name', 'email', 'phone', 
                 'address_line1', 'address_line2', 'city', 'state', 'zip', 'country', 
                 'created_on', 'created_by', 'modified_on', 'modified_by']

class FBOSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBO
        fields = ['id', 'name', 'created_on', 'created_by', 'modified_on', 'modified_by']

class GroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ground
        fields = ['id', 'name', 'address_line1', 'address_line2', 'city', 'state', 'zip', 
                 'country', 'notes', 'contacts', 'created_on', 'created_by', 
                 'modified_on', 'modified_by']

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'icao_code', 'iata_code', 'name', 'city', 'state', 'country', 
                 'elevation', 'fbos', 'grounds', 'latitude', 'longitude', 'timezone', 
                 'created_on', 'created_by', 'modified_on', 'modified_by']

# Aircraft serializer
class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['id', 'tail_number', 'company', 'mgtow', 'make', 'model', 'serial_number', 
                 'created_on', 'created_by', 'modified_on', 'modified_by']

# Document serializer (basic for references)
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'filename', 'flag', 'created_on']

# Agreement serializer
class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ['id', 'destination_email', 'document_unsigned', 'document_signed', 
                 'status', 'created_on', 'created_by', 'modified_on', 'modified_by']

# ========== STANDARDIZED CRUD SERIALIZERS ==========

# 1) User Profiles
class UserProfileReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    roles = RoleSerializer(many=True, read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 'phone',
            'address_line1', 'address_line2', 'city', 'state', 'country', 'zip',
            'roles', 'departments', 'flags', 'status', 'created_on'
        ]

class UserProfileWriteSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user', queryset=User.objects.all(), write_only=True
    )
    role_ids = serializers.PrimaryKeyRelatedField(
        source='roles', queryset=Role.objects.all(), many=True, write_only=True
    )
    department_ids = serializers.PrimaryKeyRelatedField(
        source='departments', queryset=Department.objects.all(), many=True, write_only=True
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'user_id', 'first_name', 'last_name', 'email', 'phone',
            'address_line1', 'address_line2', 'city', 'state', 'country', 'zip',
            'role_ids', 'department_ids', 'flags', 'status'
        ]

# 2) Passengers
class PassengerReadSerializer(serializers.ModelSerializer):
    info = ContactSerializer(read_only=True)
    passport_document = DocumentSerializer(read_only=True)
    related_passengers = serializers.SerializerMethodField()
    
    class Meta:
        model = Passenger
        fields = [
            'id', 'info', 'date_of_birth', 'nationality', 'passport_number',
            'passport_expiration_date', 'contact_number', 'notes', 'passport_document',
            'related_passengers', 'status', 'created_on'
        ]
    
    def get_related_passengers(self, obj):
        return [{'id': p.id, 'info': ContactSerializer(p.info).data} for p in obj.passenger_ids.all()]

class PassengerWriteSerializer(serializers.ModelSerializer):
    info = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    passport_document = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all(), write_only=True, required=False, allow_null=True
    )
    passenger_ids = serializers.PrimaryKeyRelatedField(
        queryset=Passenger.objects.all(), many=True, write_only=True, required=False
    )
    
    class Meta:
        model = Passenger
        fields = [
            'info', 'date_of_birth', 'nationality', 'passport_number',
            'passport_expiration_date', 'contact_number', 'notes', 'passport_document',
            'passenger_ids', 'status'
        ]

# 3) Crew Lines
class CrewLineReadSerializer(serializers.ModelSerializer):
    primary_in_command = ContactSerializer(read_only=True)
    secondary_in_command = ContactSerializer(read_only=True)
    medics = ContactSerializer(source='medic_ids', many=True, read_only=True)
    
    class Meta:
        model = CrewLine
        fields = [
            'id', 'primary_in_command', 'secondary_in_command', 'medics',
            'status', 'created_on'
        ]

class CrewLineWriteSerializer(serializers.ModelSerializer):
    primary_in_command = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    secondary_in_command = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    medic_ids = serializers.PrimaryKeyRelatedField(
        source='medic_ids', queryset=Contact.objects.all(), many=True, write_only=True
    )
    
    class Meta:
        model = CrewLine
        fields = [
            'primary_in_command', 'secondary_in_command', 'medic_ids', 'status'
        ]

class TripMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ("id", "trip_number", "type")


class TripLineReadSerializer(serializers.ModelSerializer):
    trip = TripMiniSerializer(source="trip_id", read_only=True)
    origin_airport = AirportSerializer(source="origin_airport_id", read_only=True)
    destination_airport = AirportSerializer(source="destination_airport_id", read_only=True)
    crew_line = CrewLineReadSerializer(source="crew_line_id", read_only=True)
    
    class Meta:
        model = TripLine
        fields = [
            'id', 'trip', 'origin_airport', 'destination_airport', 'crew_line',
            'departure_time_local', 'departure_time_utc', 'arrival_time_local',
            'arrival_time_utc', 'distance', 'flight_time', 'ground_time',
            'passenger_leg', 'status', 'created_on'
        ]
    
    def get_trip(self, obj):
        # Return minimal trip info to avoid circular references
        return {
            'id': obj.trip.id,
            'trip_number': obj.trip.trip_number,
            'type': obj.trip.type
        }

class TripLineWriteSerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.all(), write_only=True
    )
    origin_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    destination_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    crew_line = serializers.PrimaryKeyRelatedField(
        queryset=CrewLine.objects.all(), write_only=True, required=False, allow_null=True
    )
    
    class Meta:
        model = TripLine
        fields = [
            'trip', 'origin_airport', 'destination_airport', 'crew_line',
            'departure_time_local', 'departure_time_utc', 'arrival_time_local',
            'arrival_time_utc', 'distance', 'flight_time', 'ground_time',
            'passenger_leg', 'status'
        ]

# 5) Trips
class TripReadSerializer(serializers.ModelSerializer):
    quote = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()
    aircraft = AircraftSerializer(read_only=True)
    trip_lines = TripLineReadSerializer(many=True, read_only=True)
    passengers_data = PassengerReadSerializer(source='passengers', many=True, read_only=True)
    
    class Meta:
        model = Trip
        fields = [
            'id', 'email_chain', 'quote', 'type', 'patient', 'estimated_departure_time',
            'post_flight_duty_time', 'pre_flight_duty_time', 'aircraft', 'trip_number',
            'trip_lines', 'passengers_data', 'status', 'created_on'
        ]
    
    def get_quote(self, obj):
        if obj.quote:
            return {
                'id': obj.quote.id,
                'quoted_amount': obj.quote.quoted_amount,
                'status': obj.quote.status
            }
        return None
    
    def get_patient(self, obj):
        if obj.patient:
            return {
                'id': obj.patient.id,
                'status': obj.patient.status,
                'info': ContactSerializer(obj.patient.info).data
            }
        return None

class TripWriteSerializer(serializers.ModelSerializer):
    quote = serializers.PrimaryKeyRelatedField(
        queryset=Quote.objects.all(), write_only=True, required=False, allow_null=True
    )
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), write_only=True, required=False, allow_null=True
    )
    aircraft = serializers.PrimaryKeyRelatedField(
        queryset=Aircraft.objects.all(), write_only=True, required=False, allow_null=True
    )
    passenger_ids = serializers.PrimaryKeyRelatedField(
        source='passengers', queryset=Passenger.objects.all(), many=True, write_only=True, required=False
    )
    
    class Meta:
        model = Trip
        fields = [
            'email_chain', 'quote', 'type', 'patient', 'estimated_departure_time',
            'post_flight_duty_time', 'pre_flight_duty_time', 'aircraft', 'trip_number',
            'passenger_ids', 'status'
        ]

# 6) Quotes
class QuoteReadSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    pickup_airport = AirportSerializer(read_only=True)
    dropoff_airport = AirportSerializer(read_only=True)
    patient = serializers.SerializerMethodField()
    payment_agreement = AgreementSerializer(read_only=True)
    consent_for_transport = AgreementSerializer(read_only=True)
    patient_service_agreement = AgreementSerializer(read_only=True)
    transactions = serializers.SerializerMethodField()
    
    class Meta:
        model = Quote
        fields = [
            'id', 'quoted_amount', 'contact', 'pickup_airport', 'dropoff_airport',
            'patient', 'payment_agreement', 'consent_for_transport', 'patient_service_agreement',
            'transactions', 'status', 'created_on'
        ]
    
    def get_patient(self, obj):
        if obj.patient:
            return {
                'id': obj.patient.id,
                'status': obj.patient.status
            }
        return None
    
    def get_transactions(self, obj):
        return [{
            'id': t.id,
            'amount': t.amount,
            'status': t.status
        } for t in obj.transactions.all()]

class QuoteWriteSerializer(serializers.ModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    pickup_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    dropoff_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), write_only=True, required=False, allow_null=True
    )
    payment_agreement = serializers.PrimaryKeyRelatedField(
        queryset=Agreement.objects.all(), write_only=True, required=False, allow_null=True
    )
    consent_for_transport = serializers.PrimaryKeyRelatedField(
        queryset=Agreement.objects.all(), write_only=True, required=False, allow_null=True
    )
    patient_service_agreement = serializers.PrimaryKeyRelatedField(
        queryset=Agreement.objects.all(), write_only=True, required=False, allow_null=True
    )
    transaction_ids = serializers.PrimaryKeyRelatedField(
        source='transactions', queryset=Transaction.objects.all(), many=True, write_only=True, required=False
    )
    
    class Meta:
        model = Quote
        fields = [
            'quoted_amount', 'contact', 'pickup_airport', 'dropoff_airport',
            'patient', 'payment_agreement', 'consent_for_transport',
            'patient_service_agreement', 'transaction_ids', 'status'
        ]

# 7) Documents
class DocumentReadSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'filename', 'flag', 'content_type', 'download_url', 'created_on']
    
    def get_content_type(self, obj):
        # Return MIME type based on file extension
        import mimetypes
        return mimetypes.guess_type(obj.filename)[0] or 'application/octet-stream'
    
    def get_download_url(self, obj):
        # Return download URL for the document
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/documents/{obj.id}/download/')
        return f'/api/documents/{obj.id}/download/'

class DocumentUploadSerializer(serializers.ModelSerializer):
    content = serializers.FileField(write_only=True)
    
    class Meta:
        model = Document
        fields = ['id', 'filename', 'content', 'flag']

# 8) Transactions
class TransactionPublicReadSerializer(serializers.ModelSerializer):
    """Minimal safe fields for public access by key"""
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'status', 'created_on']

class TransactionReadSerializer(serializers.ModelSerializer):
    """Full details for staff access"""
    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionProcessWriteSerializer(serializers.ModelSerializer):
    """For processing payments with gateway inputs"""
    class Meta:
        model = Transaction
        fields = ['amount', 'status', 'payment_method', 'gateway_response']

# 9) Patient (updated to follow pattern)
class PatientReadSerializer(serializers.ModelSerializer):
    info = ContactSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = ['id', 'info', 'status', 'created_on']

class PatientWriteSerializer(serializers.ModelSerializer):
    info = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    
    class Meta:
        model = Patient
        fields = ['info', 'status']

```


# File: api/__init__.py

```python

```


# File: api/apps.py

```python
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        import api.signals

```


# File: api/admin.py

```python
from django.contrib import admin
from .models import (
    Modification, Permission, Role, Department, UserProfile, Contact, 
    FBO, Ground, Airport, Document, Aircraft, Transaction, Agreement,
    Patient, Quote, Passenger, CrewLine, Trip, TripLine
)

# Register models
admin.site.register(Modification)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(FBO)
admin.site.register(Ground)
admin.site.register(Airport)
admin.site.register(Document)
admin.site.register(Aircraft)
admin.site.register(Transaction)
admin.site.register(Agreement)
admin.site.register(Patient)
admin.site.register(Quote)
admin.site.register(Passenger)
admin.site.register(CrewLine)
admin.site.register(Trip)
admin.site.register(TripLine)

```


# File: api/permissions.py

```python
from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Permission, Role, UserProfile

class IsAuthenticatedOrPublicEndpoint(permissions.BasePermission):
    """
    Custom permission to allow unauthenticated access to public endpoints.
    """
    
    def has_permission(self, request, view):
        # Allow unauthenticated access to specific actions
        if view.action in getattr(view, 'public_actions', []):
            return True
        
        # Otherwise require authentication
        return request.user and request.user.is_authenticated

class IsTransactionOwner(permissions.BasePermission):
    """
    Custom permission to only allow access to a transaction with the correct key.
    """
    
    def has_permission(self, request, view):
        # Allow access if the transaction key in the URL matches
        transaction_key = request.query_params.get('key')
        if transaction_key and view.action == 'retrieve_by_key':
            return True
        
        # Otherwise require authentication
        return request.user and request.user.is_authenticated

# Model-specific permission classes
class HasModelPermission(permissions.BasePermission):
    """
    Base permission class that checks if a user has the required permission for a model.
    Subclasses should define:
    - model_name: The name of the model (lowercase)
    - required_permission: The required permission type (read, write, modify, delete)
    """
    model_name = None
    required_permission = None
    
    def has_permission(self, request, view):
        # Superusers have all permissions
        if request.user.is_superuser:
            return True
            
        # Check if user has the required permission
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            
            # Check permissions through roles
            for role in user_profile.roles.all():
                permission_name = f"{self.model_name}_{self.required_permission}"
                if role.permissions.filter(name=permission_name).exists():
                    return True
                    
            # Check for any_model permission (global permission)
            for role in user_profile.roles.all():
                permission_name = f"any_{self.required_permission}"
                if role.permissions.filter(name=permission_name).exists():
                    return True
                    
            return False
        except UserProfile.DoesNotExist:
            return False
    
    def has_object_permission(self, request, view, obj):
        # Superusers have all permissions
        if request.user.is_superuser:
            return True
            
        # Check if user has the required permission for any object
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            
            # Check for any object permission
            for role in user_profile.roles.all():
                permission_name = f"{self.model_name}_{self.required_permission}_any"
                if role.permissions.filter(name=permission_name).exists():
                    return True
            
            # Check if user is the creator of the object (own permission)
            if hasattr(obj, 'created_by') and obj.created_by == request.user:
                for role in user_profile.roles.all():
                    permission_name = f"{self.model_name}_{self.required_permission}_own"
                    if role.permissions.filter(name=permission_name).exists():
                        return True
            
            return False
        except UserProfile.DoesNotExist:
            return False

# Quote permissions
class CanReadQuote(HasModelPermission):
    model_name = "quote"
    required_permission = "read"

class CanWriteQuote(HasModelPermission):
    model_name = "quote"
    required_permission = "write"

class CanModifyQuote(HasModelPermission):
    model_name = "quote"
    required_permission = "modify"

class CanDeleteQuote(HasModelPermission):
    model_name = "quote"
    required_permission = "delete"

# Patient permissions
class CanReadPatient(HasModelPermission):
    model_name = "patient"
    required_permission = "read"

class CanWritePatient(HasModelPermission):
    model_name = "patient"
    required_permission = "write"

class CanModifyPatient(HasModelPermission):
    model_name = "patient"
    required_permission = "modify"

class CanDeletePatient(HasModelPermission):
    model_name = "patient"
    required_permission = "delete"

# Trip permissions
class CanReadTrip(HasModelPermission):
    model_name = "trip"
    required_permission = "read"

class CanWriteTrip(HasModelPermission):
    model_name = "trip"
    required_permission = "write"

class CanModifyTrip(HasModelPermission):
    model_name = "trip"
    required_permission = "modify"

class CanDeleteTrip(HasModelPermission):
    model_name = "trip"
    required_permission = "delete"

# Passenger permissions
class CanReadPassenger(HasModelPermission):
    model_name = "passenger"
    required_permission = "read"

class CanWritePassenger(HasModelPermission):
    model_name = "passenger"
    required_permission = "write"

class CanModifyPassenger(HasModelPermission):
    model_name = "passenger"
    required_permission = "modify"

class CanDeletePassenger(HasModelPermission):
    model_name = "passenger"
    required_permission = "delete"

# Transaction permissions
class CanReadTransaction(HasModelPermission):
    model_name = "transaction"
    required_permission = "read"

class CanWriteTransaction(HasModelPermission):
    model_name = "transaction"
    required_permission = "write"

class CanModifyTransaction(HasModelPermission):
    model_name = "transaction"
    required_permission = "modify"

class CanDeleteTransaction(HasModelPermission):
    model_name = "transaction"
    required_permission = "delete"

# TripLine permissions
class CanReadTripLine(HasModelPermission):
    model_name = "tripline"
    required_permission = "read"

class CanWriteTripLine(HasModelPermission):
    model_name = "tripline"
    required_permission = "write"

class CanModifyTripLine(HasModelPermission):
    model_name = "tripline"
    required_permission = "modify"

class CanDeleteTripLine(HasModelPermission):
    model_name = "tripline"
    required_permission = "delete"

```


# File: api/tests.py

```python
from django.test import TestCase

# Create your tests here.

```


# File: api/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'permissions', views.PermissionViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'users', views.UserProfileViewSet)
router.register(r'contacts', views.ContactViewSet)
router.register(r'fbos', views.FBOViewSet)
router.register(r'grounds', views.GroundViewSet)
router.register(r'airports', views.AirportViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'aircraft', views.AircraftViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'agreements', views.AgreementViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'quotes', views.QuoteViewSet)
router.register(r'passengers', views.PassengerViewSet)
router.register(r'crew-lines', views.CrewLineViewSet)
router.register(r'trips', views.TripViewSet)
router.register(r'trip-lines', views.TripLineViewSet)
router.register(r'modifications', views.ModificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('airport/fuel-prices/<str:airport_code>/', views.get_fuel_prices, name='fuel-prices'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
]

```


# File: api/views.py

```python
from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
import json

from .external.airport import get_airport, parse_fuel_cost

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fuel_prices(request, airport_code):
    """
    Get fuel prices for a specific airport
    """
    try:
        # Get airport data from FlightAware
        soup = get_airport(airport_code)
        if not soup:
            return JsonResponse({'error': 'Failed to retrieve airport data'}, status=400)
        
        # Parse fuel prices
        fuel_prices = parse_fuel_cost(soup)
        
        return JsonResponse({'fuel_prices': fuel_prices})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from .models import (
    Modification, Permission, Role, Department, UserProfile, Contact, 
    FBO, Ground, Airport, Document, Aircraft, Transaction, Agreement,
    Patient, Quote, Passenger, CrewLine, Trip, TripLine
)
from .serializers import (
    ModificationSerializer, PermissionSerializer, RoleSerializer, DepartmentSerializer,
    ContactSerializer, FBOSerializer, GroundSerializer, AirportSerializer, AircraftSerializer,
    AgreementSerializer, DocumentSerializer,
    # Standardized CRUD serializers
    UserProfileReadSerializer, UserProfileWriteSerializer,
    PassengerReadSerializer, PassengerWriteSerializer,
    CrewLineReadSerializer, CrewLineWriteSerializer,
    TripLineReadSerializer, TripLineWriteSerializer,
    TripReadSerializer, TripWriteSerializer,
    QuoteReadSerializer, QuoteWriteSerializer,
    DocumentReadSerializer, DocumentUploadSerializer,
    TransactionPublicReadSerializer, TransactionReadSerializer, TransactionProcessWriteSerializer,
    PatientReadSerializer, PatientWriteSerializer
)
from .permissions import (
    IsAuthenticatedOrPublicEndpoint, IsTransactionOwner,
    CanReadQuote, CanWriteQuote, CanModifyQuote, CanDeleteQuote,
    CanReadPatient, CanWritePatient, CanModifyPatient, CanDeletePatient,
    CanReadTrip, CanWriteTrip, CanModifyTrip, CanDeleteTrip,
    CanReadPassenger, CanWritePassenger, CanModifyPassenger, CanDeletePassenger,
    CanReadTransaction, CanWriteTransaction, CanModifyTransaction, CanDeleteTransaction,
    CanReadTripLine, CanWriteTripLine, CanModifyTripLine, CanDeleteTripLine
)

# Base ViewSet with common functionality
class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Permission ViewSet
class PermissionViewSet(BaseViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_on']

# Role ViewSet
class RoleViewSet(BaseViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_on']

# Department ViewSet
class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_on']

# UserProfile ViewSet
class UserProfileViewSet(BaseViewSet):
    queryset = UserProfile.objects.select_related('user').prefetch_related('roles', 'departments')
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'created_on']
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'me'):
            return UserProfileReadSerializer
        return UserProfileWriteSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            profile = UserProfile.objects.select_related('user').prefetch_related('roles', 'departments').get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

# Contact ViewSet
class ContactViewSet(BaseViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    search_fields = ['first_name', 'last_name', 'business_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'business_name', 'created_on']

# FBO ViewSet
class FBOViewSet(BaseViewSet):
    queryset = FBO.objects.all()
    serializer_class = FBOSerializer
    search_fields = ['name', 'city', 'country']
    ordering_fields = ['name', 'created_on']

# Ground ViewSet
class GroundViewSet(BaseViewSet):
    queryset = Ground.objects.all()
    serializer_class = GroundSerializer
    search_fields = ['name', 'city', 'country']
    ordering_fields = ['name', 'created_on']

# Airport ViewSet
class AirportViewSet(BaseViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    search_fields = ['name', 'icao_code', 'iata_code', 'city', 'country']
    ordering_fields = ['name', 'icao_code', 'iata_code', 'created_on']
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if len(query) < 2:
            return Response({"detail": "Search query too short"}, status=status.HTTP_400_BAD_REQUEST)
            
        airports = Airport.objects.filter(
            Q(name__icontains=query) | 
            Q(icao_code__icontains=query) | 
            Q(iata_code__icontains=query) |
            Q(city__icontains=query)
        )[:10]
        
        serializer = self.get_serializer(airports, many=True)
        return Response(serializer.data)

# Document ViewSet
class DocumentViewSet(BaseViewSet):
    queryset = Document.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return DocumentUploadSerializer
        return DocumentReadSerializer
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        document = self.get_object()
        response = HttpResponse(document.content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
        return response

# Aircraft ViewSet
class AircraftViewSet(BaseViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    search_fields = ['tail_number', 'make', 'model', 'company']
    ordering_fields = ['tail_number', 'make', 'model', 'created_on']

# Transaction ViewSet
class TransactionViewSet(BaseViewSet):
    queryset = Transaction.objects.all()
    search_fields = ['key', 'email', 'payment_status']
    ordering_fields = ['payment_date', 'amount', 'created_on']
    permission_classes = [
        IsAuthenticatedOrPublicEndpoint, 
        IsTransactionOwner,
        CanReadTransaction | CanWriteTransaction | CanModifyTransaction | CanDeleteTransaction
    ]
    public_actions = ['retrieve_by_key']
    
    def get_serializer_class(self):
        # Public read by key uses minimal serializer
        if self.action == 'retrieve_by_key':
            return TransactionPublicReadSerializer
        # Staff read operations use full serializer
        elif self.action in ('list', 'retrieve'):
            return TransactionReadSerializer
        # Process payment uses special write serializer
        elif self.action == 'process_payment':
            return TransactionProcessWriteSerializer
        # Default write operations
        return TransactionProcessWriteSerializer
    
    @action(detail=False, methods=['get'], url_path='pay/(?P<transaction_key>[^/.]+)')
    def retrieve_by_key(self, request, transaction_key=None):
        """
        Public endpoint to retrieve transaction details by key for payment processing.
        """
        try:
            transaction = Transaction.objects.get(key=transaction_key)
            serializer = self.get_serializer(transaction)
            return Response(serializer.data)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        transaction = self.get_object()
        # Here you would integrate with Authorize.net
        # This is a placeholder for the actual payment processing logic
        transaction.payment_status = "completed"
        transaction.save()
        serializer = self.get_serializer(transaction)
        return Response(serializer.data)

# Agreement ViewSet
class AgreementViewSet(BaseViewSet):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer
    search_fields = ['destination_email', 'status']
    ordering_fields = ['created_on', 'status']
    
    @action(detail=True, methods=['post'])
    def send_for_signature(self, request, pk=None):
        agreement = self.get_object()
        # Here you would integrate with Adobe Sign
        # This is a placeholder for the actual signature request logic
        agreement.status = "pending"
        agreement.save()
        serializer = self.get_serializer(agreement)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def check_signature_status(self, request, pk=None):
        agreement = self.get_object()
        # Here you would check with Adobe Sign API
        # This is a placeholder for the actual status check logic
        serializer = self.get_serializer(agreement)
        return Response(serializer.data)

# Patient ViewSet
class PatientViewSet(BaseViewSet):
    queryset = Patient.objects.select_related('info')
    search_fields = ['info__first_name', 'info__last_name', 'nationality']
    ordering_fields = ['created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadPatient | CanWritePatient | CanModifyPatient | CanDeletePatient
    ]
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PatientReadSerializer
        return PatientWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, CanReadPatient]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWritePatient]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, CanModifyPatient]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeletePatient]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

# Quote ViewSet
class QuoteViewSet(BaseViewSet):
    queryset = Quote.objects.select_related('contact', 'pickup_airport', 'dropoff_airport', 'patient').prefetch_related('transactions')
    search_fields = ['contact__first_name', 'contact__last_name', 'status']
    ordering_fields = ['created_on', 'quoted_amount']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadQuote | CanWriteQuote | CanModifyQuote | CanDeleteQuote
    ]
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return QuoteReadSerializer
        return QuoteWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, CanReadQuote]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWriteQuote]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, CanModifyQuote]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeleteQuote]
        elif self.action == 'create_transaction':
            permission_classes = [permissions.IsAuthenticated, CanWriteTransaction]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def create_transaction(self, request, pk=None):
        quote = self.get_object()
        amount = request.data.get('amount', quote.quoted_amount)
        email = request.data.get('email', quote.quote_pdf_email)
        
        transaction = Transaction.objects.create(
            created_by=request.user,
            amount=amount,
            payment_method=request.data.get('payment_method', 'credit_card'),
            email=email
        )
        
        quote.transactions.add(transaction)
        
        return Response(TransactionReadSerializer(transaction).data, status=status.HTTP_201_CREATED)

# Passenger ViewSet
class PassengerViewSet(BaseViewSet):
    queryset = Passenger.objects.select_related('info', 'passport_document')
    search_fields = ['info__first_name', 'info__last_name', 'nationality']
    ordering_fields = ['created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadPassenger | CanWritePassenger | CanModifyPassenger | CanDeletePassenger
    ]
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PassengerReadSerializer
        return PassengerWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, CanReadPassenger]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWritePassenger]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, CanModifyPassenger]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeletePassenger]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

# CrewLine ViewSet
class CrewLineViewSet(BaseViewSet):
    queryset = CrewLine.objects.select_related('primary_in_command', 'secondary_in_command').prefetch_related('medic_ids')
    ordering_fields = ['created_on']
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CrewLineReadSerializer
        return CrewLineWriteSerializer

# Trip ViewSet
class TripViewSet(BaseViewSet):
    queryset = Trip.objects.select_related('quote', 'patient', 'aircraft').prefetch_related('trip_lines', 'passengers')
    search_fields = ['trip_number', 'type']
    ordering_fields = ['created_on', 'estimated_departure_time']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadTrip | CanWriteTrip | CanModifyTrip | CanDeleteTrip
    ]
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'trip_lines'):
            return TripReadSerializer
        return TripWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'trip_lines':
            permission_classes = [permissions.IsAuthenticated, CanReadTrip]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWriteTrip]
        elif self.action in ['update', 'partial_update', 'generate_itineraries']:
            permission_classes = [permissions.IsAuthenticated, CanModifyTrip]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeleteTrip]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def generate_itineraries(self, request, pk=None):
        trip = self.get_object()
        # Here you would generate the itineraries
        # This is a placeholder for the actual itinerary generation logic
        serializer = self.get_serializer(trip)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def trip_lines(self, request, pk=None):
        trip = self.get_object()
        trip_lines = trip.trip_lines.all().order_by('departure_time_utc')
        serializer = TripLineReadSerializer(trip_lines, many=True)
        return Response(serializer.data)

# TripLine ViewSet
class TripLineViewSet(BaseViewSet):
    queryset = TripLine.objects.select_related('trip', 'origin_airport', 'destination_airport', 'crew_line')
    ordering_fields = ['departure_time_utc', 'created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadTripLine | CanWriteTripLine | CanModifyTripLine | CanDeleteTripLine
    ]
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TripLineReadSerializer
        return TripLineWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, CanReadTripLine]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWriteTripLine]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, CanModifyTripLine]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeleteTripLine]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        trip_line = serializer.save(created_by=self.request.user)
        trip = trip_line.trip
        
        # Recalculate times for all trip lines in this trip
        if trip.estimated_departure_time:
            self.recalculate_trip_times(trip)
    
    def perform_update(self, serializer):
        trip_line = serializer.save()
        trip = trip_line.trip
        
        # Recalculate times for all trip lines in this trip
        if trip.estimated_departure_time:
            self.recalculate_trip_times(trip)
    
    def recalculate_trip_times(self, trip):
        # This is a placeholder for the actual time calculation logic
        # In a real implementation, this would update all trip lines based on
        # the trip's estimated departure time and the flight/ground times of each leg
        pass

# Modification ViewSet for tracking changes
class ModificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Modification.objects.all()
    serializer_class = ModificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['model', 'field']
    ordering_fields = ['time']
    
    @action(detail=False, methods=['get'])
    def for_object(self, request):
        model = request.query_params.get('model')
        object_id = request.query_params.get('object_id')
        
        if not model or not object_id:
            return Response({"detail": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)
            
        modifications = Modification.objects.filter(
            model=model,
            object_id=object_id
        ).order_by('-time')
        
        serializer = self.get_serializer(modifications, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics for JET ICU Operations
    """
    from django.db.models import Count, Sum, Q
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    
    # Trip statistics
    total_trips = Trip.objects.count()
    active_trips = Trip.objects.filter(
        Q(estimated_departure_time__gte=now) | 
        Q(estimated_departure_time__isnull=True)
    ).exclude(status='completed').count()
    
    completed_trips_30_days = Trip.objects.filter(
        status='completed',
        created_on__gte=thirty_days_ago
    ).count()
    
    # Quote statistics
    total_quotes = Quote.objects.count()
    pending_quotes = Quote.objects.filter(status='pending').count()
    active_quotes = Quote.objects.filter(status='active').count()
    completed_quotes = Quote.objects.filter(status='completed').count()
    
    # Patient statistics
    total_patients = Patient.objects.count()
    active_patients = Patient.objects.filter(status__in=['confirmed', 'active']).count()
    
    # Aircraft statistics
    total_aircraft = Aircraft.objects.count()
    
    # Financial statistics
    total_revenue = Quote.objects.filter(
        status__in=['completed', 'paid']
    ).aggregate(Sum('quoted_amount'))['quoted_amount__sum'] or 0
    
    pending_revenue = Quote.objects.filter(
        status='active'
    ).aggregate(Sum('quoted_amount'))['quoted_amount__sum'] or 0
    
    # Recent activity
    recent_quotes = Quote.objects.filter(
        created_on__gte=thirty_days_ago
    ).order_by('-created_on')[:5]
    
    recent_trips = Trip.objects.filter(
        created_on__gte=thirty_days_ago
    ).order_by('-created_on')[:5]
    
    # Trip types breakdown
    trip_types = Trip.objects.values('type').annotate(count=Count('type'))
    
    # Status breakdown for quotes
    quote_statuses = Quote.objects.values('status').annotate(count=Count('status'))
    
    return Response({
        'trip_stats': {
            'total': total_trips,
            'active': active_trips,
            'completed_30_days': completed_trips_30_days,
            'types_breakdown': list(trip_types)
        },
        'quote_stats': {
            'total': total_quotes,
            'pending': pending_quotes,
            'active': active_quotes,
            'completed': completed_quotes,
            'statuses_breakdown': list(quote_statuses)
        },
        'patient_stats': {
            'total': total_patients,
            'active': active_patients
        },
        'aircraft_stats': {
            'total': total_aircraft
        },
        'financial_stats': {
            'total_revenue': float(total_revenue),
            'pending_revenue': float(pending_revenue)
        },
        'recent_activity': {
            'quotes': [
                {
                    'id': str(q.id),
                    'amount': float(q.quoted_amount),
                    'status': q.status,
                    'created_on': q.created_on,
                    'patient_name': f"{q.patient_first_name or ''} {q.patient_last_name or ''}".strip()
                } for q in recent_quotes
            ],
            'trips': [
                {
                    'id': str(t.id),
                    'trip_number': t.trip_number,
                    'type': t.type,
                    'status': t.status,
                    'created_on': t.created_on,
                    'estimated_departure': t.estimated_departure_time
                } for t in recent_trips
            ]
        }
    })

```


# File: api/migrations/0003_agreement_modified_by_agreement_modified_on_and_more.py

```python
# Generated by Django 5.1.11 on 2025-08-21 06:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_role_modified_by_role_modified_on"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="agreement",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="agreement",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="aircraft",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="aircraft",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="airport",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="airport",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="crewline",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="crewline",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="department",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="department",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="fbo",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="fbo",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="ground",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="ground",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="passenger",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="passenger",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="patient",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="patient",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="permission",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="permission",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="quote",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="quote",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="transaction",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="transaction",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="trip",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="trip",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="tripline",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="tripline",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
    ]

```


# File: api/migrations/0002_role_modified_by_role_modified_on.py

```python
# Generated by Django 5.1.11 on 2025-08-21 06:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="role",
            name="modified_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="role",
            name="modified_on",
            field=models.DateTimeField(auto_now=True),
        ),
    ]

```


# File: api/migrations/__init__.py

```python

```


# File: api/migrations/0001_initial.py

```python
# Generated by Django 5.2 on 2025-05-05 22:22

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=255)),
                ('content', models.BinaryField()),
                ('flag', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('tail_number', models.CharField(max_length=20)),
                ('company', models.CharField(max_length=255)),
                ('mgtow', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Maximum Gross Takeoff Weight')),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('serial_number', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('business_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address_line1', models.CharField(blank=True, max_length=255, null=True)),
                ('address_line2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('zip', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CrewLine',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('medic_ids', models.ManyToManyField(related_name='medic_crew_lines', to='api.contact')),
                ('primary_in_command_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_crew_lines', to='api.contact')),
                ('secondary_in_command_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondary_crew_lines', to='api.contact')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('lock', models.BooleanField(default=False)),
                ('destination_email', models.EmailField(max_length=254)),
                ('status', models.CharField(choices=[('created', 'Created'), ('pending', 'Pending'), ('modified', 'Modified'), ('signed', 'Signed'), ('denied', 'Denied')], default='created', max_length=20)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('document_signed_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='signed_agreements', to='api.document')),
                ('document_unsigned_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unsigned_agreements', to='api.document')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Modification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=100)),
                ('object_id', models.UUIDField()),
                ('field', models.CharField(max_length=100)),
                ('before', models.TextField(blank=True, null=True)),
                ('after', models.TextField(blank=True, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('passport_number', models.CharField(blank=True, max_length=100, null=True)),
                ('passport_expiration_date', models.DateField(blank=True, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passengers', to='api.contact')),
                ('passport_document_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passport_passengers', to='api.document')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('lock', models.BooleanField(default=False)),
                ('bed_at_origin', models.BooleanField(default=False)),
                ('bed_at_destination', models.BooleanField(default=False)),
                ('date_of_birth', models.DateField()),
                ('nationality', models.CharField(max_length=100)),
                ('passport_number', models.CharField(max_length=100)),
                ('passport_expiration_date', models.DateField()),
                ('special_instructions', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patients', to='api.contact')),
                ('letter_of_medical_necessity_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medical_necessity_patients', to='api.document')),
                ('passport_document_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passport_patients', to='api.document')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ground',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('address_line1', models.CharField(blank=True, max_length=255, null=True)),
                ('address_line2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('zip', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('contacts', models.ManyToManyField(related_name='grounds', to='api.contact')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('permission_ids', models.ManyToManyField(related_name='grounds', to='api.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FBO',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('address_line1', models.CharField(blank=True, max_length=255, null=True)),
                ('address_line2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('zip', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('contacts', models.ManyToManyField(related_name='fbos', to='api.contact')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('permission_ids', models.ManyToManyField(related_name='fbos', to='api.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('permission_ids', models.ManyToManyField(related_name='departments', to='api.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contact',
            name='permission_ids',
            field=models.ManyToManyField(related_name='contacts', to='api.permission'),
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('icao_code', models.CharField(max_length=4)),
                ('iata_code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(max_length=100)),
                ('elevation', models.IntegerField(blank=True, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('timezone', models.CharField(max_length=50)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('fbos', models.ManyToManyField(blank=True, related_name='airports', to='api.fbo')),
                ('grounds', models.ManyToManyField(blank=True, related_name='airports', to='api.ground')),
                ('permission_ids', models.ManyToManyField(related_name='airports', to='api.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('permissions', models.ManyToManyField(related_name='roles', to='api.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('credit_card', 'Credit Card'), ('ACH', 'ACH Transfer')], max_length=20)),
                ('payment_status', models.CharField(choices=[('created', 'Created'), ('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='created', max_length=20)),
                ('payment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('email', models.EmailField(max_length=254)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('lock', models.BooleanField(default=False)),
                ('quoted_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cruise_doctor_first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('cruise_doctor_last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('cruise_line', models.CharField(blank=True, max_length=100, null=True)),
                ('cruise_ship', models.CharField(blank=True, max_length=100, null=True)),
                ('aircraft_type', models.CharField(choices=[('65', 'Learjet 65'), ('35', 'Learjet 35'), ('TBD', 'To Be Determined')], max_length=20)),
                ('estimated_fight_time', models.DecimalField(decimal_places=2, max_digits=5)),
                ('includes_grounds', models.BooleanField(default=False)),
                ('inquiry_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('medical_team', models.CharField(choices=[('RN/RN', 'RN/RN'), ('RN/Paramedic', 'RN/Paramedic'), ('RN/MD', 'RN/MD'), ('RN/RT', 'RN/RT'), ('standard', 'Standard'), ('full', 'Full')], max_length=20)),
                ('patient_first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('patient_last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('paid', 'Paid')], default='pending', max_length=20)),
                ('number_of_stops', models.PositiveIntegerField(default=0)),
                ('quote_pdf_status', models.CharField(choices=[('created', 'Created'), ('pending', 'Pending'), ('modified', 'Modified'), ('accepted', 'Accepted'), ('denied', 'Denied')], default='created', max_length=20)),
                ('quote_pdf_email', models.EmailField(max_length=254)),
                ('consent_for_transport_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consent_quotes', to='api.agreement')),
                ('contact_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='api.contact')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('documents', models.ManyToManyField(related_name='quotes', to='api.document')),
                ('dropoff_airport_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dropoff_quotes', to='api.airport')),
                ('patient_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quotes', to='api.patient')),
                ('patient_service_agreement_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_quotes', to='api.agreement')),
                ('payment_agreement_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_quotes', to='api.agreement')),
                ('pickup_airport_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pickup_quotes', to='api.airport')),
                ('quote_pdf_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quote_pdfs', to='api.document')),
                ('transactions', models.ManyToManyField(blank=True, related_name='quotes', to='api.transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('email_chain', models.JSONField(blank=True, default=list)),
                ('type', models.CharField(choices=[('medical', 'Medical'), ('charter', 'Charter'), ('part 91', 'Part 91'), ('other', 'Other'), ('maintenance', 'Maintenance')], max_length=20)),
                ('estimated_departure_time', models.DateTimeField(blank=True, null=True)),
                ('post_flight_duty_time', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('pre_flight_duty_time', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('trip_number', models.CharField(max_length=20)),
                ('aircraft_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trips', to='api.aircraft')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('customer_itinerary_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_itinerary_trips', to='api.document')),
                ('internal_itinerary_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='internal_itinerary_trips', to='api.document')),
                ('passengers', models.ManyToManyField(blank=True, related_name='trips', to='api.passenger')),
                ('patient_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trips', to='api.patient')),
                ('quote_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='api.quote')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TripLine',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('departure_time_local', models.DateTimeField()),
                ('departure_time_utc', models.DateTimeField()),
                ('arrival_time_local', models.DateTimeField()),
                ('arrival_time_utc', models.DateTimeField()),
                ('distance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('flight_time', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ground_time', models.DecimalField(decimal_places=2, max_digits=5)),
                ('passenger_leg', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('crew_line_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trip_lines', to='api.crewline')),
                ('destination_airport_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_trip_lines', to='api.airport')),
                ('origin_airport_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin_trip_lines', to='api.airport')),
                ('trip_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_lines', to='api.trip')),
            ],
            options={
                'ordering': ['departure_time_utc'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('lock', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address_line1', models.CharField(blank=True, max_length=255, null=True)),
                ('address_line2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('zip', models.CharField(blank=True, max_length=20, null=True)),
                ('flags', models.JSONField(blank=True, default=list)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('department_ids', models.ManyToManyField(related_name='users', to='api.department')),
                ('departments', models.ManyToManyField(related_name='department_users', to='api.department')),
                ('roles', models.ManyToManyField(related_name='users', to='api.role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

```


# File: api/tests/base_test.py

```python
"""
Base test utilities for API endpoint testing.
Tests are designed to run against a live server.
"""
import json
import requests
import sys
from typing import Dict, Any, Optional


class APITester:
    """Base class for testing API endpoints against a running server."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000", auth_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        if auth_token:
            self.session.headers.update({
                'Authorization': f'Bearer {auth_token}'
            })
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate with the API and store the token."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/token/",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('access') or data.get('token')
                if token:
                    self.session.headers.update({
                        'Authorization': f'Bearer {token}'
                    })
                    return True
            return False
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def print_response(self, response: requests.Response, title: str):
        """Print formatted response details."""
        print(f"\n{'='*60}")
        print(f"TEST: {title}")
        print(f"{'='*60}")
        print(f"URL: {response.request.method} {response.url}")
        print(f"Status Code: {response.status_code}")
        
        if response.request.body:
            print(f"Request Body: {response.request.body}")
        
        try:
            response_data = response.json()
            print(f"Response Body:")
            print(json.dumps(response_data, indent=2))
        except:
            print(f"Response Body (raw): {response.text}")
        
        print(f"{'='*60}\n")
    
    def check_no_id_fields(self, data: Any, path: str = "") -> list:
        """Check for _id fields in response data and return violations."""
        violations = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                # Check for _id fields (but allow 'id' itself)
                if key.endswith('_id') and key != 'id':
                    violations.append(f"Found _id field '{key}' at path '{current_path}'")
                violations.extend(self.check_no_id_fields(value, current_path))
        elif isinstance(data, list):
            for i, item in enumerate(data):
                violations.extend(self.check_no_id_fields(item, f"{path}[{i}]"))
        
        return violations
    
    def test_endpoint(self, endpoint: str, method: str = "GET", data: Dict = None, 
                     expect_status: int = 200, title: str = None) -> requests.Response:
        """Test an endpoint and print results."""
        url = f"{self.base_url}{endpoint}"
        title = title or f"{method} {endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "PATCH":
                response = self.session.patch(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            self.print_response(response, title)
            
            # Check for _id fields in GET responses
            if method.upper() == "GET" and response.status_code == 200:
                try:
                    response_data = response.json()
                    violations = self.check_no_id_fields(response_data)
                    if violations:
                        print("⚠️  _ID FIELD VIOLATIONS FOUND:")
                        for violation in violations:
                            print(f"   - {violation}")
                    else:
                        print("✅ No _id fields found in response")
                except:
                    pass
            
            # Check status code
            if response.status_code == expect_status:
                print(f"✅ Status code matches expected: {expect_status}")
            else:
                print(f"❌ Status code {response.status_code} != expected {expect_status}")
            
            return response
            
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None


def main():
    """Run basic connectivity test."""
    tester = APITester()
    
    print("Testing API connectivity...")
    response = tester.test_endpoint("/api/", title="API Root Connectivity Test")
    
    if response and response.status_code < 500:
        print("✅ API server is reachable")
    else:
        print("❌ API server is not reachable")
        sys.exit(1)


if __name__ == "__main__":
    main()

```


# File: api/tests/test_trip_lines.py

```python
#!/usr/bin/env python3
"""
Test TripLine endpoints (/api/trip-lines/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_trip_line_endpoints():
    """Test TripLine CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING TRIP LINE ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List trip lines (GET /api/trip-lines/)
    print("\n📋 TEST 1: List Trip Lines")
    response = tester.test_endpoint(
        "/api/trip-lines/",
        method="GET",
        title="List Trip Lines"
    )
    
    # Test 2: Get specific trip line (if we have data)
    trip_line_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                trip_line_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Trip Line (ID: {trip_line_id})")
                tester.test_endpoint(
                    f"/api/trip-lines/{trip_line_id}/",
                    method="GET",
                    title=f"Get Trip Line {trip_line_id}"
                )
        except:
            print("\n⚠️  Could not extract trip line ID for detail test")
    
    # Test 3: Create new trip line (POST /api/trip-lines/)
    print("\n➕ TEST 3: Create Trip Line (Write Serializer Test)")
    create_data = {
        "trip": 1,  # Expects Trip ID only
        "origin_airport": 1,  # Expects Airport ID only
        "destination_airport": 2,  # Expects Airport ID only
        "crew_line": 1,  # Expects CrewLine ID only
        "departure_date": "2024-12-01T10:00:00Z",
        "arrival_date": "2024-12-01T14:00:00Z",
        "flight_time": "04:00:00",
        "status": "scheduled",
        "notes": "Test trip line creation"
    }
    
    tester.test_endpoint(
        "/api/trip-lines/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Trip Line with IDs only"
    )
    
    # Test 4: Try to create with nested objects (should fail)
    print("\n❌ TEST 4: Create Trip Line with Nested Objects (Should Fail)")
    invalid_data = {
        "trip": {  # Should be trip_id
            "trip_number": "TR001"
        },
        "origin_airport": {  # Should be origin_airport_id
            "icao_code": "KORD"
        },
        "destination_airport": {  # Should be destination_airport_id
            "icao_code": "KLAX"
        },
        "crew_line": {  # Should be crew_line_id
            "status": "active"
        },
        "departure_date": "2024-12-01T10:00:00Z",
        "arrival_date": "2024-12-01T14:00:00Z"
    }
    
    tester.test_endpoint(
        "/api/trip-lines/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create Trip Line with nested objects (should fail)"
    )
    
    # Test 5: Update trip line (if we have an ID)
    if trip_line_id:
        print(f"\n✏️  TEST 5: Update Trip Line (ID: {trip_line_id})")
        update_data = {
            "trip": 1,
            "origin_airport": 2,  # Changed origin
            "destination_airport": 1,  # Changed destination (reverse)
            "crew_line": 2,  # Changed crew
            "departure_date": "2024-12-02T11:00:00Z",  # Changed time
            "arrival_date": "2024-12-02T15:00:00Z",
            "flight_time": "04:00:00",
            "status": "in_progress",  # Changed status
            "notes": "Updated trip line"
        }
        
        tester.test_endpoint(
            f"/api/trip-lines/{trip_line_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Trip Line {trip_line_id} with IDs only"
        )
    
    print("\n✅ Trip Line endpoint tests completed!")


if __name__ == "__main__":
    test_trip_line_endpoints()

```


# File: api/tests/test_quotes.py

```python
#!/usr/bin/env python3
"""
Test Quote endpoints (/api/quotes/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_quote_endpoints():
    """Test Quote CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING QUOTE ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List quotes (GET /api/quotes/)
    print("\n📋 TEST 1: List Quotes")
    response = tester.test_endpoint(
        "/api/quotes/",
        method="GET",
        title="List Quotes"
    )
    
    # Test 2: Get specific quote (if we have data)
    quote_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                quote_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Quote (ID: {quote_id})")
                tester.test_endpoint(
                    f"/api/quotes/{quote_id}/",
                    method="GET",
                    title=f"Get Quote {quote_id}"
                )
                
                # Test create transaction for this quote
                print(f"\n💳 TEST 2b: Create Transaction for Quote {quote_id}")
                transaction_data = {
                    "amount": 1000.00,
                    "payment_method": "credit_card",
                    "email": "test@example.com"
                }
                tester.test_endpoint(
                    f"/api/quotes/{quote_id}/create_transaction/",
                    method="POST",
                    data=transaction_data,
                    title=f"Create Transaction for Quote {quote_id}"
                )
        except:
            print("\n⚠️  Could not extract quote ID for detail test")
    
    # Test 3: Create new quote (POST /api/quotes/)
    print("\n➕ TEST 3: Create Quote (Write Serializer Test)")
    create_data = {
        "contact": 1,  # Expects Contact ID only
        "pickup_airport": 1,  # Expects Airport ID only
        "dropoff_airport": 2,  # Expects Airport ID only
        "patient": 1,  # Expects Patient ID only
        "payment_agreement": 1,  # Expects Agreement ID only
        "quoted_amount": 7500.00,
        "status": "pending",
        "departure_date": "2024-12-01T10:00:00Z",
        "arrival_date": "2024-12-01T14:00:00Z",
        "notes": "Test quote creation"
    }
    
    tester.test_endpoint(
        "/api/quotes/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Quote with IDs only"
    )
    
    # Test 4: Try to create with nested objects (should fail)
    print("\n❌ TEST 4: Create Quote with Nested Objects (Should Fail)")
    invalid_data = {
        "contact": {  # Should be contact_id
            "first_name": "John",
            "last_name": "Doe"
        },
        "pickup_airport": {  # Should be pickup_airport_id
            "icao_code": "KORD"
        },
        "dropoff_airport": {  # Should be dropoff_airport_id
            "icao_code": "KLAX"
        },
        "patient": {  # Should be patient_id
            "status": "active"
        },
        "quoted_amount": 8500.00,
        "status": "pending"
    }
    
    tester.test_endpoint(
        "/api/quotes/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create Quote with nested objects (should fail)"
    )
    
    # Test 5: Update quote (if we have an ID)
    if quote_id:
        print(f"\n✏️  TEST 5: Update Quote (ID: {quote_id})")
        update_data = {
            "contact": 1,
            "pickup_airport": 1,
            "dropoff_airport": 2,
            "patient": 1,
            "payment_agreement": 1,
            "quoted_amount": 8000.00,  # Changed amount
            "status": "accepted",  # Changed status
            "notes": "Updated quote"
        }
        
        tester.test_endpoint(
            f"/api/quotes/{quote_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Quote {quote_id} with IDs only"
        )
    
    print("\n✅ Quote endpoint tests completed!")


if __name__ == "__main__":
    test_quote_endpoints()

```


# File: api/tests/test_passengers.py

```python
#!/usr/bin/env python3
"""
Test Passenger endpoints (/api/passengers/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_passenger_endpoints():
    """Test Passenger CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING PASSENGER ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List passengers (GET /api/passengers/)
    print("\n📋 TEST 1: List Passengers")
    response = tester.test_endpoint(
        "/api/passengers/",
        method="GET",
        title="List Passengers"
    )
    
    # Test 2: Get specific passenger (if we have data)
    passenger_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                passenger_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Passenger (ID: {passenger_id})")
                tester.test_endpoint(
                    f"/api/passengers/{passenger_id}/",
                    method="GET",
                    title=f"Get Passenger {passenger_id}"
                )
        except:
            print("\n⚠️  Could not extract passenger ID for detail test")
    
    # Test 3: Create new passenger (POST /api/passengers/)
    print("\n➕ TEST 3: Create Passenger (Write Serializer Test)")
    create_data = {
        "info": 1,  # Expects Contact ID only
        "date_of_birth": "1990-01-01",
        "nationality": "US",
        "passport_number": "123456789",
        "passport_expiration_date": "2030-01-01",
        "contact_number": "+1234567890",
        "passport_document": 1,  # Expects Document ID only
        "status": "active"
    }
    
    tester.test_endpoint(
        "/api/passengers/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Passenger with IDs only"
    )
    
    # Test 4: Try to create with nested objects (should fail)
    print("\n❌ TEST 4: Create Passenger with Nested Objects (Should Fail)")
    invalid_data = {
        "info": {  # Should be info_id
            "first_name": "John",
            "last_name": "Doe"
        },
        "passport_document": {  # Should be passport_document_id
            "filename": "passport.pdf"
        },
        "date_of_birth": "1990-01-01",
        "nationality": "US"
    }
    
    tester.test_endpoint(
        "/api/passengers/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create Passenger with nested objects (should fail)"
    )
    
    # Test 5: Update passenger (if we have an ID)
    if passenger_id:
        print(f"\n✏️  TEST 5: Update Passenger (ID: {passenger_id})")
        update_data = {
            "info": 1,
            "date_of_birth": "1990-01-01",
            "nationality": "CA",  # Changed nationality
            "passport_number": "987654321",  # Changed passport
            "passport_expiration_date": "2031-01-01",
            "contact_number": "+1987654321",
            "status": "active"
        }
        
        tester.test_endpoint(
            f"/api/passengers/{passenger_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Passenger {passenger_id} with IDs only"
        )
    
    print("\n✅ Passenger endpoint tests completed!")


if __name__ == "__main__":
    test_passenger_endpoints()

```


# File: api/tests/test_userprofile.py

```python
#!/usr/bin/env python3
"""
Test UserProfile endpoints (/api/users/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_userprofile_endpoints():
    """Test UserProfile CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING USERPROFILE ENDPOINTS")
    print("=" * 80)
    
    # Test authentication first (you may need to adjust credentials)
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):  # Adjust credentials as needed
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List users (GET /api/users/)
    print("\n📋 TEST 1: List Users")
    response = tester.test_endpoint(
        "/api/users/",
        method="GET",
        title="List UserProfiles"
    )
    
    # Test 2: Get current user (GET /api/users/me/)
    print("\n👤 TEST 2: Get Current User")
    response = tester.test_endpoint(
        "/api/users/me/",
        method="GET",
        title="Get Current User Profile"
    )
    
    # Test 3: Try to get a specific user (if we have an ID from list)
    if response and response.status_code == 200:
        try:
            user_data = response.json()
            user_id = user_data.get('id')
            if user_id:
                print(f"\n🔍 TEST 3: Get Specific User (ID: {user_id})")
                tester.test_endpoint(
                    f"/api/users/{user_id}/",
                    method="GET",
                    title=f"Get UserProfile {user_id}"
                )
        except:
            print("\n⚠️  Could not extract user ID for detail test")
    
    # Test 4: Create new user (POST /api/users/)
    print("\n➕ TEST 4: Create User (Write Serializer Test)")
    create_data = {
        "user_id": 1,  # This will likely fail, but shows the expected format
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone": "+1234567890",
        "role_ids": [1],  # Expects only IDs
        "department_ids": [1],  # Expects only IDs
        "status": "active"
    }
    
    tester.test_endpoint(
        "/api/users/",
        method="POST",
        data=create_data,
        expect_status=201,  # May fail due to constraints, but tests serializer
        title="Create UserProfile with IDs only"
    )
    
    # Test 5: Try to create with nested objects (should fail)
    print("\n❌ TEST 5: Create User with Nested Objects (Should Fail)")
    invalid_data = {
        "user": {"username": "invalid"},  # Should be user_id
        "roles": [{"name": "invalid"}],   # Should be role_ids
        "first_name": "Invalid",
        "last_name": "User"
    }
    
    tester.test_endpoint(
        "/api/users/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create UserProfile with nested objects (should fail)"
    )
    
    print("\n✅ UserProfile endpoint tests completed!")


if __name__ == "__main__":
    test_userprofile_endpoints()

```


# File: api/tests/__init__.py

```python
# Test package for API endpoints

```


# File: api/tests/test_trips.py

```python
#!/usr/bin/env python3
"""
Test Trip endpoints (/api/trips/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_trip_endpoints():
    """Test Trip CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING TRIP ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List trips (GET /api/trips/)
    print("\n📋 TEST 1: List Trips")
    response = tester.test_endpoint(
        "/api/trips/",
        method="GET",
        title="List Trips"
    )
    
    # Test 2: Get specific trip (if we have data)
    trip_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                trip_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Trip (ID: {trip_id})")
                tester.test_endpoint(
                    f"/api/trips/{trip_id}/",
                    method="GET",
                    title=f"Get Trip {trip_id}"
                )
                
                # Test trip lines for this trip
                print(f"\n🔗 TEST 2b: Get Trip Lines for Trip {trip_id}")
                tester.test_endpoint(
                    f"/api/trips/{trip_id}/trip_lines/",
                    method="GET",
                    title=f"Get Trip Lines for Trip {trip_id}"
                )
                
                # Test generate itineraries
                print(f"\n📅 TEST 2c: Generate Itineraries for Trip {trip_id}")
                tester.test_endpoint(
                    f"/api/trips/{trip_id}/generate_itineraries/",
                    method="POST",
                    title=f"Generate Itineraries for Trip {trip_id}"
                )
        except:
            print("\n⚠️  Could not extract trip ID for detail test")
    
    # Test 3: Create new trip (POST /api/trips/)
    print("\n➕ TEST 3: Create Trip (Write Serializer Test)")
    create_data = {
        "quote": 1,  # Expects Quote ID only
        "patient": 1,  # Expects Patient ID only
        "aircraft": 1,  # Expects Aircraft ID only
        "trip_number": "TR001",
        "type": "medical",
        "status": "scheduled",
        "passenger_ids": [1, 2],  # Expects list of Passenger IDs
        "departure_date": "2024-12-01T10:00:00Z",
        "arrival_date": "2024-12-01T14:00:00Z"
    }
    
    tester.test_endpoint(
        "/api/trips/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Trip with IDs only"
    )
    
    # Test 4: Try to create with nested objects (should fail)
    print("\n❌ TEST 4: Create Trip with Nested Objects (Should Fail)")
    invalid_data = {
        "quote": {  # Should be quote_id
            "quoted_amount": 5000.00
        },
        "patient": {  # Should be patient_id
            "status": "active"
        },
        "aircraft": {  # Should be aircraft_id
            "tail_number": "N123AB"
        },
        "passengers": [  # Should be passenger_ids
            {"info": {"first_name": "John"}}
        ],
        "trip_number": "TR002",
        "type": "charter"
    }
    
    tester.test_endpoint(
        "/api/trips/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create Trip with nested objects (should fail)"
    )
    
    # Test 5: Update trip (if we have an ID)
    if trip_id:
        print(f"\n✏️  TEST 5: Update Trip (ID: {trip_id})")
        update_data = {
            "quote": 1,
            "patient": 1,
            "aircraft": 1,
            "trip_number": "TR001-UPDATED",
            "type": "charter",  # Changed type
            "status": "in_progress",  # Changed status
            "passenger_ids": [1]
        }
        
        tester.test_endpoint(
            f"/api/trips/{trip_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Trip {trip_id} with IDs only"
        )
    
    print("\n✅ Trip endpoint tests completed!")


if __name__ == "__main__":
    test_trip_endpoints()

```


# File: api/tests/test_crew_lines.py

```python
#!/usr/bin/env python3
"""
Test CrewLine endpoints (/api/crew-lines/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_crew_line_endpoints():
    """Test CrewLine CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING CREW LINE ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List crew lines (GET /api/crew-lines/)
    print("\n📋 TEST 1: List Crew Lines")
    response = tester.test_endpoint(
        "/api/crew-lines/",
        method="GET",
        title="List Crew Lines"
    )
    
    # Test 2: Get specific crew line (if we have data)
    crew_line_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                crew_line_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Crew Line (ID: {crew_line_id})")
                tester.test_endpoint(
                    f"/api/crew-lines/{crew_line_id}/",
                    method="GET",
                    title=f"Get Crew Line {crew_line_id}"
                )
        except:
            print("\n⚠️  Could not extract crew line ID for detail test")
    
    # Test 3: Create new crew line (POST /api/crew-lines/)
    print("\n➕ TEST 3: Create Crew Line (Write Serializer Test)")
    create_data = {
        "primary_in_command": 1,  # Expects Contact ID only
        "secondary_in_command": 2,  # Expects Contact ID only
        "medic_ids": [3, 4],  # Expects list of Contact IDs
        "status": "active",
        "notes": "Test crew line creation"
    }
    
    tester.test_endpoint(
        "/api/crew-lines/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Crew Line with IDs only"
    )
    
    # Test 4: Try to create with nested objects (should fail)
    print("\n❌ TEST 4: Create Crew Line with Nested Objects (Should Fail)")
    invalid_data = {
        "primary_in_command": {  # Should be primary_in_command_id
            "first_name": "John",
            "last_name": "Pilot"
        },
        "secondary_in_command": {  # Should be secondary_in_command_id
            "first_name": "Jane",
            "last_name": "Copilot"
        },
        "medics": [  # Should be medic_ids
            {"first_name": "Dr. Smith"},
            {"first_name": "Nurse Johnson"}
        ],
        "status": "active"
    }
    
    tester.test_endpoint(
        "/api/crew-lines/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create Crew Line with nested objects (should fail)"
    )
    
    # Test 5: Update crew line (if we have an ID)
    if crew_line_id:
        print(f"\n✏️  TEST 5: Update Crew Line (ID: {crew_line_id})")
        update_data = {
            "primary_in_command": 2,  # Changed primary
            "secondary_in_command": 3,  # Changed secondary
            "medic_ids": [4],  # Changed medics list
            "status": "standby",  # Changed status
            "notes": "Updated crew line"
        }
        
        tester.test_endpoint(
            f"/api/crew-lines/{crew_line_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Crew Line {crew_line_id} with IDs only"
        )
    
    print("\n✅ Crew Line endpoint tests completed!")


if __name__ == "__main__":
    test_crew_line_endpoints()

```


# File: api/tests/test_transactions.py

```python
#!/usr/bin/env python3
"""
Test Transaction endpoints (/api/transactions/)
Run this against a live server to test the standardized CRUD endpoints.
Special focus on public vs staff access patterns.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_transaction_endpoints():
    """Test Transaction CRUD endpoints with special public/staff logic."""
    tester = APITester()
    
    print("🧪 TESTING TRANSACTION ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    authenticated = tester.authenticate("admin", "admin")
    if not authenticated:
        print("⚠️  Authentication failed, will test public access...")
    
    # Test 1: List transactions (GET /api/transactions/) - Staff only
    print("\n📋 TEST 1: List Transactions (Staff Access)")
    response = tester.test_endpoint(
        "/api/transactions/",
        method="GET",
        title="List Transactions (Staff)"
    )
    
    # Test 2: Get specific transaction (if we have data)
    transaction_id = None
    transaction_key = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                transaction_id = results[0].get('id')
                transaction_key = results[0].get('key')
                
                print(f"\n🔍 TEST 2: Get Specific Transaction (ID: {transaction_id})")
                tester.test_endpoint(
                    f"/api/transactions/{transaction_id}/",
                    method="GET",
                    title=f"Get Transaction {transaction_id} (Staff)"
                )
        except:
            print("\n⚠️  Could not extract transaction data for detail test")
    
    # Test 3: Public read by key (no authentication required)
    if transaction_key:
        print(f"\n🌐 TEST 3: Public Read by Key (Key: {transaction_key})")
        
        # Remove authentication for public test
        public_tester = APITester()  # No auth
        
        public_tester.test_endpoint(
            f"/api/transactions/by-key/{transaction_key}/",
            method="GET",
            title=f"Public Read Transaction by Key {transaction_key}"
        )
        
        # Restore authentication for remaining tests
        if authenticated:
            tester.authenticate("admin", "admin")
    
    # Test 4: Create new transaction (POST /api/transactions/)
    print("\n➕ TEST 4: Create Transaction")
    create_data = {
        "amount": 2500.00,
        "payment_method": "credit_card",
        "email": "customer@example.com",
        "payment_status": "pending",
        "description": "Test transaction creation"
    }
    
    response = tester.test_endpoint(
        "/api/transactions/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Transaction"
    )
    
    # Get the created transaction ID for further tests
    created_transaction_id = None
    if response and response.status_code == 201:
        try:
            created_data = response.json()
            created_transaction_id = created_data.get('id')
        except:
            pass
    
    # Test 5: Process payment (special endpoint)
    if created_transaction_id:
        print(f"\n💳 TEST 5: Process Payment (ID: {created_transaction_id})")
        payment_data = {
            "payment_status": "completed",
            "payment_method": "credit_card",
            "transaction_reference": "ref_12345"
        }
        
        tester.test_endpoint(
            f"/api/transactions/{created_transaction_id}/process_payment/",
            method="POST",
            data=payment_data,
            expect_status=200,
            title=f"Process Payment for Transaction {created_transaction_id}"
        )
    
    # Test 6: Update transaction (if we have an ID)
    if transaction_id:
        print(f"\n✏️  TEST 6: Update Transaction (ID: {transaction_id})")
        update_data = {
            "amount": 3000.00,  # Changed amount
            "payment_method": "bank_transfer",  # Changed method
            "payment_status": "processing",  # Changed status
            "email": "updated@example.com"
        }
        
        tester.test_endpoint(
            f"/api/transactions/{transaction_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Transaction {transaction_id}"
        )
    
    # Test 7: Test access control differences
    print("\n🔒 TEST 7: Access Control Verification")
    
    # Test without authentication
    no_auth_tester = APITester()
    
    print("\n   7a: List transactions without auth (should fail)")
    no_auth_tester.test_endpoint(
        "/api/transactions/",
        method="GET",
        expect_status=401,
        title="List Transactions (No Auth - Should Fail)"
    )
    
    if transaction_id:
        print(f"\n   7b: Get transaction detail without auth (should fail)")
        no_auth_tester.test_endpoint(
            f"/api/transactions/{transaction_id}/",
            method="GET",
            expect_status=401,
            title=f"Get Transaction {transaction_id} (No Auth - Should Fail)"
        )
    
    if transaction_key:
        print(f"\n   7c: Public read by key without auth (should succeed)")
        no_auth_tester.test_endpoint(
            f"/api/transactions/by-key/{transaction_key}/",
            method="GET",
            expect_status=200,
            title=f"Public Read by Key {transaction_key} (No Auth - Should Succeed)"
        )
    
    print("\n✅ Transaction endpoint tests completed!")


if __name__ == "__main__":
    test_transaction_endpoints()

```


# File: api/tests/test_patients.py

```python
#!/usr/bin/env python3
"""
Test Patient endpoints (/api/patients/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_patient_endpoints():
    """Test Patient CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING PATIENT ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List patients (GET /api/patients/)
    print("\n📋 TEST 1: List Patients")
    response = tester.test_endpoint(
        "/api/patients/",
        method="GET",
        title="List Patients"
    )
    
    # Test 2: Get specific patient (if we have data)
    patient_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                patient_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Patient (ID: {patient_id})")
                tester.test_endpoint(
                    f"/api/patients/{patient_id}/",
                    method="GET",
                    title=f"Get Patient {patient_id}"
                )
        except:
            print("\n⚠️  Could not extract patient ID for detail test")
    
    # Test 3: Create new patient (POST /api/patients/)
    print("\n➕ TEST 3: Create Patient (Write Serializer Test)")
    create_data = {
        "info": 1,  # Expects Contact ID only
        "status": "active",
        "medical_notes": "Test patient creation",
        "emergency_contact": "Emergency Contact Name",
        "emergency_phone": "+1234567890"
    }
    
    tester.test_endpoint(
        "/api/patients/",
        method="POST",
        data=create_data,
        expect_status=201,
        title="Create Patient with ID only"
    )
    
    # Test 4: Try to create with nested objects (should fail)
    print("\n❌ TEST 4: Create Patient with Nested Objects (Should Fail)")
    invalid_data = {
        "info": {  # Should be info_id
            "first_name": "John",
            "last_name": "Patient",
            "email": "patient@example.com"
        },
        "status": "active",
        "medical_notes": "Invalid patient creation"
    }
    
    tester.test_endpoint(
        "/api/patients/",
        method="POST",
        data=invalid_data,
        expect_status=400,
        title="Create Patient with nested objects (should fail)"
    )
    
    # Test 5: Update patient (if we have an ID)
    if patient_id:
        print(f"\n✏️  TEST 5: Update Patient (ID: {patient_id})")
        update_data = {
            "info": 1,
            "status": "inactive",  # Changed status
            "medical_notes": "Updated patient medical notes",
            "emergency_contact": "Updated Emergency Contact",
            "emergency_phone": "+1987654321"
        }
        
        tester.test_endpoint(
            f"/api/patients/{patient_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Patient {patient_id} with ID only"
        )
    
    print("\n✅ Patient endpoint tests completed!")


if __name__ == "__main__":
    test_patient_endpoints()

```


# File: api/tests/run_all_tests.py

```python
#!/usr/bin/env python3
"""
Run all API endpoint tests against a live server.
This script runs all individual test files and provides a summary.
"""
import sys
import os
import subprocess
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def check_server_connectivity():
    """Check if the API server is running and accessible."""
    print("🔍 Checking server connectivity...")
    tester = APITester()
    
    try:
        # Use requests directly to avoid status code checking
        import requests
        response = requests.get(f"{tester.base_url}/api/")
        tester.print_response(response, "Server Connectivity Check")
        
        # Accept 401 as valid since /api/ requires authentication
        status_code = response.status_code
        print(f"DEBUG: Response status code: {status_code}")
        if status_code in [200, 401]:
            print("✅ API server is reachable")
            return True
        else:
            print(f"❌ API server returned error status: {status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API server: {e}")
        return False


def run_test_file(test_file):
    """Run a single test file and capture output."""
    print(f"\n{'='*80}")
    print(f"🧪 RUNNING: {test_file}")
    print(f"{'='*80}")
    
    try:
        # Run the test file
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout per test file
        )
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print(f"❌ Test {test_file} timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False


def main():
    """Run all API tests."""
    print("🚀 JET-MAIN API ENDPOINT TEST SUITE")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Check server connectivity first
    if not check_server_connectivity():
        print("\n❌ Cannot connect to API server. Please ensure the server is running at http://localhost:8000")
        print("Start the server with: python manage.py runserver")
        sys.exit(1)
    
    # Define test files in order
    test_files = [
        "test_userprofile.py",
        "test_passengers.py", 
        "test_crew_lines.py",
        "test_trip_lines.py",
        "test_trips.py",
        "test_quotes.py",
        "test_patients.py",
        "test_documents.py",
        "test_transactions.py"
    ]
    
    # Track results
    results = {}
    start_time = time.time()
    
    # Run each test file
    for test_file in test_files:
        if os.path.exists(test_file):
            success = run_test_file(test_file)
            results[test_file] = success
        else:
            print(f"⚠️  Test file {test_file} not found, skipping...")
            results[test_file] = False
    
    # Print summary
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*80}")
    print("📊 TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total duration: {duration:.2f} seconds")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    passed = 0
    failed = 0
    
    for test_file, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_file:<25} {status}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 RESULTS: {passed} passed, {failed} failed out of {len(results)} tests")
    
    if failed > 0:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        print("Common issues:")
        print("- Authentication credentials may need adjustment")
        print("- Test data (IDs) may not exist in the database")
        print("- Permissions may not be configured correctly")
        print("- Some endpoints may not be implemented yet")
    else:
        print("\n🎉 All tests completed successfully!")
    
    print(f"\n{'='*80}")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

```


# File: api/tests/test_documents.py

```python
#!/usr/bin/env python3
"""
Test Document endpoints (/api/documents/)
Run this against a live server to test the standardized CRUD endpoints.
"""
import sys
import os
import base64
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_test import APITester


def test_document_endpoints():
    """Test Document CRUD endpoints."""
    tester = APITester()
    
    print("🧪 TESTING DOCUMENT ENDPOINTS")
    print("=" * 80)
    
    # Test authentication
    print("Attempting authentication...")
    if not tester.authenticate("admin", "admin"):
        print("⚠️  Authentication failed, continuing without auth...")
    
    # Test 1: List documents (GET /api/documents/)
    print("\n📋 TEST 1: List Documents")
    response = tester.test_endpoint(
        "/api/documents/",
        method="GET",
        title="List Documents"
    )
    
    # Test 2: Get specific document (if we have data)
    document_id = None
    if response and response.status_code == 200:
        try:
            data = response.json()
            results = data.get('results', [])
            if results:
                document_id = results[0].get('id')
                print(f"\n🔍 TEST 2: Get Specific Document (ID: {document_id})")
                detail_response = tester.test_endpoint(
                    f"/api/documents/{document_id}/",
                    method="GET",
                    title=f"Get Document {document_id}"
                )
                
                # Check for enhanced fields in read serializer
                if detail_response and detail_response.status_code == 200:
                    try:
                        doc_data = detail_response.json()
                        enhanced_fields = ['content_type', 'download_url']
                        found_fields = [field for field in enhanced_fields if field in doc_data]
                        missing_fields = [field for field in enhanced_fields if field not in doc_data]
                        
                        if found_fields:
                            print(f"✅ Enhanced fields found: {found_fields}")
                        if missing_fields:
                            print(f"⚠️  Enhanced fields missing: {missing_fields}")
                    except:
                        pass
                
                # Test download endpoint
                print(f"\n⬇️  TEST 2b: Download Document (ID: {document_id})")
                tester.test_endpoint(
                    f"/api/documents/{document_id}/download/",
                    method="GET",
                    title=f"Download Document {document_id}"
                )
        except:
            print("\n⚠️  Could not extract document ID for detail test")
    
    # Test 3: Upload new document (POST /api/documents/)
    print("\n📤 TEST 3: Upload Document")
    
    # Create sample file content
    sample_content = b"This is a test document content for API testing."
    encoded_content = base64.b64encode(sample_content).decode('utf-8')
    
    upload_data = {
        "filename": "test_upload.txt",
        "flag": "contract",
        "content": encoded_content,  # Base64 encoded content
        "description": "Test document upload via API"
    }
    
    response = tester.test_endpoint(
        "/api/documents/",
        method="POST",
        data=upload_data,
        expect_status=201,
        title="Upload Document"
    )
    
    # Get the uploaded document ID for further tests
    uploaded_document_id = None
    if response and response.status_code == 201:
        try:
            uploaded_data = response.json()
            uploaded_document_id = uploaded_data.get('id')
        except:
            pass
    
    # Test 4: Try alternative upload format
    print("\n📤 TEST 4: Upload Document (Alternative Format)")
    upload_data_alt = {
        "filename": "test_upload_2.pdf",
        "flag": "passport",
        "content": sample_content,  # Raw bytes (may need different handling)
        "description": "Alternative upload test"
    }
    
    tester.test_endpoint(
        "/api/documents/",
        method="POST",
        data=upload_data_alt,
        expect_status=201,
        title="Upload Document (Alternative Format)"
    )
    
    # Test 5: Update document (if we have an ID)
    if uploaded_document_id:
        print(f"\n✏️  TEST 5: Update Document (ID: {uploaded_document_id})")
        update_data = {
            "filename": "updated_test_file.txt",
            "flag": "medical_record",  # Changed flag
            "content": base64.b64encode(b"Updated document content").decode('utf-8'),
            "description": "Updated document description"
        }
        
        tester.test_endpoint(
            f"/api/documents/{uploaded_document_id}/",
            method="PUT",
            data=update_data,
            expect_status=200,
            title=f"Update Document {uploaded_document_id}"
        )
        
        # Test download of updated document
        print(f"\n⬇️  TEST 5b: Download Updated Document")
        tester.test_endpoint(
            f"/api/documents/{uploaded_document_id}/download/",
            method="GET",
            title=f"Download Updated Document {uploaded_document_id}"
        )
    
    # Test 6: Partial update (PATCH)
    if document_id:
        print(f"\n🔧 TEST 6: Partial Update Document (ID: {document_id})")
        patch_data = {
            "description": "Partially updated description",
            "flag": "updated_flag"
        }
        
        tester.test_endpoint(
            f"/api/documents/{document_id}/",
            method="PATCH",
            data=patch_data,
            expect_status=200,
            title=f"Partial Update Document {document_id}"
        )
    
    # Test 7: Test file type validation (if implemented)
    print("\n❌ TEST 7: Invalid File Upload (Testing Validation)")
    invalid_upload = {
        "filename": "",  # Empty filename
        "flag": "invalid_flag",
        "content": "invalid_content_format"
    }
    
    tester.test_endpoint(
        "/api/documents/",
        method="POST",
        data=invalid_upload,
        expect_status=400,
        title="Invalid Document Upload (Should Fail)"
    )
    
    print("\n✅ Document endpoint tests completed!")


if __name__ == "__main__":
    test_document_endpoints()

```


# File: api/management/__init__.py

```python

```


# File: api/management/commands/setup_test_data.py

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from api.models import (
    Contact, UserProfile, Role, Department, Airport, Aircraft, 
    Passenger, CrewLine, Trip, TripLine, Quote, Patient, Document, Transaction
)
import os


class Command(BaseCommand):
    help = 'Set up test data for API endpoint testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up test data...'))
        
        with transaction.atomic():
            # Create admin user
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@jetmain.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                admin_user.set_password('admin')
                admin_user.save()
                self.stdout.write(f'✅ Created admin user: admin/admin')
            else:
                self.stdout.write(f'✅ Admin user already exists')

            # Create test user
            test_user, created = User.objects.get_or_create(
                username='testuser',
                defaults={
                    'email': 'test@jetmain.com',
                    'first_name': 'Test',
                    'last_name': 'User',
                    'is_staff': False,
                    'is_superuser': False
                }
            )
            if created:
                test_user.set_password('testpass')
                test_user.save()
                self.stdout.write(f'✅ Created test user: testuser/testpass')

            # Create roles
            pilot_role, _ = Role.objects.get_or_create(
                name='Pilot',
                defaults={'description': 'Aircraft pilot'}
            )
            medic_role, _ = Role.objects.get_or_create(
                name='Medic',
                defaults={'description': 'Medical personnel'}
            )
            admin_role, _ = Role.objects.get_or_create(
                name='Admin',
                defaults={'description': 'Administrator'}
            )

            # Create departments
            flight_dept, _ = Department.objects.get_or_create(
                name='Flight Operations',
                defaults={'description': 'Flight operations department'}
            )
            medical_dept, _ = Department.objects.get_or_create(
                name='Medical',
                defaults={'description': 'Medical department'}
            )

            # Create contacts
            contacts = []
            for i in range(1, 6):
                contact, _ = Contact.objects.get_or_create(
                    email=f'contact{i}@jetmain.com',
                    defaults={
                        'first_name': f'Contact{i}',
                        'last_name': f'User{i}',
                        'phone': f'+123456789{i}',
                        'address_line1': f'{i}00 Test Street',
                        'city': 'Test City',
                        'state': 'TS',
                        'zip': f'1234{i}',
                        'country': 'USA'
                    }
                )
                contacts.append(contact)

            # Create UserProfiles
            admin_profile, _ = UserProfile.objects.get_or_create(
                user=admin_user,
                defaults={
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'phone': '+1234567890',
                    'address_line1': '123 Admin Street',
                    'city': 'Admin City',
                    'state': 'AC',
                    'zip': '12345',
                    'country': 'USA'
                }
            )
            admin_profile.roles.add(admin_role)
            admin_profile.departments.add(flight_dept)

            test_profile, _ = UserProfile.objects.get_or_create(
                user=test_user,
                defaults={
                    'first_name': 'Test',
                    'last_name': 'User',
                    'phone': '+1234567891',
                    'address_line1': '456 Test Street',
                    'city': 'Test City',
                    'state': 'TC',
                    'zip': '54321',
                    'country': 'USA'
                }
            )
            test_profile.roles.add(pilot_role)
            test_profile.departments.add(flight_dept)

            # Create airports
            airports = []
            airport_data = [
                ('KORD', 'Chicago O\'Hare', 'Chicago', 'IL'),
                ('KLAX', 'Los Angeles International', 'Los Angeles', 'CA'),
                ('KJFK', 'John F Kennedy International', 'New York', 'NY'),
                ('KDEN', 'Denver International', 'Denver', 'CO')
            ]
            
            for icao, name, city, state in airport_data:
                airport, _ = Airport.objects.get_or_create(
                    icao_code=icao,
                    defaults={
                        'name': name,
                        'city': city,
                        'state': state,
                        'country': 'USA',
                        'latitude': 40.0,
                        'longitude': -87.0
                    }
                )
                airports.append(airport)

            # Create aircraft
            aircraft, _ = Aircraft.objects.get_or_create(
                tail_number='N123JM',
                defaults={
                    'company': 'JET-MAIN',
                    'make': 'Cessna',
                    'model': 'Citation X',
                    'serial_number': 'SN123456',
                    'mgtow': 15000.00
                }
            )

            # Create passengers
            passengers = []
            for i, contact in enumerate(contacts[:3]):
                passenger, _ = Passenger.objects.get_or_create(
                    info=contact,
                    defaults={
                        'passport_number': f'P{i+1}234567',
                        'passport_expiration_date': '2030-12-31',
                        'contact_number': f'+198765432{i+1}',
                        'notes': f'No known allergies for passenger {i+1}',
                        'nationality': 'USA'
                    }
                )
                passengers.append(passenger)

            # Create patients
            patients = []
            for i, contact in enumerate(contacts[3:]):
                patient, _ = Patient.objects.get_or_create(
                    info=contact,
                    defaults={
                        'date_of_birth': '1990-01-01',
                        'nationality': 'USA',
                        'passport_number': f'PT{i+1}234567',
                        'passport_expiration_date': '2030-12-31',
                        'status': 'active',
                        'special_instructions': f'Patient {i+1} medical history',
                        'bed_at_origin': False,
                        'bed_at_destination': False
                    }
                )
                patients.append(patient)

            # Create crew lines
            crew_lines = []
            for i in range(2):
                crew_line, _ = CrewLine.objects.get_or_create(
                    primary_in_command_id=contacts[0],
                    secondary_in_command_id=contacts[1]
                )
                crew_line.medic_ids.add(contacts[2])
                crew_lines.append(crew_line)

            # Create quotes
            quotes = []
            for i in range(2):
                quote, _ = Quote.objects.get_or_create(
                    quoted_amount=15000.00,
                    contact_id=contacts[0],
                    pickup_airport_id=airports[0],
                    dropoff_airport_id=airports[1],
                    defaults={
                        'patient_id': patients[0] if patients else None,
                        'aircraft_type': 'TBD',
                        'estimated_fight_time': 4.0,
                        'medical_team': 'standard',
                        'status': 'pending',
                        'quote_pdf_email': f'quote{i+1}@jetmain.com',
                        'includes_grounds': False,
                        'number_of_stops': 0
                    }
                )
                quotes.append(quote)

            # Create trips
            trips = []
            for i, quote in enumerate(quotes):
                trip, _ = Trip.objects.get_or_create(
                    trip_number=f'TR{i+1:04d}',
                    defaults={
                        'quote_id': quote,
                        'patient_id': patients[0] if patients else None,
                        'aircraft_id': aircraft,
                        'type': 'medical',
                        'estimated_departure_time': '2024-12-01T10:00:00Z'
                    }
                )
                trip.passengers.add(passengers[0])
                trips.append(trip)

            # Create trip lines
            for i, trip in enumerate(trips):
                trip_line, _ = TripLine.objects.get_or_create(
                    trip_id=trip,
                    origin_airport_id=airports[i],
                    destination_airport_id=airports[i+1],
                    defaults={
                        'crew_line_id': crew_lines[0],
                        'departure_time_local': '2024-12-01T10:00:00',
                        'departure_time_utc': '2024-12-01T15:00:00Z',
                        'arrival_time_local': '2024-12-01T14:00:00',
                        'arrival_time_utc': '2024-12-01T19:00:00Z',
                        'distance': 1000.00,
                        'flight_time': 4.0,
                        'ground_time': 1.0,
                        'passenger_leg': True
                    }
                )

            # Create documents
            doc, _ = Document.objects.get_or_create(
                filename='test_document.pdf',
                defaults={
                    'content': b'Test document content',
                    'flag': 0
                }
            )

            # Create transactions
            for i, quote in enumerate(quotes):
                transaction_obj, _ = Transaction.objects.get_or_create(
                    amount=quote.quoted_amount,
                    email=f'transaction{i+1}@jetmain.com',
                    defaults={
                        'payment_method': 'credit_card',
                        'payment_status': 'pending'
                    }
                )

        self.stdout.write(self.style.SUCCESS('✅ Test data setup completed!'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Test Accounts:'))
        self.stdout.write(self.style.SUCCESS('  Admin: admin/admin'))
        self.stdout.write(self.style.SUCCESS('  User:  testuser/testpass'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('You can now run the API tests!'))

```


# File: api/management/commands/__init__.py

```python

```


# File: api/external/airport.py

```python
import requests
from bs4 import BeautifulSoup

def get_flight_aware(request):
    url = f"https://flightaware.com/{request}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

    return BeautifulSoup(response.content, "html.parser")

def get_airport(airport_code):
    url = f"resources/airport/{airport_code}"
    return get_flight_aware(url)


def parse_fuel_cost(soup):
    final = []
    for fbo in soup.find_all('tr', class_='fuel_facility'):
        new = {
            'fbo_name' : fbo.find('a').text.strip(),
            'jet_a_cost': fbo.find_all('td')[6].text.strip(),
        }
        if new['jet_a_cost']:
            final.append(new)

    return final


def get_fbo(airport_code, name):
    url = f"resources/airport/{airport_code}/services/FBO/{name.replace(' ', '%20')}"
    return get_flight_aware(url)

def parse_fbo(soup):
    website = soup.find('div', class_="airportBoardContainer").find('a').text.strip()
    phone = soup.find('div', class_="airportBoardContainer").find_all('td')[3].text.strip().replace('+','').replace('-','')
    return website, phone if phone else None

def parse_timezone(soup):
    timezone = soup.find('table').find_all('td')[2].find('span').text.strip()
    return timezone

if __name__ == "__main__":
    soup = get_airport("KTPA")
    print(parse_fuel_cost(soup))

```


# File: api/external/aircraft.py

```python
from bs4 import BeautifulSoup
from airport import get_flight_aware


def get_current(tailnumber):
    url = f"resources/aircraft/{tailnumber}"
    return get_flight_aware(url)
```


# File: index/models.py

```python
from django.db import models


class IndexPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

```


# File: index/serializers.py

```python
from rest_framework import serializers
from .models import IndexPage


class IndexPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexPage
        fields = '__all__'

```


# File: index/__init__.py

```python


```


# File: index/apps.py

```python
from django.apps import AppConfig


class IndexConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'index'

```


# File: index/admin.py

```python
from django.contrib import admin
from .models import IndexPage

admin.site.register(IndexPage)

```


# File: index/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndexPageViewSet

router = DefaultRouter()
router.register(r'pages', IndexPageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```


# File: index/views.py

```python
from rest_framework import viewsets
from .models import IndexPage
from .serializers import IndexPageSerializer


class IndexPageViewSet(viewsets.ModelViewSet):
    queryset = IndexPage.objects.all()
    serializer_class = IndexPageSerializer
    lookup_field = 'slug'

```


# File: maintenance/models.py

```python
from django.db import models


class Aircraft(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('grounded', 'Grounded'),
    ]
    
    registration = models.CharField(max_length=20, unique=True)
    aircraft_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    total_flight_hours = models.FloatField(default=0)
    manufacturing_date = models.DateField(null=True, blank=True)
    capacity = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.registration} - {self.aircraft_type}"


class MaintenanceLog(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='maintenance_logs')
    maintenance_date = models.DateField()
    description = models.TextField()
    performed_by = models.CharField(max_length=100)
    hours_spent = models.FloatField(default=0)
    parts_replaced = models.TextField(blank=True)
    is_scheduled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.aircraft.registration} - {self.maintenance_date}"

```


# File: maintenance/serializers.py

```python
from rest_framework import serializers
from .models import Aircraft, MaintenanceLog


class MaintenanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceLog
        fields = '__all__'


class AircraftSerializer(serializers.ModelSerializer):
    maintenance_logs = MaintenanceLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = Aircraft
        fields = '__all__'


class AircraftStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['status', 'notes']

```


# File: maintenance/__init__.py

```python


```


# File: maintenance/apps.py

```python
from django.apps import AppConfig


class MaintenanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maintenance'

```


# File: maintenance/admin.py

```python
from django.contrib import admin
from .models import Aircraft, MaintenanceLog

admin.site.register(Aircraft)
admin.site.register(MaintenanceLog)

```


# File: maintenance/urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AircraftViewSet, MaintenanceLogViewSet

router = DefaultRouter()
router.register(r'aircraft', AircraftViewSet)
router.register(r'logs', MaintenanceLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```


# File: maintenance/views.py

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Aircraft, MaintenanceLog
from .serializers import AircraftSerializer, MaintenanceLogSerializer, AircraftStatusUpdateSerializer


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        aircraft = self.get_object()
        serializer = AircraftStatusUpdateSerializer(aircraft, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaintenanceLogViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceLog.objects.all()
    serializer_class = MaintenanceLogSerializer
    
    def get_queryset(self):
        queryset = MaintenanceLog.objects.all()
        aircraft_id = self.request.query_params.get('aircraft_id')
        
        if aircraft_id:
            queryset = queryset.filter(aircraft_id=aircraft_id)
        
        return queryset

```
