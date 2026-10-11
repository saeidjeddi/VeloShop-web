import os
from .rest_framework_conf import *
from .cache_conf import *
from .celery_conf import *

from .db_conf import DATABASES
from .meddleware_conf import MIDDLEWARE
from .apps_conf import INSTALLED_APPS
from .email_conf import MAILERS



from .paths import BASE_DIR

from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', )

DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

# DATABASE_ROUTERS = [
#     "config.settings.router.DatabaseRouter",
# ]

WSGI_APPLICATION = 'config.wsgi.application'


ROOT_URLCONF = 'config.urls.urls'

AUTH_USER_MODEL = "accounts.UserModel"

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

STATIC_URL = "/assets/static/"
STATIC_ROOT = BASE_DIR.parent / "volumes" / "assets" / "static/"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'volumes' / 'media'


# ARVAN CLOUD STORAGE

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")


# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         "OPTIONS": {
#             "access_key": AWS_ACCESS_KEY_ID,
#             "secret_key": AWS_SECRET_ACCESS_KEY,
#             "bucket_name": AWS_STORAGE_BUCKET_NAME,
#             "endpoint_url": AWS_S3_ENDPOINT_URL,
#             "region_name": AWS_S3_REGION_NAME,

#             "location": "assets/media",
#             "querystring_auth": False,
#             "file_overwrite": False,
#             "default_acl": "public-read",
#         },
#     },

#     "staticfiles": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         "OPTIONS": {
#             "access_key": AWS_ACCESS_KEY_ID,
#             "secret_key": AWS_SECRET_ACCESS_KEY,
#             "bucket_name": AWS_STORAGE_BUCKET_NAME,
#             "endpoint_url": AWS_S3_ENDPOINT_URL,
#             "region_name": AWS_S3_REGION_NAME,

#             "location": "assets/static",
#             "querystring_auth": False,
#             "file_overwrite": False,
#             "default_acl": "public-read",
#         },
#     },
# }

ZARINPAL_MERCHANT_ID = os.getenv("ZARINPAL_MERCHANT_ID")
ZARINPAL_SANDBOX = os.getenv("ZARINPAL_SANDBOX", "True").lower() == "true"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_AGE = 86400  # 24 hours in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True

# Maximum request body size (500 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 500 * 1024 * 1024

# Maximum size of uploaded file kept in memory (500 MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 500 * 1024 * 1024


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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


