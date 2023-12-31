"""
Django settings for Flash project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!rb8y($i-(u(bz*&9te33711-bu!e0&oha@%bg^il&*u*4lg5w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition
SITE_ID = 6


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "bootstrap5",
    'fontawesomefree',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #provider
    'allauth.socialaccount.providers.google',
    'FlashDS.apps.FlashdsConfig',
]

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'PROFILE_FIELDS': [
            'first-name',
            'last-name',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'FlashDS.middleware.ProfileMiddleware',

]

ROOT_URLCONF = 'Flash.urls'

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

WSGI_APPLICATION = 'Flash.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


#project Root
STATIC_URL = 'static/'
LOGIN_URL = '/sign-in/'
LOGIN_REDIRECT_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR,'FlashMedia')
MEDIA_URL = '/FlashMedia/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_LOGIN_ON_GET = True
#The SMTP backend is the default configuration inherited by Django. If you want to 
#specify it explicitly, put the following in your settings:

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'flashdeliverysystem@gmail.com'
EMAIL_HOST_PASSWORD = 'qyvg hlkj wasr ggvy'
DEFAULT_FROM_EMAIL = 'Flash Delivery System <no-reply@FlashDS.localhost>'

# Firebase admin 
FIREBASE_ADMIN_CREDENTIAL = os.path.join(BASE_DIR, "flash-delivery-system-405414-firebase-adminsdk-4pgto-3685014665.json")


# Payment API KEYS
STRIPE_API_PUBLISH_KEY = "pk_test_51OEZf7GcRaeFknGRueza2YUMwwgIGCXHvbnYX8taT9kdPdUNKfACmdnYJpfNfR6iNAjS2rk6a23yGTHtLuClMoS100mq8MeJdW"
STRIPE_API_SECRET_KEY = "sk_test_51OEZf7GcRaeFknGR1aWzWBoZmR6pG6dZrdqzZiEEcnUNLb66GF4rDm29fSVC3IH9eHXN3iWwnUiRcQreUNoeudHv00m36BiWih"


#Google API KEY
GOOGLE_MAP_API_KEY = "AIzaSyAnRVXjdIs0R0g4A415tVU4WEq8O9BATD4"

#Notifications
NOTIFICATION_URL= ' https://194c-197-134-251-92.ngrok-free.app'
#trust csrf for test
CSRF_TRUSTED_ORIGINS = [' https://194c-197-134-251-92.ngrok-free.app ']


