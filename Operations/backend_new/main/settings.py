from pathlib import Path

from datetime import timedelta
import os

# OURS
from Operations.backend.backend.settings import CORS_ALLOW_CREDENTIALS
from utils import Settings




BASE_DIR = Path(__file__).resolve().parent.parent

# TODO ENSURE WE STILL NEED
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




SECRET_KEY = Settings.SECRET_KEY
ENCRYPTION_KEY = Settings.ENCRYPTION_KEY
DEBUG = Settings.DEBUG
ALLOWED_HOSTS = Settings.ALLOWED_HOSTS


# SECURITY WARNING: don't run with debug turned on in production!



## Application definition

INSTALLED_APPS = [
    # DEFAULTS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # EXTERN
    'rest_framework',
    'django_filters',
    'corsheaders',
    # INTERNAL
    'operations',
    'users'
]


# TODO VERIFY
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'api.middleware.CurrentUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

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

WSGI_APPLICATION = 'main.wsgi.application'


## Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': Settings.DB_NAME,
        'USER': Settings.DB_USER,
        'PASSWORD': Settings.DB_PASSWORD,
        'HOST': Settings.DB_HOST,
        'PORT': Settings.DB_PORT,
    }
}


## Password validation
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


## Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


## CORS SETTINGS
# allow all origins if no allowed hosts else only allow hosts specified in env
CORS_ALLOW_ALL_ORIGINS = True if not Settings.ALLOWED_HOSTS else False 
CORS_ALLOW_CREDENTIALS = True

# CRSF SETTINGS
CRSF_TRUSTED_ORIGINS = Settings.CSRF_TRUSTED_ORIGINS

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

# JWT settings (auth)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# DOCUSEAL INTEGRATION
DOCUSEAL_API_KEY = 