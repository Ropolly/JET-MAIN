# Project Structure

The following is the structure of the project:

```
backend/
    prompt2.py
    csv processor.py
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
    contact_service.py
    admin.py
    permissions.py
    tests.py
    urls.py
    views.py
    migrations/
        0006_alter_airport_iata_code_alter_airport_icao_code.py
        0005_airport_airport_type.py
        0010_tripevent.py
        0004_rename_country_airport_iso_country_and_more.py
        0008_fbo_phone_fbo_phone_secondary.py
        __init__.py
        0003_staff_staffrole_staffrolemembership_and_more.py
        0009_fbo_email.py
        0002_trip_notes.py
        0007_contact_date_of_birth_contact_nationality_and_more.py
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
            import_airports.py
            seed_staff.py
            setup_test_data.py
            __init__.py
            seed_aircraft_and_staff.py
            seed_fbos.py
            seed_dev.py
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


# File: csv processor.py

```python
import pandas as pd
import re

# Regex pattern to detect phone-like strings
phone_pattern = re.compile(
    r'(\(?\+?\d{1,3}\)?[\s.-]?\d{2,4}[\s.-]?\d{2,4}[\s.-]?\d{2,6})'
)

def extract_numbers(text):
    """Find all phone-like numbers in a text field."""
    if pd.isna(text):
        return []
    return phone_pattern.findall(str(text))

def process_row(row):
    numbers = []

    # Collect numbers from PHONE column
    numbers.extend(extract_numbers(row['PHONE']))

    # Collect numbers from Email column (sometimes contains numbers)
    numbers.extend(extract_numbers(row['Email']))

    # Deduplicate and keep order
    numbers = list(dict.fromkeys(numbers))

    # Assign cleaned numbers back
    row['PHONE'] = numbers[0] if numbers else ''
    row['PHONE2'] = numbers[1] if len(numbers) > 1 else ''

    # If email was a phone number, clear it
    if extract_numbers(row['Email']):
        row['Email'] = ''

    return row

def clean_csv(input_file, output_file):
    df = pd.read_csv(input_file, dtype=str)

    if 'PHONE2' not in df.columns:
        df['PHONE2'] = ''

    df = df.apply(process_row, axis=1)

    df.to_csv(output_file, index=False)
    print(f"Cleaned CSV written to {output_file}")

if __name__ == "__main__":
    clean_csv("FBO.csv", "FBO_clean.csv")

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
import os

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
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "airmed"),
        "USER": os.environ.get("POSTGRES_USER", "airmed"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "airmedpass"),
        # If Django is running on your Mac (outside Docker), use localhost:
        "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
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
    nationality = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiration_date = models.DateField(blank=True, null=True)

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
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_secondary = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
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


class AirportType(models.TextChoices):
    LARGE = 'large_airport', 'Large airport'
    MEDIUM = 'medium_airport', 'Medium airport'
    SMALL = 'small_airport', 'Small airport'


# Airport model
class Airport(BaseModel):
    ident = models.CharField(max_length=10, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    elevation = models.IntegerField(blank=True, null=True)
    iso_country = models.CharField(max_length=100)
    iso_region = models.CharField(max_length=100, blank=True, null=True)
    municipality = models.CharField(max_length=100, blank=True, null=True)
    icao_code = models.CharField(max_length=4, unique=True, db_index=True, blank=True, null=True)
    iata_code = models.CharField(max_length=3, db_index=True, blank=True, null=True)
    local_code = models.CharField(max_length=10, blank=True, null=True)
    gps_code = models.CharField(max_length=20, blank=True, null=True)
    airport_type = models.CharField(
        max_length=20,
        choices=AirportType.choices,
        default=AirportType.SMALL,
        db_index=True,
    )
    fbos = models.ManyToManyField(FBO, related_name="airports", blank=True)
    grounds = models.ManyToManyField(Ground, related_name="airports", blank=True)

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
    notes = models.TextField(blank=True, null=True)

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


class Staff(BaseModel):
    contact = models.OneToOneField("api.Contact", on_delete=models.CASCADE, related_name="staff")
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.contact.first_name} {self.contact.last_name}".strip() or str(self.contact_id)


class StaffRole(BaseModel):
    code = models.CharField(max_length=32, unique=True)   # e.g., 'PIC', 'SIC', 'RN', 'PARAMEDIC'
    name = models.CharField(max_length=64)                # e.g., 'Pilot in Command'

    class Meta:
        indexes = [models.Index(fields=["code"])]

    def __str__(self):
        return self.code


class StaffRoleMembership(BaseModel):
    staff = models.ForeignKey("api.Staff", on_delete=models.CASCADE, related_name="role_memberships")
    role = models.ForeignKey("api.StaffRole", on_delete=models.PROTECT, related_name="memberships")
    start_on = models.DateField(null=True, blank=True)
    end_on = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["staff", "role", "start_on", "end_on"],
                name="uniq_staff_role_interval"
            )
        ]


class TripEvent(BaseModel):
    """
    Non-flight timeline items attached to a Trip.
    """
    EVENT_TYPES = [
        ("CREW_CHANGE", "Crew Change"),
        ("OVERNIGHT", "Overnight (New Day)"),
    ]

    trip_id = models.ForeignKey("api.Trip", on_delete=models.CASCADE, related_name="events")
    airport_id = models.ForeignKey("api.Airport", on_delete=models.PROTECT, related_name="trip_events")

    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)

    # Start/end timestamps (UTC + local) so you can group by day and show durations
    start_time_local = models.DateTimeField()
    start_time_utc = models.DateTimeField()
    end_time_local = models.DateTimeField(blank=True, null=True)  # required for OVERNIGHT
    end_time_utc = models.DateTimeField(blank=True, null=True)

    # Only used for CREW_CHANGE
    crew_line_id = models.ForeignKey(
        "api.CrewLine", on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_events"
    )

    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["trip_id", "start_time_utc"]),
            models.Index(fields=["event_type"]),
        ]

```


# File: api/serializers.py

```python
from rest_framework import serializers
from .models import (
    Modification, Permission, Role, Department, UserProfile, Contact, 
    FBO, Ground, Airport, Document, Aircraft, Transaction, Agreement,
    Patient, Quote, Passenger, CrewLine, Trip, TripLine, Staff, StaffRole,
    StaffRoleMembership, Contact, TripEvent
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
    contact_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'business_name', 'email', 'phone', 
                 'address_line1', 'address_line2', 'city', 'state', 'zip', 'country',
                 'nationality', 'date_of_birth', 'passport_number', 'passport_expiration_date',
                 'contact_type', 'created_on', 'created_by', 'modified_on', 'modified_by']
    
    def get_contact_type(self, obj):
        """
        Determine contact type based on related objects
        """
        # Check if this contact is a patient
        if hasattr(obj, 'patients') and obj.patients.exists():
            return 'Patient'
        
        # Check if this contact is staff
        if hasattr(obj, 'staff'):
            try:
                staff = obj.staff
                # Check staff role memberships to determine if pilot or medic
                role_codes = staff.role_memberships.filter(
                    end_on__isnull=True  # Active memberships only
                ).values_list('role__code', flat=True)
                
                if 'PIC' in role_codes or 'SIC' in role_codes:
                    return 'Staff - Pilot'
                elif 'RN' in role_codes or 'PARAMEDIC' in role_codes:
                    return 'Staff - Medic'
                else:
                    return 'Staff'
            except:
                return 'Staff'
        
        # Check if this contact is a passenger
        if hasattr(obj, 'passengers') and obj.passengers.exists():
            return 'Passenger'
        
        # Check if this contact is a customer (has quotes)
        if hasattr(obj, 'quotes') and obj.quotes.exists():
            return 'Customer'
        
        # Default type
        return 'General'

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
    fbos_count = serializers.SerializerMethodField()
    grounds_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Airport
        fields = ['id', 'ident', 'name', 'latitude', 'longitude', 'elevation', 
                 'iso_country', 'iso_region', 'municipality', 'icao_code', 'iata_code', 
                 'local_code', 'gps_code', 'airport_type', 'timezone', 
                 'fbos', 'grounds', 'fbos_count', 'grounds_count',
                 'created_on', 'created_by', 'modified_on', 'modified_by']
    
    def get_fbos_count(self, obj):
        return obj.fbos.count()
    
    def get_grounds_count(self, obj):
        return obj.grounds.count()

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
    
    def create(self, validated_data):
        # Get contact data for filling deprecated fields
        contact = validated_data['info']
        passenger_ids = validated_data.pop('passenger_ids', [])
        
        # Use contact data as primary source, fallback to provided data
        validated_data['date_of_birth'] = contact.date_of_birth or validated_data.get('date_of_birth')
        validated_data['nationality'] = contact.nationality or validated_data.get('nationality', '')
        validated_data['passport_number'] = contact.passport_number or validated_data.get('passport_number', '')
        validated_data['passport_expiration_date'] = contact.passport_expiration_date or validated_data.get('passport_expiration_date')
        
        passenger = super().create(validated_data)
        
        # Set related passengers if provided
        if passenger_ids:
            passenger.passenger_ids.set(passenger_ids)
        
        return passenger

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
        queryset=Contact.objects.all(), many=True, write_only=True
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
    trip = TripMiniSerializer(read_only=True)
    origin_airport = AirportSerializer(read_only=True)
    destination_airport = AirportSerializer(read_only=True)
    crew_line = CrewLineReadSerializer(read_only=True)
    
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
            'id', 'email_chain', 'quote', 'type', 'patient', 'estimated_departure_time',
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
            'transactions', 'status', 'quote_pdf_status', 'aircraft_type', 'medical_team',
            'created_on'
        ]
    
    def get_patient(self, obj):
        if obj.patient:
            patient_data = {
                'id': obj.patient.id,
                'status': obj.patient.status
            }
            # Include patient's contact info (name)
            if obj.patient.info:
                patient_data['info'] = {
                    'id': obj.patient.info.id,
                    'first_name': obj.patient.info.first_name,
                    'last_name': obj.patient.info.last_name,
                    'email': obj.patient.info.email
                }
            return patient_data
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
            'patient', 'aircraft_type', 'medical_team', 'estimated_flight_time',
            'number_of_stops', 'includes_grounds', 'cruise_line', 'cruise_ship',
            'cruise_doctor_first_name', 'cruise_doctor_last_name', 'quote_pdf_email',
            'payment_agreement', 'consent_for_transport', 'patient_service_agreement', 
            'transaction_ids', 'status'
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
        fields = [
            'id', 
            'info', 
            'date_of_birth', 
            'nationality', 
            'passport_number', 
            'passport_expiration_date', 
            'special_instructions', 
            'status', 
            'bed_at_origin', 
            'bed_at_destination', 
            'created_on'
        ]

