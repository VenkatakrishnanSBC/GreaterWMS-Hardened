from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY: SECRET_KEY from environment variable (SEC-007 / ISS-008)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    # Fallback for local development only — NEVER use in production
    from django.core.management.utils import get_random_secret_key
    SECRET_KEY = get_random_secret_key()
    import warnings
    warnings.warn(
        "DJANGO_SECRET_KEY is not set! Using a random key. "
        "Set DJANGO_SECRET_KEY environment variable for production.",
        RuntimeWarning
    )

# SECURITY: DEBUG from environment variable (SEC-002 / ISS-003)
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

# SECURITY: ALLOWED_HOSTS from environment variable (SEC-003 / ISS-002)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'staff.apps.StaffConfig',
    'userprofile.apps.UserprofileConfig',
    'userregister.apps.UserregisterConfig',
    'userlogin.apps.UserloginConfig',
    'company.apps.CompanyConfig',
    'supplier.apps.SupplierConfig',
    'asn.apps.AsnConfig',
    'dn.apps.DnConfig',
    'binset.apps.BinsetConfig',
    'binsize.apps.BinsizeConfig',
    'binproperty.apps.BinpropertyConfig',
    'customer.apps.CustomerConfig',
    'capital.apps.CapitalConfig',
    'cyclecount.apps.CyclecountConfig',
    'dashboard.apps.DashboardConfig',
    'warehouse.apps.WarehouseConfig',
    'goods.apps.GoodsConfig',
    'goodsunit.apps.GoodsunitConfig',
    'goodsclass.apps.GoodsclassConfig',
    'goodscolor.apps.GoodscolorConfig',
    'goodsbrand.apps.GoodsbrandConfig',
    'goodsshape.apps.GoodsshapeConfig',
    'goodsspecs.apps.GoodsspecsConfig',
    'goodsorigin.apps.GoodsoriginConfig',
    'payment.apps.PaymentConfig',
    'driver.apps.DriverConfig',
    'stock.apps.StockConfig',
    'throttle.apps.ThrottleConfig',
    'uploadfile.apps.UploadfileConfig',
    'scanner.apps.ScannerConfig',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'drf_spectacular',
    'drf_spectacular_sidecar'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # PERF-004: Efficient static file serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # SEC-001 / ISS-001: CSRF protection enabled
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'greaterwms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'greaterwms.wsgi.application'
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost:8080,http://127.0.0.1:8080'
).split(',')

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# update
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
        },
        # PERF-007: Persistent DB connections (connection pooling)
        # Set to 0 for unlimited persistent connections, or seconds for lifetime
        'CONN_MAX_AGE': int(os.environ.get('DB_CONN_MAX_AGE', 600)),  # 10 minutes
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_new').replace('\\', '/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static').replace('\\', '/'),
]
# PERF-004 / FRONT-004: Whitenoise compressed + manifest storage
# Serves static files with content-hash filenames for cache busting
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')

SPECTACULAR_SETTINGS = {
    'TITLE': 'GreaterWMS',
    'DESCRIPTION': 'GreaterWMS API Documents',
    'VERSION': '2.1.48',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    # OTHER SETTINGS
}

REST_FRAMEWORK = {
    # AttributeError: ‘AutoSchema’ object has no attribute ‘get_link’
    # DEFAULT SET:
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
    # EXCEPTION:
    'EXCEPTION_HANDLER': 'utils.my_exceptions.custom_exception_handler',
    # Base API policies:
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
        #'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': ['utils.auth.Authtication', ],
    'DEFAULT_PERMISSION_CLASSES': ["utils.permission.Normalpermission", ],
    'DEFAULT_THROTTLE_CLASSES': ['utils.throttle.VisitThrottle', ],
    # 'DEFAULT_THROTTLE_RATES': ['utils.throttle.VisitThrottle', ],
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'rest_framework.negotiation.DefaultContentNegotiation',
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',  # ARCH-002 / ISS-037
    # ARCH-003: Default pagination for all list endpoints
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        # 'django_filters.rest_framework.backends.DjangoFilterBackend',
    ],
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',
    'NUM_PROXIES': None,
    # Versioning:
    'DEFAULT_VERSION': None,
    'ALLOWED_VERSIONS': None,
    'VERSION_PARAM': 'version',
    # Authentication:
    'UNAUTHENTICATED_USER': 'django.contrib.auth.models.AnonymousUser',
    'UNAUTHENTICATED_TOKEN': None,
    # View configuration:
    'VIEW_NAME_FUNCTION': 'rest_framework.views.get_view_name',
    'VIEW_DESCRIPTION_FUNCTION': 'rest_framework.views.get_view_description',
    'NON_FIELD_ERRORS_KEY': 'non_field_errors',
    # Testing
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer'
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'multipart',
    # Hyperlink settings
    'URL_FORMAT_OVERRIDE': 'format',
    'FORMAT_SUFFIX_KWARG': 'format',
    'URL_FIELD_NAME': 'url',
    # Encoding
    'UNICODE_JSON': True,
    'COMPACT_JSON': True,
    'STRICT_JSON': True,
    'COERCE_DECIMAL_TO_STRING': True,
    'UPLOADED_FILES_USE_URL': True,
    # Browseable API
    'HTML_SELECT_CUTOFF': 1000,
    'HTML_SELECT_CUTOFF_TEXT': "More than {count} items...",
    # Schemas
    'SCHEMA_COERCE_PATH_PK': True,
    'SCHEMA_COERCE_METHOD_NAMES': {
        'retrieve': 'read',
        'destroy': 'delete'
    },
}

