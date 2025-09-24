IS_IN_DEVELOPMENT = True


import os
from pathlib import Path
from datetime import timedelta


# HELPER
def _get_env(key: str, default=None):
    result = os.environ.get(key, default)
    if result == None:
        raise KeyError(f"{key} not set in {Path(__file__).resolve()}")
    return result


BASE_DIR = Path(__file__).resolve().parent.parent

if IS_IN_DEVELOPMENT:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = _get_env('SECRET_KEY')
ENCRYPTION_KEY = _get_env('ENCRYPTION_KEY')
DEBUG = 'True' if IS_IN_DEVELOPMENT == True else 'False'
ALLOWED_HOSTS = _get_env('ALLOWED_HOSTS').split(',')
ALLOWED_PORTS = _get_env('ALLOWED_PORTS').split(',')

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = 'true'
EMAIL_USE_SSL = 'true'

EMAIL_USER = _get_env('EMAIL_USER', 'noreply@jeticu.com')
EMAIL_PASS = _get_env('EMAIL_PASS')
EMAIL_FROM = _get_env('EMAIL_FROM', 'noreply@jeticu.com')

# for activation links
FRONTEND_URL = 'https://jeticuops.com'

# Application definitions
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    'django_filters',
    'corsheaders',
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

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _get_env("DB_NAME"),
        "USER": _get_env("DB_USER"),
        "PASSWORD": _get_env("DB_PASS"),
        # If Django is running on your Mac (outside Docker), use localhost:
        "HOST": _get_env("DB_HOST", "localhost"),
        "PORT": _get_env("DB_PORT", "5432"),
    }
}

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

# INTERNALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CORS SETTINGS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = []
for host in ALLOWED_HOSTS:
    CORS_ALLOWED_ORIGINS.append(f"https://{host}")
    for port in ALLOWED_PORTS:
        CORS_ALLOWED_ORIGINS.append(f"http://{host}:{port}")

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

# REST Settings
EST_FRAMEWORK = {
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

# AUTHORIZE.NET
AUTH_NET_LOGIN_ID = _get_env('AUTH_NET_LOGIN_ID')
AUTH_NET_TRANSACTION_ID = _get_env('AUTH_NET_TRANSACTION_ID')

# DOCUSEAL settings
DOCUSEAL_API_KEY = _get_env('DOCUSEAL_API_KEY')
DOCUSEAL_BASE_URL = _get_env('DOCUSEAL_BASE_URL', 'https://api.docuseal.com')
DOCUSEAL_WEBHOOK_SECRET = _get_env('DOCUSEAL_WEBHOOK_SECRET')
DOCUSEAL_INTERNAL_SIGNER = _get_env('DOCUSEAL_INTERNAL_SIGNER')
DOCUSEAL_CONTRACT_SETTINGS = {
    'default_expiration_days': 30,
    'send_email_notifications': True,
    'auto_generate_on_trip_creation': True,
    'templates': {
        'consent_transport': {
            'template_id': '1712631',
            'name': 'Consent for Transport',
            'requires_jet_icu_signature': True,  # JET ICU needs to be involved for field data
            'customer_role': 'patient',       # Customer signs as patient
            'jet_icu_role': 'jet_icu',        # JET ICU gets the field data
        },
        'payment_agreement': {
            'template_id': '1712677',
            'name': 'Air Ambulance Payment Agreement',
            'requires_jet_icu_signature': True,
            'customer_role': 'customer',      # Customer signs as customer
            'jet_icu_role': 'jet_icu',        # JET ICU signs as jet_icu (gets the field data)
        },
        'patient_service_agreement': {
            'template_id': '1712724',
            'name': 'Patient Service Agreement',
            'requires_jet_icu_signature': True,
            'customer_role': 'patient',       # Customer signs as patient
            'jet_icu_role': 'jet_icu',        # JET ICU signs as jet_icu (gets the field data)
        }
    }
}
