"""
Django settings for djangoconfig project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fsg^d=%qt56_)m)b#1#fgug1da#+s7$=()fig0&j6zhf-6tui1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'ferremas',
    'administracion',
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

ROOT_URLCONF = 'djangoconfig.urls'

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
                'ferremas.context_processor.total_carrito',
                'ferremas.context_processor.categorias_processor',
                'ferremas.context_processor.marcas_processor',
                'ferremas.context_processor.get_dollar',
                'ferremas.context_processor.regiones'
            ],
        },
    },
]

LOGIN_REDIRECT_URL = "/tienda/"
LOGOUT_REDIRECT_URL = "/tienda/"
API_BASE_URL = "127.0.0.1:8000/api/productos"
API_BASE_TRANSBANK_URL = "127.0.0.1:8000/api/compras"
TRANSBANK_RETURN_URL = "127.0.0.1:7000/tienda/transbank"

# credenciales API integracion
USERNAME = 'nico2'
PASSWORD = 'nico1234'
EMAIL = 'nico@correo.com'
API_TOKEN = 'Token 7688f81c094d735e469a4fc4cba97917bf07c89b'

WSGI_APPLICATION = 'djangoconfig.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbintegracion',
        'USER': 'user',
        'PASSWORD': 'zorUOpbvfwpfBRNFSTo1Os7AYZzxK8RL',
        'HOST': 'dpg-cov4i7021fec73fdt5fg-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'ferremas.password_validation.PassValidator',
    }
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'ferremas/static'),
]

STATIC_URL = '/static/'

MEDIA_URL = 'http://127.0.0.1:8000/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
