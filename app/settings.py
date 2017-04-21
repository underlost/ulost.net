# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_DIR   = os.path.dirname(__file__)
UTIL_ROOT    = os.path.join(CURRENT_DIR, 'util')
APPS_ROOT    = os.path.join(CURRENT_DIR, 'apps')
VENDOR_ROOT   = os.path.join(CURRENT_DIR, 'vendor')

if '/util' not in ' '.join(sys.path):
    sys.path.append(UTIL_ROOT)

if '/vendor' not in ' '.join(sys.path):
    sys.path.append(VENDOR_ROOT)

if '/apps' not in ' '.join(sys.path):
    sys.path.append(APPS_ROOT)

DEBUG = os.environ.get('ENABLE_DEBUG', True)
DEV_ENV = os.environ.get('DEV_ENV', True)
ENABLE_CACHE = os.environ.get('ENABLE_CACHE', False)
ENABLE_S3 = os.environ.get('ENABLE_S3', False)
ENABLE_SSL = os.environ.get('ENABLE_SSL', False)
HEROKU_ENV = os.environ.get('HEROKU_ENV', True)

if DEV_ENV:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

if ENABLE_SSL:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = [
    'localhost', '127.0.0.1',
	'ulost.net', 'www.ulost.net',
	'ulost.herokuapp.com',
]

ADMINS = (('Tyler Rilling', 'tyler@underlost.net'))
MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    #External
    'rest_framework',

    #Internal
    'coreExtend',
    'redirection',
)

MIDDLEWARE_CLASSES = (
    #'coreExtend.middleware.SubdomainURLRoutingMiddleware',
	'coreExtend.middleware.MultipleProxyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = os.environ.get('SECRET_KEY', '4eJUc9x86aXSLG07QgM1qZskVYZTBsWRkRMQc04rPLLgjos1wp')

ROOT_URLCONF = 'app.urls'
SUBDOMAIN_URLCONFS = {
	None: 'app.urls',
    'api': 'redirection.api.urls'
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(CURRENT_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

            	'coreExtend.context_processors.template_settings',
                'coreExtend.context_processors.template_times',
            ],
            'debug': DEBUG,
        },
    },
]

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', ''),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', ''),
    }
}

#DB info injected by Heroku
if HEROKU_ENV:
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

#Cache
if ENABLE_CACHE:
    from urllib.parse import urlparse
    redis_url = urlparse(os.environ.get('REDISCLOUD_URL'))
    CACHES = {
            'default': {
                'BACKEND': 'redis_cache.RedisCache',
                'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
                'OPTIONS': {
                    'PASSWORD': redis_url.password,
                    'DB': 0,
            }
        },
        "staticfiles": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "TIMEOUT": 60 * 60 * 24 * 365,
            "LOCATION": "static",
        },
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# Settings
WSGI_APPLICATION = 'ulost.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'US/Pacific'
USE_I18N = True
USE_L10N = True
USE_TZ = True
WSGI_APPLICATION = 'app.wsgi.application'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

# Static files (CSS, JavaScript, Images)
if ENABLE_S3:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = os.environ.get('LIVE_STATIC_URL', 'https://static.example.com/')
    MEDIA_URL = os.environ.get('LIVE_MEDIA_URL', 'https://static.example.com/media/')
else:
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    STATIC_URL = '/static/'
    MEDIA_URL = '/static/media/'

#Amazon S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '123')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '123')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', 'static.example.com')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_BUCKET_DOMAIN', 'static.example.com')
AWS_S3_SECURE_URLS = False
AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
AWS_S3_HOST = 's3-us-west-2.amazonaws.com'

#coreExtend settings
AUTH_USER_MODEL = 'coreExtend.Account'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
ALLOW_NEW_REGISTRATIONS = False

#Site Settings
SITE_NAME = os.environ.get('SITE_NAME', 'ulost.net')
SITE_DESC =  os.environ.get('SITE_DESC', '')
SITE_URL =  os.environ.get('SITE_URL', 'http://ulost.net')
SITE_AUTHOR = os.environ.get('SITE_AUTHOR', 'Tyler Rilling')
SITE_ID = 1
MIXPANEL_TOKEN = os.environ.get('MIXPANEL_TOKEN')

#rest_framework
REST_FRAMEWORK = {
    'PAGINATE_BY': 25, # Default to 25
    'PAGINATE_BY_PARAM': 'page_size', # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100, # Maximum limit allowed when using `?page_size=xxx`.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

LOGGING = {
    "version": 1,
    # Don't throw away default loggers.
    "disable_existing_loggers": False,
    "handlers": {
        # Redefine console logger to run in production.
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        # Redefine django logger to use redefined console logging.
        "django": {
            "handlers": ["console"],
        }
    }
}
