"""
Django settings for projet project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x6yb*#a_r*)#o-j9(#d@opf!755r#oxb@mnt&18(rgt_abmd6*'

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
    'equipement',
    'procedure',
    'contrôle',
    'log',
    'comptes'
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

AUTHENTICATION_BACKENDS = (
    'auth.CustomOIDCAuthenticationBackend',  # Custom backend
    'django.contrib.auth.backends.ModelBackend',
    'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
)

ROOT_URLCONF = 'projet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'projet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [ os.path.join(BASE_DIR,'static') ]

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#MEDIA_URL = '/images'
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Exempt URIS
# For example: ['core/banks', 'swagger']
KEYCLOAK_EXEMPT_URIS = []
KEYCLOAK_CONFIG = {
    'KEYCLOAK_SERVER_URL': 'http://keycloak.adcm.orangecm',
    'KEYCLOAK_REALM': 'digital-app',
    'KEYCLOAK_CLIENT_ID': 'HardeningApp-preprod',
    'KEYCLOAK_CLIENT_SECRET_KEY':'',
}
OIDC_RP_CLIENT_ID = 'HardeningApp-preprod'
OIDC_RP_CLIENT_SECRET = ''
OIDC_RP_SIGN_ALGO = 'RS256'
OIDC_OP_AUTHORIZATION_ENDPOINT = 'http://keycloak.adcm.orangecm/auth/realms/digital-app/protocol/openid-connect/auth'
OIDC_OP_TOKEN_ENDPOINT = 'http://keycloak.adcm.orangecm/auth/realms/digital-app/protocol/openid-connect/token'
OIDC_OP_USER_ENDPOINT = 'http://keycloak.adcm.orangecm/auth/realms/digital-app/protocol/openid-connect/userinfo'
OIDC_OP_JWKS_ENDPOINT = 'http://keycloak.adcm.orangecm/auth/realms/digital-app/protocol/openid-connect/certs'
OIDC_OP_LOGOUT_ENDPOINT = 'http://keycloak.adcm.orangecm/auth/realms/digital-app/protocol/openid-connect/logout'
OIDC_CREATE_USER = False

LOGIN_REDIRECT_URL = '/bord/'
LOGOUT_REDIRECT_URL = '/'