class PatientWriteSerializer(serializers.ModelSerializer):
    info = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    
    class Meta:
        model = Patient
        fields = [
            'info', 
            'date_of_birth', 
            'nationality', 
            'passport_number', 
            'passport_expiration_date', 
            'special_instructions', 
            'status', 
            'bed_at_origin', 
            'bed_at_destination'
        ]
    
    def create(self, validated_data):
        # Get contact data for filling deprecated fields
        contact = validated_data['info']
        
        # Use contact data as primary source, fallback to provided data
        validated_data['date_of_birth'] = contact.date_of_birth or validated_data.get('date_of_birth')
        validated_data['nationality'] = contact.nationality or validated_data.get('nationality', '')
        validated_data['passport_number'] = contact.passport_number or validated_data.get('passport_number', '')
        validated_data['passport_expiration_date'] = contact.passport_expiration_date or validated_data.get('passport_expiration_date')
        
        return super().create(validated_data)


class StaffWriteSerializer(serializers.ModelSerializer):
    # Accept a Contact id on write
    contact_id = serializers.PrimaryKeyRelatedField(
        source="contact", queryset=Contact.objects.all()
    )

    class Meta:
        model = Staff
        fields = ("id", "contact_id", "active", "notes")

    def validate_contact_id(self, contact: Contact):
        # Friendly error if a Staff already exists for the Contact (OneToOne is also enforced by DB)
        if self.instance is None and Staff.objects.filter(contact=contact).exists():
            raise serializers.ValidationError("Staff for this contact already exists.")
        return contact


# --- StaffRole ---

class StaffRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRole
        fields = ("id", "code", "name", "created_on")


# --- StaffRoleMembership ---

class StaffRoleMembershipWriteSerializer(serializers.ModelSerializer):
    staff_id = serializers.PrimaryKeyRelatedField(
        source="staff", queryset=Staff.objects.all()
    )
    role_id = serializers.PrimaryKeyRelatedField(
        source="role", queryset=StaffRole.objects.all()
    )

    class Meta:
        model = StaffRoleMembership
        fields = ("id", "staff_id", "role_id", "start_on", "end_on")

    def validate(self, attrs):
        start_on = attrs.get("start_on")
        end_on = attrs.get("end_on")
        if start_on and end_on and end_on < start_on:
            raise serializers.ValidationError({"end_on": "end_on cannot be before start_on"})
        return attrs


