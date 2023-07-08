from core.settings.base import *
from datetime import timedelta
from urllib.parse import quote_plus as urlquote

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'PORT': os.environ.get('DB_PORT'),
        'HOST': os.environ.get('DB_HOST')
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=int(os.environ.get('ACCESS_TOKEN_LIFETIME'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(seconds=int(os.environ.get('REFRESH_TOKEN_LIFETIME'))),
}

FRONT_END_DOMAIN = os.environ.get('FRONT_END_DOMAIN')
BACK_END_DOMAIN = os.environ.get('BACK_END_DOMAIN')

# Forgot password link expiry time
PASSWORD_RESET_TIMEOUT = int(os.environ.get("PASSWORD_RESET_TIMEOUT"))

MEDIA_ROOT = BASE_DIR / 'media_files'
MEDIA_URL = '/media/'

ELASTIC_SEARCH_URL = 'http://{user_name}:{password}@{host_ip}:{host_port}'.format(
    user_name=os.environ.get('ELASTICSEARCH_USERNAME'),
    password=urlquote(os.environ.get('ELASTICSEARCH_PASSWORD')),
    host_ip=os.environ.get('ELASTICSEARCH_HOST_IP'),
    host_port=int(os.environ.get('ELASTICSEARCH_HOST_PORT'))
)

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': [ELASTIC_SEARCH_URL],
    },
}

FRAMEWORK_INDEX_NAME = os.environ.get('FRAMEWORK_INDEX_NAME')
INQUIRY_EMAIL = os.environ.get('INQUIRY_EMAIL')