SERVER_LOGS_FILE = os.path.join(BASE_DIR, "logs", "server.log")
ERROR_LOGS_FILE = os.path.join(BASE_DIR, "logs", "error.log")
if not os.path.exists(os.path.join(BASE_DIR, "logs")):
    os.makedirs(os.path.join(BASE_DIR, "logs"))

STANDARD_LOG_FORMAT = (
    "[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s"
)
CONSOLE_LOG_FORMAT = (
    "[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s"
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": STANDARD_LOG_FORMAT},
        "console": {
            "format": CONSOLE_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "file": {
            "format": CONSOLE_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": SERVER_LOGS_FILE,
            "maxBytes": 1024 * 1024 * 100,
            "backupCount": 5,
            "formatter": "standard",
            "encoding": "utf-8",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": ERROR_LOGS_FILE,
            "maxBytes": 1024 * 1024 * 100,
            "backupCount": 3,
            "formatter": "standard",
            "encoding": "utf-8",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "error", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "scripts": {
            "handlers": ["console", "error", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": [],
            "propagate": True,
            "level": "INFO",
        },
    },
}

# SECURITY: CORS restricted to trusted origins (SEC-004 / ISS-004)
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = os.environ.get('CORS_ALLOW_ALL', 'False').lower() in ('true', '1')
CORS_ORIGIN_WHITELIST = os.environ.get(
    'CORS_ORIGIN_WHITELIST',
    'http://localhost:8080,http://127.0.0.1:8080'
).split(',')

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'token',
    'language',
    'operator',
    'device',
    'app-id',
    'event-sign'
)

LAZY_RENDERING = True
NATIVE_SCROLLBARS = True

ALLOCATION_SECONDS = 1
GET_THROTTLE = 500
POST_THROTTLE = 500
PUT_THROTTLE = 500
PATCH_THROTTLE = 500
DELETE_THROTTLE = 500

# SECURITY: JWT expiration reduced from 20 years to 24 hours
JWT_TIME = 60 * 60 * 24  # 24 hours

# SECURITY: HTTPS enforcement settings (SEC-011)
# Only enforce in production (when DEBUG is False)
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURITY: Request size limits (SEC-012)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# CODE-008 / ISS-040: Application-level logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'greaterwms.log'),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'stock': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'asn': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'dn': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'utils': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# PERF-002 / PERF-003: Redis cache configuration
# Set REDIS_URL env var to enable Redis caching (e.g., redis://localhost:6379/0)
# Falls back to local memory cache if Redis is not configured
REDIS_URL = os.environ.get('REDIS_URL', '')
if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'db': 0,
            },
            'KEY_PREFIX': 'gwms',
            'TIMEOUT': 300,  # 5 minutes default TTL
        },
        'throttle': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'db': 1,
            },
            'KEY_PREFIX': 'throttle',
            'TIMEOUT': 60,  # 1 minute for throttle records
        },
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'gwms-cache',
            'TIMEOUT': 300,
        },
        'throttle': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'gwms-throttle',
            'TIMEOUT': 60,
        },
    }

# Cache timeout settings for frequently queried data
CACHE_TTL_SHORT = 60       # 1 minute (for rapidly changing data like stock)
CACHE_TTL_MEDIUM = 300     # 5 minutes (for goods, suppliers, customers)
CACHE_TTL_LONG = 3600      # 1 hour (for bin configs, settings)

# UPGRADE-004: Celery async task processing configuration
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/2')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/3')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes hard limit
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes soft limit
CELERY_WORKER_CONCURRENCY = int(os.environ.get('CELERY_CONCURRENCY', 4))

# UPGRADE-005: OAuth2 / SSO configuration
# Install: pip install django-allauth
# Set OAUTH_ENABLED=true and configure provider credentials
OAUTH_ENABLED = os.environ.get('OAUTH_ENABLED', 'false').lower() == 'true'
if OAUTH_ENABLED:
    INSTALLED_APPS += [
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.github',
        'allauth.socialaccount.providers.microsoft',
    ]
    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    ]
    SITE_ID = 1
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    SOCIALACCOUNT_AUTO_SIGNUP = True
    LOGIN_REDIRECT_URL = '/'

    # Provider credentials from env vars
    SOCIALACCOUNT_PROVIDERS = {
        'google': {
            'APP': {
                'client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID', ''),
                'secret': os.environ.get('GOOGLE_OAUTH_SECRET', ''),
            },
            'SCOPE': ['profile', 'email'],
        },
        'github': {
            'APP': {
                'client_id': os.environ.get('GITHUB_OAUTH_CLIENT_ID', ''),
                'secret': os.environ.get('GITHUB_OAUTH_SECRET', ''),
            },
        },
    }

# FEATURE-002: Email notification settings
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'true').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@greaterwms.com')