class StaffRoleMembershipReadSerializer(serializers.ModelSerializer):
    staff_id = serializers.PrimaryKeyRelatedField(source="staff", read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(source="role", read_only=True)
    role = StaffRoleSerializer(read_only=True)

    class Meta:
        model = StaffRoleMembership
        fields = ("id", "staff_id", "role_id", "role", "start_on", "end_on", "created_on")


class StaffReadSerializer(serializers.ModelSerializer):
    # Return the FK as an id to stay consistent with your API style
    contact_id = serializers.PrimaryKeyRelatedField(source="contact", read_only=True)
    # Include full contact information for display purposes
    contact = ContactSerializer(read_only=True)
    # Include role memberships for display purposes
    role_memberships = StaffRoleMembershipReadSerializer(many=True, read_only=True)

    class Meta:
        model = Staff
        fields = ("id", "contact_id", "contact", "active", "notes", "created_on", "role_memberships")


class TripEventWriteSerializer(serializers.ModelSerializer):
    trip_id = serializers.PrimaryKeyRelatedField(source="trip_id", queryset=Trip.objects.all())
    airport_id = serializers.PrimaryKeyRelatedField(source="airport_id", queryset=Airport.objects.all())
    crew_line_id = serializers.PrimaryKeyRelatedField(
        source="crew_line_id", queryset=CrewLine.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = TripEvent
        fields = (
            "id",
            "trip_id",
            "airport_id",
            "event_type",
            "start_time_local",
            "start_time_utc",
            "end_time_local",
            "end_time_utc",
            "crew_line_id",
            "notes",
        )

    def validate(self, attrs):
        ev_type = attrs.get("event_type") or (self.instance and self.instance.event_type)
        if ev_type == "CREW_CHANGE":
            if not attrs.get("crew_line_id") and not (self.instance and self.instance.crew_line_id):
                raise serializers.ValidationError({"crew_line_id": "Required for CREW_CHANGE"})
            # end_time is not required for crew change; treat as instantaneous or short window

        if ev_type == "OVERNIGHT":
            st = attrs.get("start_time_utc") or (self.instance and self.instance.start_time_utc)
            et = attrs.get("end_time_utc") or (self.instance and self.instance.end_time_utc)
            if not (st and et):
                raise serializers.ValidationError({"end_time_utc": "OVERNIGHT requires start and end times"})
            if et <= st:
                raise serializers.ValidationError({"end_time_utc": "Must be after start_time_utc"})
        return attrs


class TripEventReadSerializer(serializers.ModelSerializer):
    # Return IDs to match your API style
    trip_id = serializers.PrimaryKeyRelatedField(source="trip_id", read_only=True)
    airport_id = serializers.PrimaryKeyRelatedField(source="airport_id", read_only=True)
    crew_line_id = serializers.PrimaryKeyRelatedField(source="crew_line_id", read_only=True)

    class Meta:
        model = TripEvent
        fields = (
            "id",
            "trip_id",
            "airport_id",
            "event_type",
            "start_time_local",
            "start_time_utc",
            "end_time_local",
            "end_time_utc",
            "crew_line_id",
            "notes",
            "created_on",
        )

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


# File: api/contact_service.py

```python
"""
Unified Contact Creation Service

This service provides a clean, consistent way to create contact records
that can be used for patients, staff, customers, and passengers.
All passport information, birth dates, and contact details are now 
stored on the Contact model.
"""

from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Contact, Patient, Staff, Passenger
from typing import Dict, Any, Optional, Tuple
from datetime import date


class ContactCreationService:
    """
    Service class for creating contacts and associated records (Patient, Staff, Passenger, etc.)
    """
    
    @staticmethod
    def create_contact_with_related(
        contact_data: Dict[str, Any],
        related_type: str,
        related_data: Optional[Dict[str, Any]] = None,
        created_by=None
    ) -> Tuple[Contact, Any]:
        """
        Create a contact record along with its related record (Patient, Staff, Passenger, etc.)
        
        Args:
            contact_data: Dictionary containing contact information
            related_type: Type of related record ('patient', 'staff', 'passenger', 'customer')
            related_data: Additional data specific to the related record type
            created_by: User who is creating the record
            
        Returns:
            Tuple of (Contact instance, Related instance)
            
        Raises:
            ValidationError: If data validation fails
        """
        if related_data is None:
            related_data = {}
            
        with transaction.atomic():
            # Validate and create contact
            contact = ContactCreationService._create_contact(contact_data, created_by)
            
            # Create related record
            related_instance = None
            if related_type == 'patient':
                related_instance = ContactCreationService._create_patient(contact, related_data, created_by)
            elif related_type == 'staff':
                related_instance = ContactCreationService._create_staff(contact, related_data, created_by)
            elif related_type == 'passenger':
                related_instance = ContactCreationService._create_passenger(contact, related_data, created_by)
            elif related_type == 'customer':
                # For customers, we just need the contact record
                related_instance = contact
            else:
                raise ValidationError(f"Unknown related type: {related_type}")
                
            return contact, related_instance
    
    @staticmethod
    def _create_contact(contact_data: Dict[str, Any], created_by=None) -> Contact:
        """
        Create and validate a Contact record
        """
        # Validate required fields
        ContactCreationService._validate_contact_data(contact_data)
        
        # Create contact instance
        contact = Contact(
            # Personal Information
            first_name=contact_data.get('first_name', '').strip(),
            last_name=contact_data.get('last_name', '').strip(),
            business_name=contact_data.get('business_name', '').strip(),
            
            # Contact Information
            email=contact_data.get('email', '').strip(),
            phone=contact_data.get('phone', '').strip(),
            
            # Address Information
            address_line1=contact_data.get('address_line1', '').strip(),
            address_line2=contact_data.get('address_line2', '').strip(),
            city=contact_data.get('city', '').strip(),
            state=contact_data.get('state', '').strip(),
            zip=contact_data.get('zip', '').strip(),
            country=contact_data.get('country', '').strip(),
            
            # Personal Details (now on Contact table)
            nationality=contact_data.get('nationality', '').strip(),
            date_of_birth=contact_data.get('date_of_birth'),
            passport_number=contact_data.get('passport_number', '').strip(),
            passport_expiration_date=contact_data.get('passport_expiration_date'),
            
            # Audit fields
            created_by=created_by,
            status=contact_data.get('status', 'active')
        )
        
        # Validate and save
        contact.full_clean()
        contact.save()
        
        return contact
    
    @staticmethod
    def _create_patient(contact: Contact, patient_data: Dict[str, Any], created_by=None) -> Patient:
        """
        Create a Patient record linked to the Contact
        """
        patient = Patient(
            info=contact,
            special_instructions=patient_data.get('special_instructions', '').strip(),
            bed_at_origin=patient_data.get('bed_at_origin', False),
            bed_at_destination=patient_data.get('bed_at_destination', False),
            status=patient_data.get('status', 'pending'),
            created_by=created_by,
            
            # Note: These fields are now deprecated and will be removed in future migration
            # The data should come from contact.date_of_birth, contact.nationality, etc.
            date_of_birth=contact.date_of_birth or date.today(),
            nationality=contact.nationality or 'Unknown',
            passport_number=contact.passport_number or '',
            passport_expiration_date=contact.passport_expiration_date or date.today(),
        )
        
        patient.full_clean()
        patient.save()
        
        return patient
    
    @staticmethod
    def _create_staff(contact: Contact, staff_data: Dict[str, Any], created_by=None) -> Staff:
        """
        Create a Staff record linked to the Contact
        """
        # Check if staff already exists for this contact
        if Staff.objects.filter(contact=contact).exists():
            raise ValidationError("Staff record already exists for this contact")
            
        staff = Staff(
            contact=contact,
            active=staff_data.get('active', True),
            notes=staff_data.get('notes', '').strip(),
            created_by=created_by
        )
        
        staff.full_clean()
        staff.save()
        
        return staff
    
    @staticmethod
    def _create_passenger(contact: Contact, passenger_data: Dict[str, Any], created_by=None) -> Passenger:
        """
        Create a Passenger record linked to the Contact
        """
        passenger = Passenger(
            info=contact,
            contact_number=passenger_data.get('contact_number', '').strip(),
            notes=passenger_data.get('notes', '').strip(),
            status=passenger_data.get('status', 'active'),
            created_by=created_by,
            
            # Note: These fields are now deprecated and will be removed in future migration
            # The data should come from contact.date_of_birth, contact.nationality, etc.
            date_of_birth=contact.date_of_birth,
            nationality=contact.nationality or '',
            passport_number=contact.passport_number or '',
            passport_expiration_date=contact.passport_expiration_date,
        )
        
        passenger.full_clean()
        passenger.save()
        
        return passenger
    
    @staticmethod
    def _validate_contact_data(contact_data: Dict[str, Any]):
        """
        Validate contact data before creation
        """
        # Check that either personal name or business name is provided
        first_name = contact_data.get('first_name', '').strip()
        last_name = contact_data.get('last_name', '').strip()
        business_name = contact_data.get('business_name', '').strip()
        
        if not first_name and not last_name and not business_name:
            raise ValidationError("Either first/last name or business name is required")
        
        # Validate email format if provided
        email = contact_data.get('email', '').strip()
        if email and '@' not in email:
            raise ValidationError("Invalid email format")
        
        # Validate passport expiration is after birth date if both provided
        birth_date = contact_data.get('date_of_birth')
        passport_expiration = contact_data.get('passport_expiration_date')
        
        if birth_date and passport_expiration and passport_expiration <= birth_date:
            raise ValidationError("Passport expiration date must be after date of birth")
    
    @staticmethod
    def update_contact_and_related(
        contact: Contact,
        contact_data: Dict[str, Any],
        related_instance: Any = None,
        related_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[Contact, Any]:
        """
        Update existing contact and related record
        """
        with transaction.atomic():
            # Update contact fields
            for field, value in contact_data.items():
                if hasattr(contact, field):
                    if isinstance(value, str):
                        value = value.strip()
                    setattr(contact, field, value)
            
            contact.full_clean()
            contact.save()
            
            # Update related record if provided
            if related_instance and related_data:
                for field, value in related_data.items():
                    if hasattr(related_instance, field):
                        if isinstance(value, str):
                            value = value.strip()
                        setattr(related_instance, field, value)
                
                related_instance.full_clean()
                related_instance.save()
            
            return contact, related_instance


class ContactCreationSerializer(serializers.Serializer):
    """
    Serializer for unified contact creation requests
    """
    # Contact data
    first_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    business_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    # Address fields
    address_line1 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    address_line2 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    state = serializers.CharField(max_length=100, required=False, allow_blank=True)
    zip = serializers.CharField(max_length=20, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    # Personal details (now on Contact table)
    nationality = serializers.CharField(max_length=100, required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    passport_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    passport_expiration_date = serializers.DateField(required=False, allow_null=True)
    
    # Related record type and data
    related_type = serializers.ChoiceField(
        choices=['patient', 'staff', 'passenger', 'customer'],
        required=True
    )
    related_data = serializers.JSONField(required=False, default=dict)
    
    def validate(self, data):
        # Ensure either personal or business name is provided
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        business_name = data.get('business_name', '').strip()
        
        if not first_name and not last_name and not business_name:
            raise serializers.ValidationError(
                "Either first/last name or business name is required"
            )
        
        return data
    
    def create(self, validated_data):
        # Extract related data
        related_type = validated_data.pop('related_type')
        related_data = validated_data.pop('related_data', {})
        
        # Get user from context
        created_by = self.context.get('request').user if self.context.get('request') else None
        
        # Create contact and related record
        contact, related_instance = ContactCreationService.create_contact_with_related(
            contact_data=validated_data,
            related_type=related_type,
            related_data=related_data,
            created_by=created_by
        )
        
        return {
            'contact': contact,
            'related_instance': related_instance,
            'related_type': related_type
        }
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
router.register(r"staff", views.StaffViewSet, basename="staff")
router.register(r"staff-roles", views.StaffRoleViewSet, basename="staff-role")
router.register(r"staff-role-memberships", views.StaffRoleMembershipViewSet, basename="staff-role-membership")
router.register(r"trip-events", TripEventViewSet, basename="trip-event")

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('airport/fuel-prices/<str:airport_code>/', views.get_fuel_prices, name='fuel-prices'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('contacts/create-with-related/', views.create_contact_with_related, name='create-contact-with-related'),
]

```


# File: api/views.py

```python
from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
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
    Patient, Quote, Passenger, CrewLine, Trip, TripLine, Staff, StaffRole, StaffRoleMembership
)
from .contact_service import ContactCreationService, ContactCreationSerializer
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
    PatientReadSerializer, PatientWriteSerializer, StaffReadSerializer, StaffWriteSerializer,
    StaffRoleSerializer,
    StaffRoleMembershipReadSerializer, StaffRoleMembershipWriteSerializer,
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

# Standard pagination class for all ViewSets
class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

# Custom pagination for airports (if different settings needed)
class AirportPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

# Base ViewSet with common functionality
class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination  # Apply pagination to all ViewSets
    
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
    pagination_class = AirportPagination
    search_fields = ['name', 'ident', 'icao_code', 'iata_code', 'municipality', 'iso_country', 'iso_region']
    ordering_fields = ['name', 'ident', 'icao_code', 'iata_code', 'airport_type', 'created_on']
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if len(query) < 2:
            return Response({"detail": "Search query too short"}, status=status.HTTP_400_BAD_REQUEST)
            
        airports = Airport.objects.filter(
            Q(name__icontains=query) | 
            Q(ident__icontains=query) |
            Q(icao_code__icontains=query) | 
            Q(iata_code__icontains=query) |
            Q(municipality__icontains=query) |
            Q(iso_country__icontains=query)
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
    queryset = Quote.objects.select_related('contact', 'pickup_airport', 'dropoff_airport', 'patient', 'patient__info').prefetch_related('transactions')
    search_fields = ['contact__first_name', 'contact__last_name', 'patient__info__first_name', 'patient__info__last_name', 'status']
    ordering_fields = ['created_on', 'quoted_amount']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadQuote | CanWriteQuote | CanModifyQuote | CanDeleteQuote
    ]
    
    def get_queryset(self):
        """
        Filter quotes by status and handle UUID search if provided in query params
        """
        queryset = super().get_queryset()
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset
    
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
    queryset = Trip.objects.select_related('quote', 'patient', 'patient__info', 'aircraft').prefetch_related('trip_lines', 'passengers__info')
    search_fields = ['trip_number', 'type', 'patient__info__first_name', 'patient__info__last_name', 'passengers__info__first_name', 'passengers__info__last_name']
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
                    'patient_name': f"{q.patient.info.first_name or ''} {q.patient.info.last_name or ''}".strip() if q.patient and q.patient.info else 'No patient'
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


class StaffViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Staff.objects.select_related("contact").all().order_by("-created_on")
    search_fields = ['contact__first_name', 'contact__last_name', 'contact__business_name', 'contact__email']

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return StaffReadSerializer
        return StaffWriteSerializer


class StaffRoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StaffRole.objects.all().order_by("code")
    serializer_class = StaffRoleSerializer


class StaffRoleMembershipViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StaffRoleMembership.objects.select_related("staff", "role").all().order_by("-created_on")

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by staff_id if provided
        staff_id = self.request.query_params.get('staff_id', None)
        if staff_id is not None:
            queryset = queryset.filter(staff_id=staff_id)
        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return StaffRoleMembershipReadSerializer
        return StaffRoleMembershipWriteSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_contact_with_related(request):
    """
    Unified endpoint for creating contacts with related records (Patient, Staff, Passenger, Customer)
    
    POST /api/contacts/create-with-related/
    
    Body:
    {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-01",
        "passport_number": "123456789",
        "passport_expiration_date": "2030-01-01",
        "nationality": "US",
        "related_type": "patient",  // "patient", "staff", "passenger", "customer"
        "related_data": {
            "special_instructions": "Requires wheelchair assistance",
            "bed_at_origin": true,
            "status": "confirmed"
        }
    }
    """
    serializer = ContactCreationSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        try:
            result = serializer.save()
            
            # Return appropriate response based on related type
            contact = result['contact']
            related_instance = result['related_instance']
            related_type = result['related_type']
            
            response_data = {
                'contact': ContactSerializer(contact).data,
                'related_type': related_type,
                'success': True,
                'message': f'{related_type.capitalize()} created successfully'
            }
            
            # Add specific related data
            if related_type == 'patient':
                from .serializers import PatientReadSerializer
                response_data['patient'] = PatientReadSerializer(related_instance).data
            elif related_type == 'staff':
                response_data['staff'] = StaffReadSerializer(related_instance).data
            elif related_type == 'passenger':
                from .serializers import PassengerReadSerializer
                response_data['passenger'] = PassengerReadSerializer(related_instance).data
            elif related_type == 'customer':
                response_data['customer'] = ContactSerializer(related_instance).data
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e),
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


```


# File: api/migrations/0006_alter_airport_iata_code_alter_airport_icao_code.py

```python
# Generated by Django 5.1.11 on 2025-08-24 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_airport_airport_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="airport",
            name="iata_code",
            field=models.CharField(blank=True, db_index=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name="airport",
            name="icao_code",
            field=models.CharField(
                blank=True, db_index=True, max_length=4, null=True, unique=True
            ),
        ),
    ]

```


# File: api/migrations/0005_airport_airport_type.py

```python
# Generated by Django 5.1.11 on 2025-08-24 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_rename_country_airport_iso_country_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="airport",
            name="airport_type",
            field=models.CharField(
                choices=[
                    ("large_airport", "Large airport"),
                    ("medium_airport", "Medium airport"),
                    ("small_airport", "Small airport"),
                ],
                db_index=True,
                default="small_airport",
                max_length=20,
            ),
        ),
    ]

```


# File: api/migrations/0010_tripevent.py

```python
# Generated by Django 5.1.11 on 2025-08-26 04:02

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_fbo_email"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TripEvent",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("CREW_CHANGE", "Crew Change"),
                            ("OVERNIGHT", "Overnight (New Day)"),
                        ],
                        max_length=20,
                    ),
                ),
                ("start_time_local", models.DateTimeField()),
                ("start_time_utc", models.DateTimeField()),
                ("end_time_local", models.DateTimeField(blank=True, null=True)),
                ("end_time_utc", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "airport_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="trip_events",
                        to="api.airport",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "crew_line_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="trip_events",
                        to="api.crewline",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "trip_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="api.trip",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["trip_id", "start_time_utc"],
                        name="api_tripeve_trip_id_aaf262_idx",
                    ),
                    models.Index(
                        fields=["event_type"], name="api_tripeve_event_t_85f611_idx"
                    ),
                ],
            },
        ),
    ]

```


# File: api/migrations/0004_rename_country_airport_iso_country_and_more.py

```python
# Generated by Django 5.1.11 on 2025-08-24 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_staff_staffrole_staffrolemembership_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="airport",
            old_name="country",
            new_name="iso_country",
        ),
        migrations.RenameField(
            model_name="airport",
            old_name="state",
            new_name="iso_region",
        ),
        migrations.RemoveField(
            model_name="airport",
            name="city",
        ),
        migrations.AddField(
            model_name="airport",
            name="gps_code",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="airport",
            name="ident",
            field=models.CharField(
                db_index=True, default="UTC", max_length=10, unique=True
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="airport",
            name="local_code",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="airport",
            name="municipality",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

```


# File: api/migrations/0008_fbo_phone_fbo_phone_secondary.py

```python
# Generated by Django 5.1.11 on 2025-08-26 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_contact_date_of_birth_contact_nationality_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="fbo",
            name="phone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="fbo",
            name="phone_secondary",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

```


# File: api/migrations/__init__.py

```python

```


# File: api/migrations/0003_staff_staffrole_staffrolemembership_and_more.py

```python
# Generated by Django 5.1.11 on 2025-08-23 05:26

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_trip_notes"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("active", models.BooleanField(default=True)),
                ("notes", models.TextField(blank=True)),
                (
                    "contact",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="staff",
                        to="api.contact",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="StaffRole",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("code", models.CharField(max_length=32, unique=True)),
                ("name", models.CharField(max_length=64)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StaffRoleMembership",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("start_on", models.DateField(blank=True, null=True)),
                ("end_on", models.DateField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="memberships",
                        to="api.staffrole",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="role_memberships",
                        to="api.staff",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="staffrole",
            index=models.Index(fields=["code"], name="api_staffro_code_20dc3e_idx"),
        ),
        migrations.AddConstraint(
            model_name="staffrolemembership",
            constraint=models.UniqueConstraint(
                fields=("staff", "role", "start_on", "end_on"),
                name="uniq_staff_role_interval",
            ),
        ),
    ]

```


# File: api/migrations/0009_fbo_email.py

```python
# Generated by Django 5.1.11 on 2025-08-26 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_fbo_phone_fbo_phone_secondary"),
    ]

    operations = [
        migrations.AddField(
            model_name="fbo",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]

```


# File: api/migrations/0002_trip_notes.py

```python
# Generated by Django 5.1.11 on 2025-08-22 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trip",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
    ]

```


# File: api/migrations/0007_contact_date_of_birth_contact_nationality_and_more.py

```python
# Generated by Django 5.1.11 on 2025-08-24 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_alter_airport_iata_code_alter_airport_icao_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="nationality",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="passport_expiration_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="passport_number",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

```


# File: api/migrations/0001_initial.py

```python
# Generated by Django 5.1.11 on 2025-08-22 04:07

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("filename", models.CharField(max_length=255)),
                ("content", models.BinaryField()),
                ("flag", models.IntegerField(default=0)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Aircraft",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                (
                    "tail_number",
                    models.CharField(db_index=True, max_length=20, unique=True),
                ),
                ("company", models.CharField(max_length=255)),
                (
                    "mgtow",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        verbose_name="Maximum Gross Takeoff Weight",
                    ),
                ),
                ("make", models.CharField(max_length=100)),
                ("model", models.CharField(max_length=100)),
                ("serial_number", models.CharField(max_length=100)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("first_name", models.CharField(blank=True, max_length=100, null=True)),
                ("last_name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "business_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "address_line1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "address_line2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("zip", models.CharField(blank=True, max_length=20, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CrewLine",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "medic_ids",
                    models.ManyToManyField(
                        related_name="medic_crew_lines", to="api.contact"
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "primary_in_command",
                    models.ForeignKey(
                        db_column="primary_in_command_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="primary_crew_lines",
                        to="api.contact",
                    ),
                ),
                (
                    "secondary_in_command",
                    models.ForeignKey(
                        db_column="secondary_in_command_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="secondary_crew_lines",
                        to="api.contact",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Agreement",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("lock", models.BooleanField(default=False)),
                ("destination_email", models.EmailField(max_length=254)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("pending", "Pending"),
                            ("modified", "Modified"),
                            ("signed", "Signed"),
                            ("denied", "Denied"),
                        ],
                        default="created",
                        max_length=20,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "document_signed",
                    models.ForeignKey(
                        blank=True,
                        db_column="document_signed_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="signed_agreements",
                        to="api.document",
                    ),
                ),
                (
                    "document_unsigned",
                    models.ForeignKey(
                        blank=True,
                        db_column="document_unsigned_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="unsigned_agreements",
                        to="api.document",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FBO",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=255)),
                (
                    "address_line1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "address_line2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("zip", models.CharField(blank=True, max_length=20, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "contacts",
                    models.ManyToManyField(related_name="fbos", to="api.contact"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Ground",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=255)),
                (
                    "address_line1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "address_line2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("zip", models.CharField(blank=True, max_length=20, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "contacts",
                    models.ManyToManyField(related_name="grounds", to="api.contact"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Airport",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                (
                    "icao_code",
                    models.CharField(db_index=True, max_length=4, unique=True),
                ),
                ("iata_code", models.CharField(db_index=True, max_length=3)),
                ("name", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("country", models.CharField(max_length=100)),
                ("elevation", models.IntegerField(blank=True, null=True)),
                ("latitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("timezone", models.CharField(max_length=50)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "fbos",
                    models.ManyToManyField(
                        blank=True, related_name="airports", to="api.fbo"
                    ),
                ),
                (
                    "grounds",
                    models.ManyToManyField(
                        blank=True, related_name="airports", to="api.ground"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Modification",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("model", models.CharField(max_length=100)),
                ("object_id", models.UUIDField()),
                ("field", models.CharField(max_length=100)),
                ("before", models.TextField(blank=True, null=True)),
                ("after", models.TextField(blank=True, null=True)),
                ("time", models.DateTimeField(auto_now_add=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "ordering": ["-time"],
            },
        ),
        migrations.CreateModel(
            name="Passenger",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "nationality",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "passport_number",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("passport_expiration_date", models.DateField(blank=True, null=True)),
                (
                    "contact_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="passengers",
                        to="api.contact",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "passenger_ids",
                    models.ManyToManyField(
                        blank=True,
                        related_name="related_passengers",
                        to="api.passenger",
                    ),
                ),
                (
                    "passport_document",
                    models.ForeignKey(
                        blank=True,
                        db_column="passport_document_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="passport_passengers",
                        to="api.document",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("lock", models.BooleanField(default=False)),
                ("bed_at_origin", models.BooleanField(default=False)),
                ("bed_at_destination", models.BooleanField(default=False)),
                ("date_of_birth", models.DateField()),
                ("nationality", models.CharField(max_length=100)),
                ("passport_number", models.CharField(max_length=100)),
                ("passport_expiration_date", models.DateField()),
                ("special_instructions", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("confirmed", "Confirmed"),
                            ("active", "Active"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patients",
                        to="api.contact",
                    ),
                ),
                (
                    "letter_of_medical_necessity",
                    models.ForeignKey(
                        blank=True,
                        db_column="letter_of_medical_necessity_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="medical_necessity_patients",
                        to="api.document",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "passport_document",
                    models.ForeignKey(
                        blank=True,
                        db_column="passport_document_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="passport_patients",
                        to="api.document",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Permission",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "permission_ids",
                    models.ManyToManyField(
                        related_name="departments", to="api.permission"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "permissions",
                    models.ManyToManyField(related_name="roles", to="api.permission"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                (
                    "key",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("credit_card", "Credit Card"),
                            ("ACH", "ACH Transfer"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("pending", "Pending"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="created",
                        max_length=20,
                    ),
                ),
                (
                    "payment_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("email", models.EmailField(max_length=254)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Quote",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("lock", models.BooleanField(default=False)),
                ("quoted_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "cruise_doctor_first_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "cruise_doctor_last_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "cruise_line",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "cruise_ship",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "aircraft_type",
                    models.CharField(
                        choices=[
                            ("65", "Learjet 65"),
                            ("35", "Learjet 35"),
                            ("TBD", "To Be Determined"),
                        ],
                        max_length=20,
                    ),
                ),
                ("estimated_flight_time", models.DurationField()),
                ("includes_grounds", models.BooleanField(default=False)),
                (
                    "inquiry_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "medical_team",
                    models.CharField(
                        choices=[
                            ("RN/RN", "RN/RN"),
                            ("RN/Paramedic", "RN/Paramedic"),
                            ("RN/MD", "RN/MD"),
                            ("RN/RT", "RN/RT"),
                            ("standard", "Standard"),
                            ("full", "Full"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("confirmed", "Confirmed"),
                            ("active", "Active"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                            ("paid", "Paid"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("number_of_stops", models.PositiveIntegerField(default=0)),
                (
                    "quote_pdf_status",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("pending", "Pending"),
                            ("modified", "Modified"),
                            ("accepted", "Accepted"),
                            ("denied", "Denied"),
                        ],
                        default="created",
                        max_length=20,
                    ),
                ),
                ("quote_pdf_email", models.EmailField(max_length=254)),
                (
                    "consent_for_transport",
                    models.ForeignKey(
                        blank=True,
                        db_column="consent_for_transport_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="consent_quotes",
                        to="api.agreement",
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        db_column="contact_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quotes",
                        to="api.contact",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "documents",
                    models.ManyToManyField(related_name="quotes", to="api.document"),
                ),
                (
                    "dropoff_airport",
                    models.ForeignKey(
                        db_column="dropoff_airport_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dropoff_quotes",
                        to="api.airport",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        blank=True,
                        db_column="patient_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="quotes",
                        to="api.patient",
                    ),
                ),
                (
                    "patient_service_agreement",
                    models.ForeignKey(
                        blank=True,
                        db_column="patient_service_agreement_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="service_quotes",
                        to="api.agreement",
                    ),
                ),
                (
                    "payment_agreement",
                    models.ForeignKey(
                        blank=True,
                        db_column="payment_agreement_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="payment_quotes",
                        to="api.agreement",
                    ),
                ),
                (
                    "pickup_airport",
                    models.ForeignKey(
                        db_column="pickup_airport_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pickup_quotes",
                        to="api.airport",
                    ),
                ),
                (
                    "quote_pdf",
                    models.ForeignKey(
                        blank=True,
                        db_column="quote_pdf_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="quote_pdfs",
                        to="api.document",
                    ),
                ),
                (
                    "transactions",
                    models.ManyToManyField(
                        blank=True, related_name="quotes", to="api.transaction"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Trip",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("email_chain", models.JSONField(blank=True, default=list)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("medical", "Medical"),
                            ("charter", "Charter"),
                            ("part 91", "Part 91"),
                            ("other", "Other"),
                            ("maintenance", "Maintenance"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "estimated_departure_time",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("post_flight_duty_time", models.DurationField(blank=True, null=True)),
                ("pre_flight_duty_time", models.DurationField(blank=True, null=True)),
                (
                    "trip_number",
                    models.CharField(db_index=True, max_length=20, unique=True),
                ),
                (
                    "aircraft",
                    models.ForeignKey(
                        blank=True,
                        db_column="aircraft_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="trips",
                        to="api.aircraft",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "customer_itinerary",
                    models.ForeignKey(
                        blank=True,
                        db_column="customer_itinerary_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="customer_itinerary_trips",
                        to="api.document",
                    ),
                ),
                (
                    "internal_itinerary",
                    models.ForeignKey(
                        blank=True,
                        db_column="internal_itinerary_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="internal_itinerary_trips",
                        to="api.document",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "passengers",
                    models.ManyToManyField(
                        blank=True, related_name="trips", to="api.passenger"
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        blank=True,
                        db_column="patient_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="trips",
                        to="api.patient",
                    ),
                ),
                (
                    "quote",
                    models.ForeignKey(
                        blank=True,
                        db_column="quote_id",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trips",
                        to="api.quote",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TripLine",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("departure_time_local", models.DateTimeField()),
                ("departure_time_utc", models.DateTimeField()),
                ("arrival_time_local", models.DateTimeField()),
                ("arrival_time_utc", models.DateTimeField()),
                ("distance", models.DecimalField(decimal_places=2, max_digits=10)),
                ("flight_time", models.DurationField()),
                ("ground_time", models.DurationField()),
                ("passenger_leg", models.BooleanField(default=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "crew_line",
                    models.ForeignKey(
                        blank=True,
                        db_column="crew_line_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="trip_lines",
                        to="api.crewline",
                    ),
                ),
                (
                    "destination_airport",
                    models.ForeignKey(
                        db_column="destination_airport_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="destination_trip_lines",
                        to="api.airport",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "origin_airport",
                    models.ForeignKey(
                        db_column="origin_airport_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="origin_trip_lines",
                        to="api.airport",
                    ),
                ),
                (
                    "trip",
                    models.ForeignKey(
                        db_column="trip_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trip_lines",
                        to="api.trip",
                    ),
                ),
            ],
            options={
                "ordering": ["departure_time_utc"],
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(db_index=True, default="active", max_length=50),
                ),
                ("lock", models.BooleanField(default=False)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "address_line1",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "address_line2",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("zip", models.CharField(blank=True, max_length=20, null=True)),
                ("flags", models.JSONField(blank=True, default=list)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "department_ids",
                    models.ManyToManyField(related_name="users", to="api.department"),
                ),
                (
                    "departments",
                    models.ManyToManyField(
                        related_name="department_users", to="api.department"
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("roles", models.ManyToManyField(related_name="users", to="api.role")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
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


# File: api/management/commands/import_airports.py

```python
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, IntegrityError

from api.models import Airport, AirportType  # adjust import path if needed

# Optional timezone lookup
try:
    from timezonefinder import TimezoneFinder
    TF = TimezoneFinder()
except Exception:
    TF = None


def to_decimal(val, places=6):
    if val is None:
        return None
    s = str(val).strip()
    if not s or s.lower() == "null":
        return None
    try:
        d = Decimal(s)
        return d.quantize(Decimal("0." + "0" * places))
    except (InvalidOperation, ValueError):
        return None


def to_int(val):
    if val is None:
        return None
    s = str(val).strip()
    if not s or s.lower() == "null":
        return None
    try:
        return int(Decimal(s))
    except (InvalidOperation, ValueError):
        return None


def norm_str(val):
    if val is None:
        return None
    s = str(val).strip()
    return s or None


TYPE_MAP = {
    "large_airport": getattr(AirportType, "LARGE", "large_airport"),
    "medium_airport": getattr(AirportType, "MEDIUM", "medium_airport"),
    "small_airport": getattr(AirportType, "SMALL", "small_airport"),
    "heliport": getattr(AirportType, "SMALL", "small_airport"),
    "seaplane_base": getattr(AirportType, "SMALL", "small_airport"),
    "closed": getattr(AirportType, "SMALL", "small_airport"),
}


def infer_timezone(lat, lon):
    if lat is None or lon is None:
        return "UTC"
    if TF is None:
        return "UTC"
    try:
        tz = TF.timezone_at(lat=float(lat), lng=float(lon))
        return tz or "UTC"
    except Exception:
        return "UTC"


def flush_buffer(buffer, batch_size):
    """Try bulk_create, then fallback to row-by-row on conflicts."""
    created = 0
    skipped = 0
    if not buffer:
        return 0, 0

    try:
        with transaction.atomic():
            Airport.objects.bulk_create(
                buffer, ignore_conflicts=True, batch_size=batch_size
            )
            created += len(buffer)
        return created, skipped
    except IntegrityError:
        pass  # fallback row by row

    for inst in buffer:
        try:
            with transaction.atomic():
                inst.save()
                created += 1
        except IntegrityError:
            skipped += 1
    return created, skipped


class Command(BaseCommand):
    help = "Import airports from a CSV with columns like OurAirports."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to airports.csv")
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing airports matched by ident.",
        )
        parser.add_argument(
            "--batch",
            type=int,
            default=1000,
            help="Bulk create batch size.",
        )

    def handle(self, *args, **opts):
        csv_path = Path(opts["csv_path"])
        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        update_existing = opts["update"]
        batch_size = opts["batch"]

        created = updated = skipped = 0
        buffer = []

        # preload existing idents for quick lookup
        existing_idents = set(
            Airport.objects.values_list("ident", flat=True)
        )

        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                ident = norm_str(row.get("ident"))
                if not ident:
                    skipped += 1
                    continue

                name = norm_str(row.get("name")) or ident
                lat = to_decimal(row.get("latitude_deg"))
                lon = to_decimal(row.get("longitude_deg"))
                elevation = to_int(row.get("elevation_ft"))

                iso_country = norm_str(row.get("iso_country")) or "US"
                iso_region = norm_str(row.get("iso_region"))
                municipality = norm_str(row.get("municipality"))

                icao_code = norm_str(row.get("icao_code"))
                iata_code = norm_str(row.get("iata_code"))
                gps_code = norm_str(row.get("gps_code"))
                local_code = norm_str(row.get("local_code"))

                csv_type = (norm_str(row.get("type")) or "").lower()
                airport_type = TYPE_MAP.get(
                    csv_type, getattr(AirportType, "SMALL", "small_airport")
                )

                tz = infer_timezone(lat, lon)

                defaults = dict(
                    name=name,
                    latitude=lat,
                    longitude=lon,
                    elevation=elevation,
                    iso_country=iso_country,
                    iso_region=iso_region,
                    municipality=municipality,
                    icao_code=icao_code,
                    iata_code=iata_code,
                    local_code=local_code,
                    gps_code=gps_code,
                    airport_type=airport_type,
                    timezone=tz,
                )

                if ident in existing_idents:
                    if update_existing:
                        try:
                            Airport.objects.filter(ident=ident).update(**defaults)
                            updated += 1
                        except IntegrityError:
                            skipped += 1
                    continue
                else:
                    buffer.append(Airport(ident=ident, **defaults))
                    if len(buffer) >= batch_size:
                        c, s = flush_buffer(buffer, batch_size)
                        created += c
                        skipped += s
                        buffer = []

        # flush leftover
        if buffer:
            c, s = flush_buffer(buffer, batch_size)
            created += c
            skipped += s

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete: created={created}, updated={updated}, skipped={skipped}"
            )
        )

