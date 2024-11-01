import os

# Helper function to read values from terraform-outputs.txt
def read_terraform_output(key):
    try:
        with open("./infrastructure/terraform-outputs.txt") as f:
            for line in f:
                if line.startswith(f"{key}:"):
                    return line.split(": ", 1)[1].strip()
    except FileNotFoundError:
        print("Terraform outputs file not found. Using default settings.")
    return ""

# Required Settings
ALLOWED_HOSTS = ['*']

# Database Configuration
DATABASE = {
    'NAME': 'status_page',
    'USER': read_terraform_output("RDS Username") or os.getenv('DB_USER', 'status_page'),
    'PASSWORD': os.getenv('DB_PASSWORD', 'Qz147369'),  # Secure this with AWS Secrets Manager or environment variable
    'HOST': read_terraform_output("RDS Endpoint").split(':')[0] if read_terraform_output("RDS Endpoint") else os.getenv('DB_HOST', 'localhost'),
    'PORT': read_terraform_output("RDS Endpoint").split(':')[1] if ':' in read_terraform_output("RDS Endpoint") else os.getenv('DB_PORT', '5432'),
    'CONN_MAX_AGE': 300,
}

# Redis Configuration
REDIS = {
    'tasks': {
        'HOST': read_terraform_output("Redis Endpoint") or os.getenv('REDIS_HOST', 'redis'),  # Changed to 'redis'
        'PORT': int(os.getenv('REDIS_PORT', '6379')),
        'PASSWORD': '',
        'DATABASE': 0,
        'SSL': False,
    },
    'caching': {
        'HOST': read_terraform_output("Redis Endpoint") or os.getenv('REDIS_HOST', 'redis'),  # Changed to 'redis'
        'PORT': int(os.getenv('REDIS_PORT', '6379')),
        'PASSWORD': '',
        'DATABASE': 1,
        'SSL': False,
    }
}

# Define the URL which will be used e.g. in E-Mails
SITE_URL = ""

# Secret Key for Django
SECRET_KEY = 'JTrYVpooBfFc(nxNvLs+cR6Qg2JV-0Xd-uf(G%+eOnmg@%kDy9'  # Ensure to secure this properly!

# Optional Settings
ADMINS = [
    # ('John Doe', 'jdoe@example.com'),
]

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    #     'OPTIONS': {
    #         'min_length': 10,
    #     }
    # },
]

BASE_PATH = ''

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    # 'https://hostname.example.com',
]
CORS_ORIGIN_REGEX_WHITELIST = [
    # r'^(https?://)?(\w+\.)?example\.com$',
]

DEBUG = True

EMAIL = {
    'SERVER': 'localhost',
    'PORT': 25,
    'USERNAME': '',
    'PASSWORD': '',
    'USE_SSL': False,
    'USE_TLS': False,
    'TIMEOUT': 10,  # seconds
    'FROM_EMAIL': '',
}

INTERNAL_IPS = ('127.0.0.1', '::1')

LOGGING = {}

LOGIN_TIMEOUT = None

# MEDIA_ROOT can be set if necessary
# MEDIA_ROOT = '/opt/status-page/statuspage/media'

FIELD_CHOICES = {}

PLUGINS = [
    # 'sp_uptimerobot',
    # 'sp_external_status_providers',
]

PLUGINS_CONFIG = {
    'sp_uptimerobot': {
        'uptime_robot_api_key': '',
    },
}

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
