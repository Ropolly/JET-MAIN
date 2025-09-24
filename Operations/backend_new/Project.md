```
backend_new/
├── 📎 .python-version
├── 📂 core/
│   ├── 🐍 __init__.py
│   ├── 🐍 asgi.py
│   ├── 🐍 settings.py
│   ├── 🐍 urls.py
│   └── 🐍 wsgi.py
├── 📂 dev/

├── 🐍 manage.py
├── ⚙️ pyproject.toml
└── 📎 uv.lock
```

# 📂 backend_new

#### 📎 .python-version

```
3.13

```

## 📂 core

#### 🐍 __init__.py

```python

```

#### 🐍 asgi.py

```python
"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = get_asgi_application()

```

#### 🐍 settings.py

```python
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
    'django.contrib.staticfiles',
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
    'api.middleware.CurrentUserMiddleware',
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

```

#### 🐍 urls.py

```python
"""
URL configuration for main project.

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
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

```

#### 🐍 wsgi.py

```python
"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

```

## 📂 dev

#### 🐍 manage.py

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
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

#### ⚙️ pyproject.toml

```toml
[project]
name = "backend-new"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "django>=5.2.6",
    "django-cors-headers>=4.9.0",
    "django-filter>=25.1",
    "djangorestframework>=3.16.1",
    "djangorestframework-simplejwt>=5.5.1",
    "dotenv>=0.9.9",
    "psycopg2[binary]>=2.9.10",
]

```

#### 📎 uv.lock