```


# File: api/management/commands/seed_staff.py

```python
# api/management/commands/seed_staff.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from api.models import (
    Staff,
    StaffRole,
    StaffRoleMembership,
    Contact,
    CrewLine,
)

ROLE_CODES = [
    ("PIC", "Pilot in Command"),
    ("SIC", "Second in Command"),
    ("RN", "Registered Nurse"),
    ("PARAMEDIC", "Paramedic"),
    ("RT", "Respiratory Therapist"),
    ("MD", "Physician"),
]


class Command(BaseCommand):
    help = (
        "Seeds StaffRole, backfills Staff for Contacts used on CrewLines, "
        "and (optionally) creates basic StaffRoleMemberships for PIC/SIC."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-memberships",
            action="store_true",
            help="Also create StaffRoleMemberships for PIC/SIC based on CrewLine usage.",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        # Ensure roles exist
        created_roles = 0
        for code, name in ROLE_CODES:
            _, was_created = StaffRole.objects.get_or_create(code=code, defaults={"name": name})
            if was_created:
                created_roles += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"StaffRole ensured (created {created_roles}, total {StaffRole.objects.count()})."
            )
        )

        # Collect all Contact IDs referenced by CrewLine (PIC, SIC, and medics)
        contact_ids = set()

        # PIC / SIC via FK fields (use iterator with chunk_size for memory safety)
        for cl in CrewLine.objects.only(
            "primary_in_command_id", "secondary_in_command_id"
        ).iterator(chunk_size=1000):
            if getattr(cl, "primary_in_command_id_id", None):
                contact_ids.add(cl.primary_in_command_id_id)
            if getattr(cl, "secondary_in_command_id_id", None):
                contact_ids.add(cl.secondary_in_command_id_id)

        # Medics via M2M; when using prefetch_related, don't call iterator() without chunk_size
        for cl in CrewLine.objects.prefetch_related("medic_ids"):
            contact_ids.update(cl.medic_ids.values_list("id", flat=True))

        # Backfill Staff rows for those Contacts
        created_staff = 0
        for cid in contact_ids:
            _, was_created = Staff.objects.get_or_create(contact_id=cid, defaults={"active": True})
            if was_created:
                created_staff += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Staff ensured for {len(contact_ids)} contact(s) (created {created_staff})."
            )
        )

        # Optionally add PIC/SIC memberships effective today
        if opts.get("with_memberships"):
            today = timezone.now().date()

            roles = {r.code: r for r in StaffRole.objects.filter(code__in=["PIC", "SIC"])}
            pic = roles.get("PIC")
            sic = roles.get("SIC")

            made = 0

            if pic:
                pic_contact_ids = (
                    CrewLine.objects.exclude(primary_in_command_id__isnull=True)
                    .values_list("primary_in_command_id", flat=True)
                    .distinct()
                )
                for cid in pic_contact_ids:
                    staff = Staff.objects.filter(contact_id=cid).first()
                    if staff and not StaffRoleMembership.objects.filter(
                        staff=staff, role=pic, start_on=today, end_on=None
                    ).exists():
                        StaffRoleMembership.objects.create(
                            staff=staff, role=pic, start_on=today, end_on=None
                        )
                        made += 1

            if sic:
                sic_contact_ids = (
                    CrewLine.objects.exclude(secondary_in_command_id__isnull=True)
                    .values_list("secondary_in_command_id", flat=True)
                    .distinct()
                )
                for cid in sic_contact_ids:
                    staff = Staff.objects.filter(contact_id=cid).first()
                    if staff and not StaffRoleMembership.objects.filter(
                        staff=staff, role=sic, start_on=today, end_on=None
                    ).exists():
                        StaffRoleMembership.objects.create(
                            staff=staff, role=sic, start_on=today, end_on=None
                        )
                        made += 1

            self.stdout.write(self.style.SUCCESS(f"PIC/SIC memberships created today: {made}"))
        else:
            self.stdout.write(
                self.style.WARNING("Skipped memberships (run with --with-memberships to add PIC/SIC).")
            )

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


