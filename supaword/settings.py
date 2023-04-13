import os
import mimetypes

from django.contrib import staticfiles
from django.core.checks import templates
from django.core.management import templates

"""
Django settings for supaword project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from .secure_env import SERVER_DEBUG, DJANGO_KEY, POSTGRES_PASSWORD, POSTGRES_ADDRESS, POSTGRES_USER, POSTGRES_DB


# Server version
VERSION = "0.1.1"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_KEY
DEBUG = True
ALLOWED_HOSTS = [
    "*",
    "supaword-service-production.up.railway.app",
    "*.supaword-service-production.up.railway.app",
    "*.railway.app"
]


# Application definition
INSTALLED_APPS = [
    # Django administrative interface
    'django.contrib.admin',
    'django.contrib.auth',

    # Creating and managing relationships between objects
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    # Message-passing framework to store messages for the user during redirection
    'django.contrib.messages',

    # Serving static files, such as images, CSS, and JavaScript files
    'django.contrib.staticfiles',

    # Additional packages to access abstract models
    'django_extensions',

    # DRF package
    'rest_framework',

    # CORS headers
    'corsheaders',

    # Used with DRF to filter queryset
    'django_filters',

    # Core app
    'core'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]


CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    "https://supaword-service-production.up.railway.app",
    "https://supaword-service-development.up.railway.app"
]
CORS_ALLOW_METHODS = ['POST', 'GET']

ROOT_URLCONF = 'supaword.urls'


# noinspection PyUnresolvedReferences
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'supaword.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    # postgres://postgres:[password]@138.68.124.47:5432/postgres
    # DBMS: PostgreSQL (ver. 14.7 (Ubuntu 14.7-0ubuntu0.22.10.1))
    # Case sensitivity: plain=lower, delimited=exact
    # Driver: PostgreSQL JDBC Driver (ver. 42.5.0, JDBC4.2)
    # Ping: 509 ms
    # SSL: yes
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'ZvJd63GBhaqB22WrwNa',
        'HOST': '138.68.124.47',
        'PORT': '5432',
    },
    'dev': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_ADDRESS,
        'PORT': '5432',
    },
    'wapasqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'wapamock': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db-mock.sqlite3',
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = []

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# The BASE_DIR/static directory is where you would put your application-specific static files.
# These are files that are specific to your application, such as images, CSS, and JavaScript files
# that are used by your HTML templates.

# On the other hand, the BASE_DIR/staticfiles directory is where you would put
# your project-wide static files.
# These are static files that are shared across the entire project, such as the favicon.ico file,
# robots.txt file, and other files that are not specific to any one application.

# STATIC_URL is the URL prefix that Django will use to serve static files. For example,
# if you set STATIC_URL to 'static/', and you have a file called 'app.css' in your STATIC_ROOT directory,
# then you can access that file at the URL 'http://localhost:8000/static/app.css'.
# The URL prefix can be any string you like, but it should end with a forward slash /.

# STATIC_ROOT is the absolute filesystem path to the directory where Django will collect
# all your static files into a single location for deployment.
# This directory will be created automatically when you run the collectstatic command.

# STATICFILES_DIRS is a list of directories where Django will look
# for additional static files in addition to the STATIC_ROOT directory.
# This setting is useful when you have static files that are not tied to a specific app.
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'build')

# Settings for projects to access DRF features
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_json_api.filters.QueryParameterValidationFilter',
        'rest_framework_json_api.filters.OrderingFilter',
        'rest_framework_json_api.django_filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'SEARCH_PARAM': 'filter[search]',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'
}
