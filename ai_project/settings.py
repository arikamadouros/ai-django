from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-replace-this-with-a-unique-key'

DEBUG = True

ALLOWED_HOSTS = [
  '*',
  'localhost',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bot',
    'openai_integration',
    'searchai_integration',
    'ai_integration',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ai_project.urls'
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://0.0.0.0:8000']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ai_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AZURE Integration Variables
AZURE_OPENAI_API_BASE = config("AZURE_OPENAI_API_BASE")
AZURE_OPENAI_API_KEY = config("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT_NAME = config("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = config("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_CONTENT_TYPE = config("AZURE_OPENAI_CONTENT_TYPE")
AZURE_OPENAI_COMPLETION = config("AZURE_OPENAI_COMPLETION")
SEARCH_ENDPOINT=config("SEARCH_ENDPOINT")
SEARCH_API_KEY=config("SEARCH_API_KEY")
SEARCH_VERSION=config("SEARCH_VERSION")
SEARCH_CONTENT_TYPE=config("SEARCH_CONTENT_TYPE")