# Project Structure

The following is the structure of the project:

```
backend/
    prompt2.py
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
        __init__.py
        0001_initial.py
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
    status = models.CharField(max_length=50, default="active")
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
    permission_ids = models.ManyToManyField(Permission, related_name="contacts")
    
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
    permission_ids = models.ManyToManyField(Permission, related_name="fbos")
    
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
    permission_ids = models.ManyToManyField(Permission, related_name="grounds")
    
    def __str__(self):
        return self.name

# Airport model
class Airport(BaseModel):
    icao_code = models.CharField(max_length=4)
    iata_code = models.CharField(max_length=3)
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
    permission_ids = models.ManyToManyField(Permission, related_name="airports")
    
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
    tail_number = models.CharField(max_length=20)
    company = models.CharField(max_length=255)
    mgtow = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maximum Gross Takeoff Weight")
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.tail_number} - {self.make} {self.model}"

# Transaction model
class Transaction(BaseModel):
    key = models.UUIDField(default=uuid.uuid4, editable=False)
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
    document_unsigned_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="unsigned_agreements")
    document_signed_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="signed_agreements")
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
    passport_document_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_patients")
    special_instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ], default="pending")
    letter_of_medical_necessity_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="medical_necessity_patients")
    
    def __str__(self):
        return f"Patient: {self.info}"

# Quote model
class Quote(BaseModel):
    quoted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="quotes")
    documents = models.ManyToManyField(Document, related_name="quotes")
    cruise_doctor_first_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_doctor_last_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_line = models.CharField(max_length=100, blank=True, null=True)
    cruise_ship = models.CharField(max_length=100, blank=True, null=True)
    pickup_airport_id = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="pickup_quotes")
    dropoff_airport_id = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="dropoff_quotes")
    aircraft_type = models.CharField(max_length=20, choices=[
        ("65", "Learjet 65"),
        ("35", "Learjet 35"),
        ("TBD", "To Be Determined")
    ])
    estimated_fight_time = models.DecimalField(max_digits=5, decimal_places=2)
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
    patient_first_name = models.CharField(max_length=100, blank=True, null=True)
    patient_last_name = models.CharField(max_length=100, blank=True, null=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="quotes")
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("paid", "Paid")
    ], default="pending")
    number_of_stops = models.PositiveIntegerField(default=0)
    quote_pdf_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="quote_pdfs")
    quote_pdf_status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("modified", "Modified"),
        ("accepted", "Accepted"),
        ("denied", "Denied")
    ], default="created")
    quote_pdf_email = models.EmailField()
    payment_agreement_id = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="payment_quotes")
    consent_for_transport_id = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="consent_quotes")
    patient_service_agreement_id = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="service_quotes")
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
    passport_document_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_passengers")
    
    def __str__(self):
        return f"Passenger: {self.info}"

# Crew Line model
class CrewLine(BaseModel):
    primary_in_command_id = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="primary_crew_lines")
    secondary_in_command_id = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="secondary_crew_lines")
    medic_ids = models.ManyToManyField(Contact, related_name="medic_crew_lines")
    
    def __str__(self):
        return f"Crew: {self.primary_in_command_id} and {self.secondary_in_command_id}"

# Trip model
class Trip(BaseModel):
    email_chain = models.JSONField(default=list, blank=True)
    quote_id = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="trips", null=True, blank=True)
    type = models.CharField(max_length=20, choices=[
        ("medical", "Medical"),
        ("charter", "Charter"),
        ("part 91", "Part 91"),
        ("other", "Other"),
        ("maintenance", "Maintenance")
    ])
    patient_id = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips")
    estimated_departure_time = models.DateTimeField(blank=True, null=True)
    post_flight_duty_time = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pre_flight_duty_time = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    aircraft_id = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips")
    trip_number = models.CharField(max_length=20)
    internal_itinerary_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="internal_itinerary_trips")
    customer_itinerary_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_itinerary_trips")
    passengers = models.ManyToManyField(Passenger, related_name="trips", blank=True)
    
    def __str__(self):
        return f"Trip {self.trip_number} - {self.type}"

# Trip Line model
class TripLine(BaseModel):
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_lines")
    origin_airport_id = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="origin_trip_lines")
    destination_airport_id = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="destination_trip_lines")
    crew_line_id = models.ForeignKey(CrewLine, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_lines")
    departure_time_local = models.DateTimeField()
    departure_time_utc = models.DateTimeField()
    arrival_time_local = models.DateTimeField()
    arrival_time_utc = models.DateTimeField()
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    flight_time = models.DecimalField(max_digits=5, decimal_places=2)
    ground_time = models.DecimalField(max_digits=5, decimal_places=2)
    passenger_leg = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Trip Line: {self.origin_airport_id} to {self.destination_airport_id}"
    
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
        read_only_fields = ['is_staff']

# Base serializers
class ModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modification
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'

# Contact and location serializers
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class FBOSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBO
        fields = '__all__'

class GroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ground
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

# Document serializer
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'filename', 'flag', 'created_on']

class DocumentUploadSerializer(serializers.ModelSerializer):
    content = serializers.FileField()
    
    class Meta:
        model = Document
        fields = ['id', 'filename', 'content', 'flag']

# Aircraft serializer
class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'

# Transaction serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

# Agreement serializer
class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = '__all__'

# Patient serializer
class PatientSerializer(serializers.ModelSerializer):
    info = ContactSerializer(read_only=True)
    info_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        source='info',
        write_only=True
    )
    
    class Meta:
        model = Patient
        fields = '__all__'

# Quote serializer
class QuoteSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(source='contact_id', read_only=True)
    
    class Meta:
        model = Quote
        fields = '__all__'

# Passenger serializer
class PassengerSerializer(serializers.ModelSerializer):
    info = ContactSerializer(read_only=True)
    
    class Meta:
        model = Passenger
        fields = '__all__'

# Crew Line serializer
class CrewLineSerializer(serializers.ModelSerializer):
    primary_in_command = ContactSerializer(source='primary_in_command_id', read_only=True)
    secondary_in_command = ContactSerializer(source='secondary_in_command_id', read_only=True)
    medics = ContactSerializer(source='medic_ids', many=True, read_only=True)
    
    class Meta:
        model = CrewLine
        fields = '__all__'

# Trip serializer
class TripLineSerializer(serializers.ModelSerializer):
    origin_airport = AirportSerializer(source='origin_airport_id', read_only=True)
    destination_airport = AirportSerializer(source='destination_airport_id', read_only=True)
    crew_line = CrewLineSerializer(source='crew_line_id', read_only=True)
    
    class Meta:
        model = TripLine
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    quote = QuoteSerializer(source='quote_id', read_only=True)
    patient = PatientSerializer(source='patient_id', read_only=True)
    aircraft = AircraftSerializer(source='aircraft_id', read_only=True)
    trip_lines = TripLineSerializer(many=True, read_only=True)
    passengers_data = PassengerSerializer(source='passengers', many=True, read_only=True)
    
    class Meta:
        model = Trip
        fields = '__all__'

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
    UserProfileSerializer, ContactSerializer, FBOSerializer, GroundSerializer,
    AirportSerializer, DocumentSerializer, DocumentUploadSerializer, AircraftSerializer,
    TransactionSerializer, AgreementSerializer, PatientSerializer, QuoteSerializer,
    PassengerSerializer, CrewLineSerializer, TripSerializer, TripLineSerializer
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
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'created_on']
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
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
    serializer_class = DocumentSerializer
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return DocumentUploadSerializer
        return DocumentSerializer
    
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
    serializer_class = TransactionSerializer
    search_fields = ['key', 'email', 'payment_status']
    ordering_fields = ['payment_date', 'amount', 'created_on']
    permission_classes = [
        IsAuthenticatedOrPublicEndpoint, 
        IsTransactionOwner,
        CanReadTransaction | CanWriteTransaction | CanModifyTransaction | CanDeleteTransaction
    ]
    public_actions = ['retrieve_by_key']
    
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
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    search_fields = ['info__first_name', 'info__last_name', 'nationality']
    ordering_fields = ['created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadPatient | CanWritePatient | CanModifyPatient | CanDeletePatient
    ]
    
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
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    search_fields = ['contact_id__first_name', 'contact_id__last_name', 'status']
    ordering_fields = ['created_on', 'quoted_amount']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadQuote | CanWriteQuote | CanModifyQuote | CanDeleteQuote
    ]
    
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
        
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

# Passenger ViewSet
class PassengerViewSet(BaseViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    search_fields = ['info__first_name', 'info__last_name', 'nationality']
    ordering_fields = ['created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadPassenger | CanWritePassenger | CanModifyPassenger | CanDeletePassenger
    ]
    
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
    queryset = CrewLine.objects.all()
    serializer_class = CrewLineSerializer
    ordering_fields = ['created_on']

# Trip ViewSet
class TripViewSet(BaseViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    search_fields = ['trip_number', 'type']
    ordering_fields = ['created_on', 'estimated_departure_time']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadTrip | CanWriteTrip | CanModifyTrip | CanDeleteTrip
    ]
    
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
        serializer = TripLineSerializer(trip_lines, many=True)
        return Response(serializer.data)

# TripLine ViewSet
class TripLineViewSet(BaseViewSet):
    queryset = TripLine.objects.all()
    serializer_class = TripLineSerializer
    ordering_fields = ['departure_time_utc', 'created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadTripLine | CanWriteTripLine | CanModifyTripLine | CanDeleteTripLine
    ]
    
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
        trip = trip_line.trip_id
        
        # Recalculate times for all trip lines in this trip
        if trip.estimated_departure_time:
            self.recalculate_trip_times(trip)
    
    def perform_update(self, serializer):
        trip_line = serializer.save()
        trip = trip_line.trip_id
        
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