```
version = 1
revision = 3
requires-python = ">=3.13"

[[package]]
name = "asgiref"
version = "3.9.2"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/7f/bf/0f3ecda32f1cb3bf1dca480aca08a7a8a3bdc4bed2343a103f30731565c9/asgiref-3.9.2.tar.gz", hash = "sha256:a0249afacb66688ef258ffe503528360443e2b9a8d8c4581b6ebefa58c841ef1", size = 36894, upload-time = "2025-09-23T15:00:55.136Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/c7/d1/69d02ce34caddb0a7ae088b84c356a625a93cd4ff57b2f97644c03fad905/asgiref-3.9.2-py3-none-any.whl", hash = "sha256:0b61526596219d70396548fc003635056856dba5d0d086f86476f10b33c75960", size = 23788, upload-time = "2025-09-23T15:00:53.627Z" },
]

[[package]]
name = "backend-new"
version = "0.1.0"
source = { virtual = "." }
dependencies = [
    { name = "django" },
    { name = "django-cors-headers" },
    { name = "django-filter" },
    { name = "djangorestframework" },
    { name = "djangorestframework-simplejwt" },
    { name = "dotenv" },
    { name = "psycopg2" },
]

[package.metadata]
requires-dist = [
    { name = "django", specifier = ">=5.2.6" },
    { name = "django-cors-headers", specifier = ">=4.9.0" },
    { name = "django-filter", specifier = ">=25.1" },
    { name = "djangorestframework", specifier = ">=3.16.1" },
    { name = "djangorestframework-simplejwt", specifier = ">=5.5.1" },
    { name = "dotenv", specifier = ">=0.9.9" },
    { name = "psycopg2", extras = ["binary"], specifier = ">=2.9.10" },
]

[[package]]
name = "django"
version = "5.2.6"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "asgiref" },
    { name = "sqlparse" },
    { name = "tzdata", marker = "sys_platform == 'win32'" },
]
sdist = { url = "https://files.pythonhosted.org/packages/4c/8c/2a21594337250a171d45dda926caa96309d5136becd1f48017247f9cdea0/django-5.2.6.tar.gz", hash = "sha256:da5e00372763193d73cecbf71084a3848458cecf4cee36b9a1e8d318d114a87b", size = 10858861, upload-time = "2025-09-03T13:04:03.23Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/f5/af/6593f6d21404e842007b40fdeb81e73c20b6649b82d020bb0801b270174c/django-5.2.6-py3-none-any.whl", hash = "sha256:60549579b1174a304b77e24a93d8d9fafe6b6c03ac16311f3e25918ea5a20058", size = 8303111, upload-time = "2025-09-03T13:03:47.808Z" },
]

[[package]]
name = "django-cors-headers"
version = "4.9.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "asgiref" },
    { name = "django" },
]
sdist = { url = "https://files.pythonhosted.org/packages/21/39/55822b15b7ec87410f34cd16ce04065ff390e50f9e29f31d6d116fc80456/django_cors_headers-4.9.0.tar.gz", hash = "sha256:fe5d7cb59fdc2c8c646ce84b727ac2bca8912a247e6e68e1fb507372178e59e8", size = 21458, upload-time = "2025-09-18T10:40:52.326Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/30/d8/19ed1e47badf477d17fb177c1c19b5a21da0fd2d9f093f23be3fb86c5fab/django_cors_headers-4.9.0-py3-none-any.whl", hash = "sha256:15c7f20727f90044dcee2216a9fd7303741a864865f0c3657e28b7056f61b449", size = 12809, upload-time = "2025-09-18T10:40:50.843Z" },
]

[[package]]
name = "django-filter"
version = "25.1"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "django" },
]
sdist = { url = "https://files.pythonhosted.org/packages/b5/40/c702a6fe8cccac9bf426b55724ebdf57d10a132bae80a17691d0cf0b9bac/django_filter-25.1.tar.gz", hash = "sha256:1ec9eef48fa8da1c0ac9b411744b16c3f4c31176c867886e4c48da369c407153", size = 143021, upload-time = "2025-02-14T16:30:53.238Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/07/a6/70dcd68537c434ba7cb9277d403c5c829caf04f35baf5eb9458be251e382/django_filter-25.1-py3-none-any.whl", hash = "sha256:4fa48677cf5857b9b1347fed23e355ea792464e0fe07244d1fdfb8a806215b80", size = 94114, upload-time = "2025-02-14T16:30:50.435Z" },
]

[[package]]
name = "djangorestframework"
version = "3.16.1"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "django" },
]
sdist = { url = "https://files.pythonhosted.org/packages/8a/95/5376fe618646fde6899b3cdc85fd959716bb67542e273a76a80d9f326f27/djangorestframework-3.16.1.tar.gz", hash = "sha256:166809528b1aced0a17dc66c24492af18049f2c9420dbd0be29422029cfc3ff7", size = 1089735, upload-time = "2025-08-06T17:50:53.251Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/b0/ce/bf8b9d3f415be4ac5588545b5fcdbbb841977db1c1d923f7568eeabe1689/djangorestframework-3.16.1-py3-none-any.whl", hash = "sha256:33a59f47fb9c85ede792cbf88bde71893bcda0667bc573f784649521f1102cec", size = 1080442, upload-time = "2025-08-06T17:50:50.667Z" },
]

[[package]]
name = "djangorestframework-simplejwt"
version = "5.5.1"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "django" },
    { name = "djangorestframework" },
    { name = "pyjwt" },
]
sdist = { url = "https://files.pythonhosted.org/packages/a8/27/2874a325c11112066139769f7794afae238a07ce6adf96259f08fd37a9d7/djangorestframework_simplejwt-5.5.1.tar.gz", hash = "sha256:e72c5572f51d7803021288e2057afcbd03f17fe11d484096f40a460abc76e87f", size = 101265, upload-time = "2025-07-21T16:52:25.026Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/60/94/fdfb7b2f0b16cd3ed4d4171c55c1c07a2d1e3b106c5978c8ad0c15b4a48b/djangorestframework_simplejwt-5.5.1-py3-none-any.whl", hash = "sha256:2c30f3707053d384e9f315d11c2daccfcb548d4faa453111ca19a542b732e469", size = 107674, upload-time = "2025-07-21T16:52:07.493Z" },
]

[[package]]
name = "dotenv"
version = "0.9.9"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "python-dotenv" },
]
wheels = [
    { url = "https://files.pythonhosted.org/packages/b2/b7/545d2c10c1fc15e48653c91efde329a790f2eecfbbf2bd16003b5db2bab0/dotenv-0.9.9-py2.py3-none-any.whl", hash = "sha256:29cf74a087b31dafdb5a446b6d7e11cbce8ed2741540e2339c69fbef92c94ce9", size = 1892, upload-time = "2025-02-19T22:15:01.647Z" },
]

[[package]]
name = "psycopg2"
version = "2.9.10"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/62/51/2007ea29e605957a17ac6357115d0c1a1b60c8c984951c19419b3474cdfd/psycopg2-2.9.10.tar.gz", hash = "sha256:12ec0b40b0273f95296233e8750441339298e6a572f7039da5b260e3c8b60e11", size = 385672, upload-time = "2024-10-16T11:24:54.832Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/ae/49/a6cfc94a9c483b1fa401fbcb23aca7892f60c7269c5ffa2ac408364f80dc/psycopg2-2.9.10-cp313-cp313-win_amd64.whl", hash = "sha256:91fd603a2155da8d0cfcdbf8ab24a2d54bca72795b90d2a3ed2b6da8d979dee2", size = 2569060, upload-time = "2025-01-04T20:09:15.28Z" },
]

[[package]]
name = "pyjwt"
version = "2.10.1"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/e7/46/bd74733ff231675599650d3e47f361794b22ef3e3770998dda30d3b63726/pyjwt-2.10.1.tar.gz", hash = "sha256:3cc5772eb20009233caf06e9d8a0577824723b44e6648ee0a2aedb6cf9381953", size = 87785, upload-time = "2024-11-28T03:43:29.933Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/61/ad/689f02752eeec26aed679477e80e632ef1b682313be70793d798c1d5fc8f/PyJWT-2.10.1-py3-none-any.whl", hash = "sha256:dcdd193e30abefd5debf142f9adfcdd2b58004e644f25406ffaebd50bd98dacb", size = 22997, upload-time = "2024-11-28T03:43:27.893Z" },
]

[[package]]
name = "python-dotenv"
version = "1.1.1"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/f6/b0/4bc07ccd3572a2f9df7e6782f52b0c6c90dcbb803ac4a167702d7d0dfe1e/python_dotenv-1.1.1.tar.gz", hash = "sha256:a8a6399716257f45be6a007360200409fce5cda2661e3dec71d23dc15f6189ab", size = 41978, upload-time = "2025-06-24T04:21:07.341Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/5f/ed/539768cf28c661b5b068d66d96a2f155c4971a5d55684a514c1a0e0dec2f/python_dotenv-1.1.1-py3-none-any.whl", hash = "sha256:31f23644fe2602f88ff55e1f5c79ba497e01224ee7737937930c448e4d0e24dc", size = 20556, upload-time = "2025-06-24T04:21:06.073Z" },
]

[[package]]
name = "sqlparse"
version = "0.5.3"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/e5/40/edede8dd6977b0d3da179a342c198ed100dd2aba4be081861ee5911e4da4/sqlparse-0.5.3.tar.gz", hash = "sha256:09f67787f56a0b16ecdbde1bfc7f5d9c3371ca683cfeaa8e6ff60b4807ec9272", size = 84999, upload-time = "2024-12-10T12:05:30.728Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/a9/5c/bfd6bd0bf979426d405cc6e71eceb8701b148b16c21d2dc3c261efc61c7b/sqlparse-0.5.3-py3-none-any.whl", hash = "sha256:cf2196ed3418f3ba5de6af7e82c694a9fbdbfecccdfc72e281548517081f16ca", size = 44415, upload-time = "2024-12-10T12:05:27.824Z" },
]

[[package]]
name = "tzdata"
version = "2025.2"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/95/32/1a225d6164441be760d75c2c42e2780dc0873fe382da3e98a2e1e48361e5/tzdata-2025.2.tar.gz", hash = "sha256:b60a638fcc0daffadf82fe0f57e53d06bdec2f36c4df66280ae79bce6bd6f2b9", size = 196380, upload-time = "2025-03-23T13:54:43.652Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/5c/23/c7abc0ca0a1526a0774eca151daeb8de62ec457e77262b66b359c3c7679e/tzdata-2025.2-py2.py3-none-any.whl", hash = "sha256:1a403fada01ff9221ca8044d701868fa132215d84beb92242d9acd2147f667a8", size = 347839, upload-time = "2025-03-23T13:54:41.845Z" },
]

```