# File: api/management/commands/seed_aircraft_and_staff.py

```python
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from django.utils import timezone

from decimal import Decimal
from datetime import datetime
import re

from api.models import (
    Aircraft,
    Contact,
    Staff,
    StaffRole,
    StaffRoleMembership,
)

# -----------------------------
# SOURCE DATA (from your prompt)
# -----------------------------

AIRCRAFT_ROWS = [
    # tail, company, make, model, serial_number, mgtow (lb)
    ("N911KQ", "Secret Squirrel Aerospace LLC", "Kodiak",   "Kodiak 100", "100-0009", "7255"),
    ("N35LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "35A",       "240",      "18300"),
    ("N36LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "36A",       "44",       "18300"),
    ("N30LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "31",        "002",      "18300"),
    ("N60LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "52",       "23500"),
    ("N65LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "243",      "23500"),
    ("N70LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "70",       "23500"),
    ("N80LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "305",      "23500"),
    ("N85LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "244",      "23500"),
    ("N90LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "287",      "23500"),
]

PILOT_ROWS = [
    # Name, Nat., DOB, Passport #, Exp., Contact #, Email
    ("Anthony Guglielmetti","US","11/27/1997","534687611","10/27/2025","813-613-1396","AnthonyGuglielmetti@jeticu.com"),
    ("Christopher McGuire","US","11/26/1985","565155697","02/06/2027","813-468-6889","chris.mcguire@jeticu.com"),
    ("Jason Rowe","US","11/20/1982","583027251","11/08/2027","218-343-2005","jrowe@jeticu.com"),
    ("Kurt Veilleux","US","09/17/1983","A35779864","02/08/2034","813-417-6891","kurt@jeticu.com"),
    ("Michael Honeycutt","US","12/18/1969","A03627887","10/13/2032","727-415-9458","mike@jeticu.com"),
    ("John Cannon II","US","05/06/1998","A61105507","02/24/2035","786-879-9393","john.cannon@jeticu.com"),
    ("Patrick Buttermore","US","12/22/1986","A35779865","02/08/2034","813-951-0961","Patrick.Buttermore@jeticu.com"),
    ("Thomas Lacey","US","08/04/1968","A07991093","12/26/2032","727-510-5189","tom@jeticu.com"),
    ("Steven Peterson","US","04/10/1997","A26963982","07/30/2033","845-520-0244","StevePeterson@jeticu.com"),
    ("Tyler Towle","US","04/28/1997","A36095632","10/20/2034","801-824-2782","TylerTowle@jeticu.com"),
    ("Oleg Baumgart","US","01/12/1981","541154548","12/06/2025","575-571-6363","oleg.baumgart@jeticu.com"),
    ("Gary Kelley","US","09/30/1955","561205578","10/11/2027","727-560-0555","puffin@jeticu.com"),
    ("Jack Al-Hussaini","US","11/06/2002","590363317","12/27/2028","704-818-7600","JackAl-Hussaini@jeticu.com"),
]

MEDIC_ROWS = [
    ("Amy Nicole Nilsen","US","05/31/1993","A35874322","05/21/2034","845-421-0106","AMY.NILSEN31@GMAIL.COM"),
    ("Carlos Smith","US","9/10/1972","645442043","04/15/2029","813-454-7837","emnole1995@gmail.com"),
    ("Christopher Izzi","US","12/31/1990","A06603660","06/13/2032","570-856-2730","deltanu239@gmail.com"),
    ("Jacob Samuel Cruz","US","8/10/1995","559629951","04/03/2027","813-340-9103","jcruzmusic16@icloud.com"),
    ("Devin Mormando","US","9/4/1986","A34987989","12/06/2033","352-573-1380","dmormando@elfr.org"),
    ("Jill Butler","US","5/8/1971","678687790","07/04/2032","813-614-4496","jsbutlerrn@gmail.com"),
    ("Eric Castellucci","US","08/10/1953","512319513","01/25/2024","813-417-3210","trilucci@gmail.com"),
    ("Nicholas Mc Sweeney","US","11/6/1990","542911451","04/03/2026","386-588-4005","nickjb_1106@yahoo.com"),
    ("Gary Hurlbut","US","09/26/1968","A03628812","11/20/2032","727-355-3944","AirHurly@gmail.com"),
    ("Harold John Haverty","US","08/23/1961","583528607","05/19/2028","727-504-0451","havertyjohn@yahoo.com"),
    ("James Byrns","US","07/11/1968","A04083672","10/16/2033","727-518-4441","james.byrns68@gmail.com"),
    ("Jamie Lynn Juliano","US","02/18/1983","554218813","07/19/2026","815-641-4906","jamie.juliano7@gmail.com"),
    ("Jared Wayt","US","02/07/1986","565787394","02/26/2028","813-312-4708","jaredw@jeticu.com"),
    ("Jessica May Mone","US","07/22/1978","598263733","06/12/2029","727-599-5138","mjessy0722@gmail.com"),
    ("John David Mulford","US","08/21/1984","A04704947","02/05/2033","813-833-4663","johnmulford@yahoo.com"),
    ("John P. Opyoke","US","7/30/1969","A20507949","05/30/2033","352-263-6925","trinityurgentcare@yahoo.com"),
    ("Jon Inkrott","US","3/17/1972","599921500","07/17/2029","407-516-5579","jon.inkrott@adventhealth.com"),
    ("Justin Andrews","US","10/24/1984","568082572","10/01/2030","239-233-9799","RFinkle5@me.com"),
    ("Kimberly Recinella","US","4/5/1992","673093739","01/23/2032","513-226-1066","ktrecinella@gmail.com"),
    ("Kristin Howell","US","08/17/1984","587818528","09/17/2028","813-361-3009","kristinvictory@gmail.com"),
    ("Kurt Veilleux","US","09/17/1983","520374483","08/03/2024","813-417-6891","kurt@jeticu.com"),
    ("Mary McCarthy","US","11/06/1955","A03492999","02/15/2032","727-641-0085","mary@jeticu.com"),
    ("Michael Abesada","US","01/07/1979","A23420769","10/25/2033","786-447-7153","abesadam@gmail.com"),
    ("Robert Sullivan","US","12/19/1983","572232934","05/24/2027","352-406-2573","bsullivan403@yahoo.com"),
    ("Anthony Marino","US","03/23/1982","674420053","02/10/2032","772-418-0312","antr0323@gmail.com"),
    ("Jefferson Day","US","09/01/1989","A22153633","06/25/2033","352-585-1068","Jeffy_day@yahoo.com"),
    ("Ronald Figueredo","US","7/31/1976","567221355","06/13/2029","610-952-3430","ronaldfigueredo@gmail.com"),
    ("Ronald Wyant","US","09/28/1963","A04483166","09/27/2033","727-639-5126","swyant1@icloud.com"),
    ("Bruce Loeb Jr.","US","01/27/1971","A10316135","11/06/2032","904-338-6447","bnloeb9@gmail.com"),
    ("Thomas Tropeano","US","2/16/1954","549865068","03/13/2027","352-804-9629","tltropeano@yahoo.com"),
    ("Tiffany Bourne","US","03/15/1973","A04483169","09/27/2033","813-260-0343","bourneid73@gmail.com"),
    ("Carla Lynn Sieber","US","07/27/1991","A49128381","11/13/2034","727-424-6886","carlasieber@msn.com"),
    ("Tyson Elledge","US","08/03/1979","A03502556","03/27/2032","352-442-2819","tysonelledge@aol.com"),
    ("Mario Rocha","US","06/02/1970","641826321","03/10/2029","813-215-3277","mario.r.rocha70@gmail.com"),
    ("Jason A. Berger","US","12/10/1990","643816544","09/16/2029","727-512-2959","jberger9359@gmail.com"),
    ("Courtney Hershey","US","05/12/1979","A15958520","03/04/2033","727-519-4714","hersheycourtney@gmail.com"),
]

# Desired role set per cohort
PILOT_ROLE_CODES = ["PIC", "SIC"]
MEDIC_ROLE_CODES = ["RT", "RN", "PARAMEDIC", "MD"]

# Default human-readable names if roles don't exist
ROLE_NAMES_BY_CODE = {
    "PIC": "Pilot in Command",
    "SIC": "Second in Command",
    "RN": "Registered Nurse",
    "PARAMEDIC": "Paramedic",
    "MD": "Physician",
    "RT": "Respiratory Therapist",
}


# -----------------------------
# HELPERS
# -----------------------------

DATE_PATTERNS = ["%m/%d/%Y", "%m/%d/%y", "%m/%-d/%Y", "%m/%-d/%y"]  # macOS strptime may not support %-d; we'll handle manually.

def parse_date(s):
    if not s:
        return None
    s = s.strip()
    # Normalize single-digit months/days to zero-padded mm/dd/yyyy
    # e.g., 9/4/1986 -> 09/04/1986
    parts = re.split(r"[/-]", s)
    if len(parts) == 3:
        mm, dd, yyyy = parts
        if len(mm) == 1: mm = f"0{mm}"
        if len(dd) == 1: dd = f"0{dd}"
        if len(yyyy) == 2:  # assume 20xx for 2-digit years? safer: 19xx for <=30?
            yyyy = "20" + yyyy if int(yyyy) < 50 else "19" + yyyy
        s = f"{mm}/{dd}/{yyyy}"
    for fmt in ("%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def split_name(full_name):
    """
    Split 'First [Middle/Initial/Joint] Last [Suffix]' into first_name, last_name.
    We'll keep everything after the first token as last_name for simplicity,
    but handle common suffixes ("Jr.", "II", "III") gracefully.
    """
    if not full_name:
        return None, None
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0], ""
    # Keep suffix attached to last
    suffixes = {"Jr.", "Jr", "Sr.", "Sr", "II", "III", "IV", "V"}
    first = parts[0]
    last = " ".join(parts[1:])
    # compact "Al-Hussaini" etc. untouched
    # nothing more fancy needed for now
    return first, last


def get_or_create_role(code):
    role = StaffRole.objects.filter(code=code).first()
    if role:
        return role
    # Create with default name if missing
    name = ROLE_NAMES_BY_CODE.get(code, code)
    role = StaffRole.objects.create(code=code, name=name)
    return role


def upsert_contact(name, nationality, dob, passport_no, passport_exp, phone, email):
    first_name, last_name = split_name(name)
    # Try to match by email first; fall back to (name + phone)
    contact = None
    if email:
        contact = Contact.objects.filter(email=email.strip()).first()
    if not contact:
        # Try exact name + phone
        contact = Contact.objects.filter(
            first_name=first_name or "",
            last_name=last_name or "",
            phone=(phone or "").strip() or None,
        ).first()

    dob_dt = parse_date(dob)
    pass_exp_dt = parse_date(passport_exp)

    if contact:
        # Update basics if missing
        dirty = False
        if not contact.first_name and first_name:
            contact.first_name = first_name; dirty = True
        if not contact.last_name and last_name:
            contact.last_name = last_name; dirty = True
        if nationality and (contact.nationality != nationality):
            contact.nationality = nationality; dirty = True
        if email and (contact.email != email):
            contact.email = email; dirty = True
        if phone and (contact.phone != phone):
            contact.phone = phone; dirty = True
        if dob_dt and (contact.date_of_birth != dob_dt):
            contact.date_of_birth = dob_dt; dirty = True
        if passport_no and (contact.passport_number != passport_no):
            contact.passport_number = passport_no; dirty = True
        if pass_exp_dt and (contact.passport_expiration_date != pass_exp_dt):
            contact.passport_expiration_date = pass_exp_dt; dirty = True
        if dirty:
            contact.save()
    else:
        contact = Contact.objects.create(
            first_name=first_name or "",
            last_name=last_name or "",
            nationality=nationality or None,
            date_of_birth=dob_dt,
            passport_number=passport_no or None,
            passport_expiration_date=pass_exp_dt,
            phone=phone or None,
            email=email or None,
        )
    return contact


def ensure_staff_for_contact(contact):
    staff = getattr(contact, "staff", None)
    if staff:
        return staff
    return Staff.objects.create(contact=contact, active=True)


def ensure_memberships(staff, role_codes):
    for code in role_codes:
        role = get_or_create_role(code)
        # Do not create duplicates with same open interval (start_on=None, end_on=None)
        exists = StaffRoleMembership.objects.filter(
            staff=staff, role=role, start_on=None, end_on=None
        ).exists()
        if not exists:
            StaffRoleMembership.objects.create(
                staff=staff, role=role, start_on=None, end_on=None
            )


def d(val):
    """Decimal helper for mgtow."""
    if val is None or str(val).strip() == "":
        return None
    return Decimal(str(val))


# -----------------------------
# COMMAND
# -----------------------------

class Command(BaseCommand):
    help = "Seed Aircraft and Staff (Pilots & Medics) into the database."

    def handle(self, *args, **options):
        created_aircraft = updated_aircraft = 0
        created_contacts = updated_contacts = 0
        created_staff = 0
        created_roles = 0
        created_memberships = 0  # (we won't count precisely per-row here; optional)

        # Ensure baseline roles exist (safe if already present)
        for code in set(PILOT_ROLE_CODES + MEDIC_ROLE_CODES):
            if not StaffRole.objects.filter(code=code).exists():
                StaffRole.objects.create(code=code, name=ROLE_NAMES_BY_CODE.get(code, code))
                created_roles += 1

        # --- Aircraft upsert ---
        for tail, company, make, model, serial, mgtow_lb in AIRCRAFT_ROWS:
            mgtow = d(mgtow_lb)  # store the lb number in Decimal (your field is Decimal)
            obj = Aircraft.objects.filter(tail_number=tail).first()
            if obj:
                dirty = False
                if obj.company != company:
                    obj.company = company; dirty = True
                if obj.make != make:
                    obj.make = make; dirty = True
                if obj.model != model:
                    obj.model = model; dirty = True
                if obj.serial_number != serial:
                    obj.serial_number = serial; dirty = True
                if obj.mgtow != mgtow:
                    obj.mgtow = mgtow; dirty = True
                if dirty:
                    obj.save()
                    updated_aircraft += 1
            else:
                Aircraft.objects.create(
                    tail_number=tail,
                    company=company,
                    make=make,
                    model=model,
                    serial_number=serial,
                    mgtow=mgtow,
                )
                created_aircraft += 1

        # --- Pilots ---
        for (name, nat, dob, passport_no, exp, phone, email) in PILOT_ROWS:
            contact_before = Contact.objects.filter(email=email).first()
            contact = upsert_contact(name, nat, dob, passport_no, exp, phone, email)
            if contact_before is None and contact is not None:
                created_contacts += 1
            elif contact_before is not None:
                # we may have updated fields
                updated_contacts += 0  # keep simple; adjust if you want exact diffs

            staff = ensure_staff_for_contact(contact)
            # Before creating, check how many memberships exist to approximate "created_memberships"
            pre_count = StaffRoleMembership.objects.filter(staff=staff).count()
            ensure_memberships(staff, PILOT_ROLE_CODES)
            post_count = StaffRoleMembership.objects.filter(staff=staff).count()
            created_memberships += max(0, post_count - pre_count)

        # --- Medics ---
        for (name, nat, dob, passport_no, exp, phone, email) in MEDIC_ROWS:
            contact_before = Contact.objects.filter(email=email).first()
            contact = upsert_contact(name, nat, dob, passport_no, exp, phone, email)
            if contact_before is None and contact is not None:
                created_contacts += 1
            else:
                updated_contacts += 0

            staff = ensure_staff_for_contact(contact)
            pre_count = StaffRoleMembership.objects.filter(staff=staff).count()
            ensure_memberships(staff, MEDIC_ROLE_CODES)
            post_count = StaffRoleMembership.objects.filter(staff=staff).count()
            created_memberships += max(0, post_count - pre_count)

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
        self.stdout.write(
            f"Aircraft: created={created_aircraft}, updated={updated_aircraft}\n"
            f"Contacts: created~={created_contacts}\n"
            f"Staff: ensured (created as needed)\n"
            f"Roles: created={created_roles} (only if missing)\n"
            f"Role memberships created~={created_memberships}"
        )

```


