"""
Django settings for AudioBook project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

import environ
import firebase_admin
from firebase_admin import credentials
from google.oauth2 import service_account
from icecream import ic

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start.sh development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# Initialize environment variables
env = environ.Env()
# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# False if not in os.environ because of casting above
DEBUG = env.bool('DEBUG')
# print(DEBUG == True)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
# print(ALLOWED_HOSTS is not [])

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [
    'django_extensions',
    "debug_toolbar",
    'drf_material',
    'rest_framework',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'djoser',
    "corsheaders",
    'django_celery_results',
    'django_celery_beat',
    'taggit',
]

LOCAL_APPS = [
    'apps.user.apps.UserConfig',
    'apps.book.apps.BookConfig',
    'apps.category.apps.CategoryConfig',
    'apps.notification.apps.NotificationConfig',
    'apps.subscription.apps.SubscriptionConfig',
    'apps.chapter.apps.ChapterConfig',
    'apps.author.apps.AuthorConfig',
    'apps.bookmark.apps.BookmarkConfig',
    'apps.book_page.apps.BookPageConfig',
]

INSTALLED_APPS += LOCAL_APPS
INSTALLED_APPS += THIRD_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # new
]

ROOT_URLCONF = 'AudioBook.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': []
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            "builtins": ["apps.user.templatetags.length_is"],  # <- HERE
        },
    },
]

WSGI_APPLICATION = 'AudioBook.wsgi.application'
ASGI_APPLICATION = "AudioBook.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# LANGUAGE_CODE = 'uz-uz'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
# MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR / 'staticfiles/'
MEDIA_ROOT = BASE_DIR / 'media/'

AUTH_USER_MODEL = 'user.User'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': env.db(),
    'extra': env.db_url(
        'DATABASE_URL',
        default=env('DATABASE_URL'),
        engine=env('SQL_ENGINE')
    )
}

# Celery settings
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis as the message broker
CELERY_RESULT_BACKEND = 'django-db'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'


CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
]

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'apps.user.serializers.CustomUserCreateSerializer',
        'user': 'apps.user.serializers.CustomUserSerializer',
        'current_user': 'apps.user.serializers.CustomUserSerializer',
    },
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'auth/confirm-email/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'auth/password-reset-confirm/{uid}/{token}'
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

INTERNAL_IPS = env.list('ALLOWED_HOSTS')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'auth_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'plan.log',
        },
    },
    'loggers': {
        'django.security.Authentication': {
            'handlers': ['auth_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',  # Needed for file uploads
    ),
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'AudioBook',
    'DESCRIPTION': 'Mobile app API',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

# Path to your Firebase service account key JSON file
FIREBASE_ADMIN_CREDENTIALS = os.path.join(BASE_DIR, 'credentials', 'serviceAccountKey.json')

# Initialize the Firebase app
firebase_cred = credentials.Certificate(FIREBASE_ADMIN_CREDENTIALS)
firebase_admin.initialize_app(firebase_cred, {
    'storageBucket': 'audiobook-50fe7.appspot.com'  # Use only the bucket name
})

# Firebase Storage settings
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'audiobook-50fe7.appspot.com'
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(FIREBASE_ADMIN_CREDENTIALS)

# Optional: Define media URL for Firebase-hosted files
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"

# looking up existing tags
TAGGIT_CASE_INSENSITIVE = True

if __name__ == '__main__':
    ic(BASE_DIR)
