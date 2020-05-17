import os
from dotenv import load_dotenv, find_dotenv
from datetime import timedelta
from pathlib import Path


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_name = os.path.basename(os.path.dirname(__file__))

# env_path = Path('.') / '.env'
# env_path = Path('.') / '.env_prod'

# load_dotenv(dotenv_path=env_path)
load_dotenv()
# load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG")

GOOGLE_APPLICATION_CREDENTIALS = os.path.join(BASE_DIR + '/shopbackend/gcloud_credentials.json')
DEFAULT_FILE_STORAGE = 'shopbackend.gcloud.GoogleCloudMediaFileStorage'
STATICFILES_STORAGE = 'shopbackend.gcloud.GoogleCloudStaticFileStorage'
GS_PROJECT_ID = os.getenv("GS_PROJECT_ID")
GS_STATIC_BUCKET_NAME = os.getenv("GS_STATIC_BUCKET_NAME")
GS_MEDIA_BUCKET_NAME = os.getenv("GS_MEDIA_BUCKET_NAME")


ALLOWED_HOSTS = ['*']

ADMINS = os.getenv("ADMINS")
MANAGERS = os.getenv("MANAGERS")
# ALLOWED_HOSTS = [str(os.getenv("HOST")).split(':')[0]]

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = os.getenv("CORS_ORIGIN_WHITELIST")

INSTALLED_APPS = [
    'django.contrib.admindocs',
    'django.contrib.admin',
    # 'shopbackend.apps.MyAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'main.apps.MainConfig',
    'rest_framework',
    
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

ROOT_URLCONF = app_name + '.urls'

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

"""
LOGGING = {
     'version': 1,
     'disable_existing_loggers': False,
     'formatters': {
         'verbose': {
             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
             'style': '{',
         },
         'simple': {
             'format': '{levelname} {message}',
             'style': '{',
         },
     },
     'filters': {
         'require_debug_false': {
             '()': 'django.utils.log.CallbackFilter',
             'callback': _require_debug_false
         }
     },
     'handlers': {
         'console': {
             'level': 'INFO',
             # 'filters': ['require_debug_true'],
             'class': 'logging.StreamHandler',
             'formatter': 'simple'
         },
         'mail_admins': {
             'level': 'ERROR',
             'class': 'django.utils.log.AdminEmailHandler',
             'filters': {
                 'require_debug_false': {
                     '()': 'django.utils.log.CallbackFilter',
                     'callback': _require_debug_false
                 }
             }
         }
     },
     'loggers': {
         'django': {
             'handlers': ['console'],
             'propagate': True,
         },
         'django.request': {
             'handlers': ['mail_admins'],
             'level': 'ERROR',
             'propagate': False,
         },
         'myproject.custom': {
             'handlers': ['console', 'mail_admins'],
             'level': 'INFO',
             'filters': {
                 'require_debug_false': {
                     '()': 'django.utils.log.CallbackFilter',
                     'callback': _require_debug_false
                }
            }
        }
    }
}
"""
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

FIXTURE_DIRS = (os.path.join(BASE_DIR, 'fixtures'),)

WSGI_APPLICATION = app_name + '.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE"),
        'NAME': os.getenv("DB_NAME"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
    }
    # 'default':{
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
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

CACHES = {
    'default': {
        'BACKEND': os.getenv("CACHE_BACKEND"),
        'LOCATION': os.getenv("CACHE_LOCATION"),
    }
}

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
# EMAIL_FILE_PATH = os.getenv("EMAIL_FILE_PATH")
EMAIL_FILE_PATH = 'https://storage.googleapis.com/{}/emails/'.format(GS_MEDIA_BUCKET_NAME)
EMAIL_USE_TLS = True

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

# STATIC_URL = os.getenv("STATIC_URL")
# STATIC_ROOT = os.getenv("STATIC_ROOT")
#
# MEDIA_URL = os.getenv("MEDIA_URL")
# MEDIA_ROOT = os.getenv("MEDIA_ROOT")


STATIC_URL = 'https://storage.googleapis.com/{}/'.format(GS_STATIC_BUCKET_NAME)
STATIC_ROOT = "static/"

MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(GS_MEDIA_BUCKET_NAME)
MEDIA_ROOT = "media/"

UPLOAD_ROOT = 'media/uploads/'

DOWNLOAD_ROOT = os.path.join(BASE_DIR, "static/media/downloads")
DOWNLOAD_URL = STATIC_URL + "media/downloads"

