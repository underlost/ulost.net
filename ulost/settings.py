# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT_DIR = os.path.dirname(__file__)
APPS_ROOT = os.path.join(CURRENT_DIR, 'apps')

if '/apps' not in ' '.join(sys.path):
    sys.path.append(APPS_ROOT)

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
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

    'djcelery',
    'rest_framework',

    #Internal
    'coreExtend',
    'pithy',
)

MIDDLEWARE_CLASSES = (
    'coreExtend.middleware.SubdomainURLRoutingMiddleware',
	'coreExtend.middleware.MultipleProxyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ulost.urls'
SUBDOMAIN_URLCONFS = {
	None: 'ulost.urls',
    'api': 'pithy.api.urls'
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(CURRENT_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'coreExtend.context_processors.template_settings',
                'coreExtend.context_processors.template_times',
            ],
        },
    },
]

#DB info injected by Heroku
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

#Cache
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    import urlparse
    redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
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

# Settings
WSGI_APPLICATION = 'ulost.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'US/Pacific'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_DOMAIN = '.herokuapp.com'

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (os.path.join(CURRENT_DIR, 'static'), )
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATIC_URL = '/static/'
MEDIA_URL = '/static/media/'

#coreExtend settings
AUTH_USER_MODEL = 'coreExtend.Account'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
ALLOW_NEW_REGISTRATIONS = False

#Site Settings
SITE_NAME = os.environ.get('SITE_NAME', 'ulost')
SITE_DESC =  os.environ.get('SITE_DESC', 'A private URL shortening service')
SITE_URL =  os.environ.get('SITE_URL', 'https://ulost.net/')
SITE_AUTHOR = os.environ.get('SITE_AUTHOR', 'Tyler Rilling')
SITE_ID = 1

#rest_framework
REST_FRAMEWORK = {
    'PAGINATE_BY': 25,                 # Default to 25
    'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100             # Maximum limit allowed when using `?page_size=xxx`.
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
