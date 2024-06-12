from pathlib import Path

from app import env


SECRET_KEY = env.SECRET_KEY
DEFAULT_HMAC_KEY = env.OSF_HMAC_KEY or "lmaoooooo"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.DEBUG

USER_REFERENCE_COOKIE = "osf"
OSF_BASE_URL = env.OSF_BASE_URL.rstrip("/")
OSF_API_BASE_URL = env.OSF_API_BASE_URL.rstrip("/")
OSF_BROKER_URL = "amqp://guest:guest@192.168.168.167:5672//"
ALLOWED_RESOURCE_URI_PREFIXES = {OSF_BASE_URL}
if DEBUG:
    # allow for local osf shenanigans
    ALLOWED_RESOURCE_URI_PREFIXES.update(
        [
            "http://192.168.168.167:5000",
            "http://localhost:5000",
        ]
    )

ALLOWED_HOSTS = env.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "rest_framework",
    "rest_framework_json_api",
    "addon_service",
]

if DEBUG:
    # run under ASGI locally:
    INSTALLED_APPS.insert(0, "daphne")  # django's reference asgi server
    ASGI_APPLICATION = "app.asgi.application"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Database settings for PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.POSTGRES_DB,
        "USER": env.POSTGRES_USER,
        "PASSWORD": env.POSTGRES_PASSWORD,
        "HOST": env.POSTGRES_HOST,
        "PORT": env.POSTGRES_PORT,
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": env.OSFDB_CONN_MAX_AGE,
        "OPTIONS": {
            "sslmode": env.OSFDB_SSLMODE,
        },
    },
}

if env.OSFDB_HOST:
    DATABASES["osf"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.OSFDB_NAME,
        "USER": env.OSFDB_USER,
        "PASSWORD": env.OSFDB_PASSWORD,
        "HOST": env.OSFDB_HOST,
        "PORT": env.OSFDB_PORT,
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": env.OSFDB_CONN_MAX_AGE,
        "OPTIONS": {
            "sslmode": env.OSFDB_SSLMODE,
        },
    }

DATABASE_ROUTERS = ["addon_service.osf_models.db_router.OsfDatabaseRouter"]

REST_FRAMEWORK = {
    "PAGE_SIZE": 101,
    "EXCEPTION_HANDLER": "addon_service.exception_handler.api_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework_json_api.pagination.JsonApiPageNumberPagination",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework_json_api.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework_json_api.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework_json_api.filters.QueryParameterValidationFilter",
        "rest_framework_json_api.filters.OrderingFilter",
        "rest_framework_json_api.django_filters.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": ("app.authentication.GVCombinedAuthentication",),
    "SEARCH_PARAM": "filter[search]",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []  # type: ignore


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

# Queue names and routing keys for Rabbit/Celery Messaging
EXCHANGE_NAME = (
    "account_status_changes"  # Assuming this is the exchange name used for publishing
)

OSF_SENSITIVE_DATA_SECRET = env.OSF_SENSITIVE_DATA_SECRET
OSF_SENSITIVE_DATA_SALT = env.OSF_SENSITIVE_DATA_SALT