# File: api/management/commands/seed_fbos.py

```python
import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import FBO, Airport  # adjust import path if different


HEADERS = {
    "icao": ("ID", "ICAO", "Airport", "Airport ID"),
    "name": ("FBO", "Name"),
    "phone": ("PHONE", "Phone"),
    "phone2": ("PHONE2", "Phone2", "Alt Phone"),
    "email": ("Email", "E-mail"),
    "notes": ("FBO NOTES", "Notes"),
}


def pick(row, keys):
    """Return the first non-empty trimmed value from row for any of the provided keys."""
    for k in keys:
        if k in row and row[k] is not None:
            v = str(row[k]).strip()
            if v != "":
                return v
    return ""


class Command(BaseCommand):
    help = "Seed FBO records from a CSV and link them to Airports by ICAO code."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to the CSV file.")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report without writing any changes.",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing FBO phone/email/notes if new data present.",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        csv_path = Path(opts["csv_path"])
        dry_run = opts["dry_run"]
        do_update = opts["update"]

        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        created_fbos = 0
        linked_pairs = 0
        updated_fbos = 0
        skipped_rows = 0
        missing_airports = 0

        # Read CSV with BOM tolerance
        with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            # Normalize header keys once (DictReader preserves original)
            # We'll still use the HEADERS map via pick()

            for i, row in enumerate(reader, start=2):  # start=2 accounts for header row = line 1
                icao = pick(row, HEADERS["icao"]).upper()
                name = pick(row, HEADERS["name"])
                phone = pick(row, HEADERS["phone"])
                phone2 = pick(row, HEADERS["phone2"])
                email = pick(row, HEADERS["email"])
                notes = pick(row, HEADERS["notes"])

                if not icao or not name:
                    skipped_rows += 1
                    self.stdout.write(self.style.WARNING(
                        f"[line {i}] Skipped: missing required ICAO and/or FBO name."
                    ))
                    continue

                airport = Airport.objects.filter(icao_code__iexact=icao).first()
                if not airport:
                    missing_airports += 1
                    self.stdout.write(self.style.WARNING(
                        f"[line {i}] No Airport found for ICAO '{icao}'. Row skipped."
                    ))
                    continue

                # Try to find an existing FBO by name (+email/phone if available) to avoid global name collisions
                fbo_qs = FBO.objects.filter(name__iexact=name)
                if email:
                    fbo_qs = fbo_qs.filter(email__iexact=email) | fbo_qs
                if phone:
                    fbo_qs = fbo_qs.filter(phone__iexact=phone) | fbo_qs

                fbo = fbo_qs.distinct().first()

                if fbo is None:
                    # Create new FBO
                    fbo = FBO(
                        name=name,
                        phone=phone or None,
                        phone_secondary=phone2 or None,
                        email=email or None,
                        notes=notes or None,
                    )
                    if not dry_run:
                        fbo.save()
                    created_fbos += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"[line {i}] Created FBO '{name}'."
                    ))
                else:
                    # Optionally update existing with any new info provided
                    if do_update:
                        changed = False
                        if phone and fbo.phone != phone:
                            fbo.phone = phone
                            changed = True
                        if phone2 and fbo.phone_secondary != phone2:
                            fbo.phone_secondary = phone2
                            changed = True
                        if email and (fbo.email or "").lower() != email.lower():
                            fbo.email = email
                            changed = True
                        if notes and (fbo.notes or "").strip() != notes:
                            fbo.notes = notes
                            changed = True
                        if changed and not dry_run:
                            fbo.save()
                            updated_fbos += 1
                            self.stdout.write(self.style.SUCCESS(
                                f"[line {i}] Updated FBO '{name}'."
                            ))

                # Link to Airport via M2M (Airport ↔ FBO)
                if not dry_run:
                    airport.fbos.add(fbo)
                linked_pairs += 1

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN: no changes were written."))

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created FBOs: {created_fbos}, Updated: {updated_fbos}, "
            f"Linked (Airport↔FBO): {linked_pairs}, Skipped rows: {skipped_rows}, "
            f"Missing airports: {missing_airports}"
        ))

```


