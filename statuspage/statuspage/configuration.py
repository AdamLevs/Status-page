import os

# Django settings

ALLOWED_HOSTS = ['*']

# Database Configuration
DATABASE = {
    'NAME': os.getenv('DB_NAME', 'status_page'),
    'USER': os.getenv('DB_USER', 'status_page'),
    'PASSWORD': os.getenv('DB_PASSWORD', ''),
    'HOST': os.getenv('DB_HOST', 'localhost'),
    'PORT': os.getenv('DB_PORT', '5432'),
    'CONN_MAX_AGE': 300,
}

# Redis Configuration
REDIS = {
    'tasks': {
        'HOST': os.getenv('REDIS_HOST', '127.0.0.1'),
        'PORT': int(os.getenv('REDIS_PORT', '6379')),
        'PASSWORD': '',
        'DATABASE': 0,
        'SSL': False,
    },
    'caching': {
        'HOST': os.getenv('REDIS_HOST', '127.0.0.1'),
        'PORT': int(os.getenv('REDIS_PORT', '6379')),
        'PASSWORD': '',
        'DATABASE': 1,
        'SSL': False,
    }
}

# Define the URL for E-Mails
SITE_URL = ""

# Secret Key for Django
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default_secret')

# Optional Settings
ADMINS = []

AUTH_PASSWORD_VALIDATORS = []

BASE_PATH = ''

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = []

DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

EMAIL = {
    'SERVER': 'localhost',
    'PORT': 25,
    'USERNAME': '',
    'PASSWORD': '',
    'USE_SSL': False,
    'USE_TLS': False,
    'TIMEOUT': 10,
    'FROM_EMAIL': '',
}

INTERNAL_IPS = ('127.0.0.1', '::1')

RQ_DEFAULT_TIMEOUT = 300

CSRF_COOKIE_NAME = 'csrftoken'
SESSION_COOKIE_NAME = 'sessionid'

TIME_ZONE = 'UTC'
DATE_FORMAT = 'N j, Y'
SHORT_DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'g:i a'
SHORT_TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'N j, Y g:i a'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i'