# File: api/management/commands/seed_dev.py

```python
# api/management/commands/seed_dev.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction, connection
from decimal import Decimal
from datetime import timedelta, datetime
from django.utils import timezone
from uuid import UUID

from api.models import (
    Permission, Role, Department, UserProfile, Contact, FBO, Ground, Airport,
    Document, Aircraft, Transaction, Agreement, Patient, Quote, Passenger,
    CrewLine, Trip, TripLine
)

def aware(dt_str: str):
    dt = datetime.fromisoformat(dt_str)
    return timezone.make_aware(dt) if timezone.is_naive(dt) else dt

class Command(BaseCommand):
    help = "Seed development/test data"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.NOTICE("Seeding data..."))

            # --- Base users for created_by/modified_by ---
            admin_user, _ = User.objects.get_or_create(
                username="admin",
                defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True}
            )
            if not admin_user.has_usable_password():
                admin_user.set_password("admin123")
                admin_user.save()

            alice_user, _ = User.objects.get_or_create(
                username="alice",
                defaults={"email": "alice@example.com", "is_staff": True}
            )
            if not alice_user.has_usable_password():
                alice_user.set_password("password123")
                alice_user.save()

            bob_user, _ = User.objects.get_or_create(
                username="bob",
                defaults={"email": "bob@example.com"}
            )
            if not bob_user.has_usable_password():
                bob_user.set_password("password123")
                bob_user.save()

            # --- Your explicit auth_user id=7 + exact hash/timestamps ---
            target_user_id = 7
            password_hash = "pbkdf2_sha256$870000$FXqSBkZnJCTre722mo1IwH$feY/56s+7Ry8EnAEmrNRFZdw0q7jZZ6KmjM6jly+R2s="
            last_login_str = "2025-08-16 16:34:56.213251"
            date_joined_str = "2025-08-16 15:54:58.108485"

            u7, created = User.objects.get_or_create(
                id=target_user_id,
                defaults=dict(
                    username="chaimkitchner",
                    email="ck@cekitch.com",
                    is_superuser=True,
                    is_staff=True,
                    is_active=True,
                    password=password_hash,
                    last_login=aware(last_login_str),
                    date_joined=aware(date_joined_str),
                ),
            )
            if not created:
                u7.username = "chaimkitchner"
                u7.email = "ck@cekitch.com"
                u7.is_superuser = True
                u7.is_staff = True
                u7.is_active = True
                u7.password = password_hash
                u7.save(update_fields=["username", "email", "is_superuser", "is_staff", "is_active", "password"])
                User.objects.filter(pk=u7.pk).update(
                    last_login=aware(last_login_str),
                    date_joined=aware(date_joined_str),
                )

            # bump sequence in Postgres so future inserts don't collide with id=7
            if connection.vendor == "postgresql":
                with connection.cursor() as cur:
                    cur.execute(
                        "SELECT setval(pg_get_serial_sequence('auth_user','id'), "
                        "(SELECT GREATEST(COALESCE(MAX(id), 1), 1) FROM auth_user))"
                    )

            # --- Matching api_userprofile record (UUID + timestamps you provided) ---
            profile_id = UUID("26e9897c-9ffe-427d-beaa-e1c6e8978f19")
            created_on_str = "2025-08-16 16:46:57.983721"
            modified_on_str = "2025-08-21 06:52:22.459238"

            up_defaults = dict(
                user=u7,
                first_name="Chaim",
                last_name="Kitchner",
                email="ck@cekitch.com",
                status="active",
                lock=False,
                created_by=u7,
                modified_by=u7,
            )
            up, up_created = UserProfile.objects.get_or_create(id=profile_id, defaults=up_defaults)
            if not up_created:
                up.user = u7
                up.first_name = "Chaim"
                up.last_name = "Kitchner"
                up.email = "ck@cekitch.com"
                up.status = "active"
                up.lock = False
                up.created_by = u7
                up.modified_by = u7
                up.save()
            UserProfile.objects.filter(pk=profile_id).update(
                created_on=aware(created_on_str),
                modified_on=aware(modified_on_str),
            )

            # --- Permissions / Roles / Departments ---
            p_view, _ = Permission.objects.get_or_create(
                name="view_quotes",
                defaults={"description": "Can view quotes", "created_by": admin_user, "modified_by": admin_user},
            )
            p_edit, _ = Permission.objects.get_or_create(
                name="edit_quotes",
                defaults={"description": "Can edit quotes", "created_by": admin_user, "modified_by": admin_user},
            )
            p_trips, _ = Permission.objects.get_or_create(
                name="manage_trips",
                defaults={"description": "Can manage trips", "created_by": admin_user, "modified_by": admin_user},
            )

            role_admin, _ = Role.objects.get_or_create(
                name="Admin",
                defaults={"description": "Admin role", "created_by": admin_user, "modified_by": admin_user},
            )
            role_admin.permissions.set([p_view, p_edit, p_trips])

            role_ops, _ = Role.objects.get_or_create(
                name="Dispatcher",
                defaults={"description": "Operations/Dispatcher", "created_by": admin_user, "modified_by": admin_user},
            )
            role_ops.permissions.set([p_view, p_trips])

            dept_ops, _ = Department.objects.get_or_create(
                name="Operations",
                defaults={"description": "Ops department", "created_by": admin_user, "modified_by": admin_user},
            )
            dept_med, _ = Department.objects.get_or_create(
                name="Medical",
                defaults={"description": "Medical department", "created_by": admin_user, "modified_by": admin_user},
            )
            dept_ops.permission_ids.set([p_view, p_trips, p_edit])
            dept_med.permission_ids.set([p_view])

            # hook M2Ms for user profiles
            up.roles.set([role_admin])
            up.departments.set([dept_ops])
            up.department_ids.set([dept_ops])

            # --- Contacts (pilots/medic/customer) ---
            pilot1, _ = Contact.objects.get_or_create(
                first_name="Pat", last_name="Pilot",
                defaults={"email": "pat.pilot@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            pilot2, _ = Contact.objects.get_or_create(
                first_name="Sam", last_name="Second",
                defaults={"email": "sam.second@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            medic1, _ = Contact.objects.get_or_create(
                first_name="Rory", last_name="RN",
                defaults={"email": "rory.rn@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            customer, _ = Contact.objects.get_or_create(
                business_name="Oceanic Cruises",
                defaults={"email": "ops@oceanic.example.com", "created_by": admin_user, "modified_by": admin_user},
            )

            # --- FBO / Ground / Airports ---
            fbo_jfk, _ = FBO.objects.get_or_create(
                name="Signature JFK",
                defaults={"city": "New York", "state": "NY", "created_by": admin_user, "modified_by": admin_user},
            )
            fbo_jfk.contacts.set([pilot1])

            ground_lax, _ = Ground.objects.get_or_create(
                name="LAX Limo",
                defaults={"city": "Los Angeles", "state": "CA", "created_by": admin_user, "modified_by": admin_user},
            )
            ground_lax.contacts.set([customer])

            jfk, _ = Airport.objects.get_or_create(
                icao_code="KJFK",
                defaults=dict(
                    iata_code="JFK", name="John F. Kennedy International", city="New York",
                    state="NY", country="USA", elevation=13,
                    latitude=Decimal("40.641311"), longitude=Decimal("-73.778139"),
                    timezone="America/New_York", created_by=admin_user, modified_by=admin_user
                ),
            )
            lax, _ = Airport.objects.get_or_create(
                icao_code="KLAX",
                defaults=dict(
                    iata_code="LAX", name="Los Angeles International", city="Los Angeles",
                    state="CA", country="USA", elevation=125,
                    latitude=Decimal("33.941589"), longitude=Decimal("-118.408530"),
                    timezone="America/Los_Angeles", created_by=admin_user, modified_by=admin_user
                ),
            )
            jfk.fbos.add(fbo_jfk)
            lax.grounds.add(ground_lax)

            # --- Aircraft ---
            aircraft, _ = Aircraft.objects.get_or_create(
                tail_number="N123AB",
                defaults=dict(
                    company="Airmed Partners", mgtow=Decimal("21500.00"),
                    make="Learjet", model="35A", serial_number="LJ35-0001",
                    created_by=admin_user, modified_by=admin_user
                ),
            )

            # --- Documents & Agreements ---
            pdf_bytes = b"%PDF-1.4 test\n%%EOF"
            doc_quote, _ = Document.objects.get_or_create(filename="quote.pdf", defaults={"content": pdf_bytes})
            doc_agree, _ = Document.objects.get_or_create(filename="agreement.pdf", defaults={"content": pdf_bytes})
            doc_passport, _ = Document.objects.get_or_create(filename="passport.jpg", defaults={"content": b'\x00\x01TEST'})

            agreement_payment, _ = Agreement.objects.get_or_create(
                destination_email="billing@oceanic.example.com",
                defaults={"document_unsigned": doc_agree, "status": "created",
                          "created_by": admin_user, "modified_by": admin_user},
            )
            agreement_consent, _ = Agreement.objects.get_or_create(
                destination_email="consent@oceanic.example.com",
                defaults={"document_unsigned": doc_agree, "status": "created",
                          "created_by": admin_user, "modified_by": admin_user},
            )

            # --- Patient / Passengers ---
            patient_contact, _ = Contact.objects.get_or_create(
                first_name="Jamie", last_name="Doe",
                defaults={"email": "jamie@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            patient, _ = Patient.objects.get_or_create(
                info=patient_contact,
                defaults=dict(
                    bed_at_origin=True, bed_at_destination=False,
                    date_of_birth=timezone.now().date().replace(year=1988),
                    nationality="USA", passport_number="X1234567",
                    passport_expiration_date=timezone.now().date().replace(year=2032),
                    passport_document=doc_passport, status="pending",
                    created_by=admin_user, modified_by=admin_user
                ),
            )

            pax_contact1, _ = Contact.objects.get_or_create(
                first_name="Alex", last_name="Doe",
                defaults={"email": "alex@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            pax1, _ = Passenger.objects.get_or_create(
                info=pax_contact1,
                defaults=dict(
                    nationality="USA", passport_number="PAX001",
                    passport_expiration_date=timezone.now().date().replace(year=2030),
                    contact_number="+1-555-0110", passport_document=doc_passport,
                    created_by=admin_user, modified_by=admin_user
                ),
            )

            pax_contact2, _ = Contact.objects.get_or_create(
                first_name="Taylor", last_name="Smith",
                defaults={"email": "taylor@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            pax2, _ = Passenger.objects.get_or_create(
                info=pax_contact2,
                defaults=dict(
                    nationality="USA", passport_number="PAX002",
                    passport_expiration_date=timezone.now().date().replace(year=2031),
                    contact_number="+1-555-0111", passport_document=doc_passport,
                    created_by=admin_user, modified_by=admin_user
                ),
            )
            pax1.passenger_ids.add(pax2)

            # --- Crew Line ---
            crew, _ = CrewLine.objects.get_or_create(
                primary_in_command=pilot1,
                secondary_in_command=pilot2,
                defaults={"created_by": admin_user, "modified_by": admin_user},
            )
            crew.medic_ids.set([medic1])

            # --- Quote ---
            quote, _ = Quote.objects.get_or_create(
                contact=customer, pickup_airport=jfk, dropoff_airport=lax,
                defaults=dict(
                    quoted_amount=Decimal("45999.00"),
                    aircraft_type="35",
                    estimated_flight_time=timedelta(hours=5, minutes=30),
                    includes_grounds=True, inquiry_date=timezone.now(),
                    medical_team="RN/Paramedic", patient=patient,
                    status="pending", number_of_stops=1,
                    quote_pdf=doc_quote, quote_pdf_status="created",
                    quote_pdf_email="quotes@airmed.example.com",
                    payment_agreement=agreement_payment,
                    consent_for_transport=agreement_consent,
                    created_by=admin_user, modified_by=admin_user
                ),
            )
            quote.documents.set([doc_quote])

            # --- Transaction ---
            txn, _ = Transaction.objects.get_or_create(
                email="payer@oceanic.example.com",
                amount=Decimal("10000.00"),
                payment_method="credit_card",
                defaults=dict(
                    payment_status="completed",
                    payment_date=timezone.now(),
                    created_by=admin_user, modified_by=admin_user
                ),
            )
            quote.transactions.add(txn)

            # --- Trip + legs ---
            trip, _ = Trip.objects.get_or_create(
                trip_number="TRIP-0001",
                defaults=dict(
                    email_chain=[], quote=quote, type="medical", patient=patient,
                    estimated_departure_time=timezone.now() + timedelta(days=3, hours=2),
                    post_flight_duty_time=timedelta(hours=2),
                    pre_flight_duty_time=timedelta(hours=1),
                    aircraft=aircraft,
                    internal_itinerary=doc_quote,
                    customer_itinerary=doc_quote,
                    created_by=admin_user, modified_by=admin_user
                ),
            )
            trip.passengers.set([pax1, pax2])

            dep_utc = timezone.now() + timedelta(days=3, hours=2)
            arr_utc = dep_utc + timedelta(hours=6)
            TripLine.objects.get_or_create(
                trip=trip, origin_airport=jfk, destination_airport=lax,
                departure_time_local=dep_utc, departure_time_utc=dep_utc,
                arrival_time_local=arr_utc, arrival_time_utc=arr_utc,
                defaults=dict(
                    crew_line=crew, distance=Decimal("2475.50"),
                    flight_time=timedelta(hours=6), ground_time=timedelta(minutes=45),
                    passenger_leg=True, created_by=admin_user, modified_by=admin_user
                ),
            )

            dep2 = arr_utc + timedelta(hours=2)
            arr2 = dep2 + timedelta(hours=5, minutes=45)
            TripLine.objects.get_or_create(
                trip=trip, origin_airport=lax, destination_airport=jfk,
                departure_time_local=dep2, departure_time_utc=dep2,
                arrival_time_local=arr2, arrival_time_utc=arr2,
                defaults=dict(
                    crew_line=crew, distance=Decimal("2475.50"),
                    flight_time=timedelta(hours=5, minutes=45), ground_time=timedelta(minutes=30),
                    passenger_leg=True, created_by=admin_user, modified_by=admin_user
                ),
            )

            self.stdout.write(self.style.SUCCESS("✅ Seed complete."))
            self.stdout.write(self.style.SUCCESS("Users: admin/admin123; alice/bob with password123"))
            self.stdout.write(self.style.SUCCESS("Custom user id=7: chaimkitchner (pre-hashed)"))

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
