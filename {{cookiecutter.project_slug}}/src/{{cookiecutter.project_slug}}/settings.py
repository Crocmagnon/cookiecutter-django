import os
from pathlib import Path

import environ

INTERNAL_IPS = [
    "127.0.0.1",
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BASE_DIR = PROJECT_ROOT / "src"
CONTRIB_DIR = PROJECT_ROOT / "contrib"


env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=str,
    ALLOWED_HOSTS=(list, []),
    DEBUG_TOOLBAR=(bool, True),
    STATIC_ROOT=(Path, BASE_DIR / "public" / "static"),
    LOG_LEVEL=(str, "DEBUG"),
    LOG_FORMAT=(str, "default"),
    APP_DATA=(Path, PROJECT_ROOT / "data"),
    DATABASE_URL=str,
)

env_file = os.getenv("ENV_FILE", None)

if env_file:
    environ.Env.read_env(env_file)


SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")
DEBUG_TOOLBAR = env("DEBUG") and env("DEBUG_TOOLBAR")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

EXTERNAL_APPS = [
    "django_linear_migrations",
    "django_extensions",
    "django_htmx",
    "django_cleanup.apps.CleanupConfig",  # should be last: https://pypi.org/project/django-cleanup/
]
if DEBUG_TOOLBAR:
    EXTERNAL_APPS.append("debug_toolbar")

CUSTOM_APPS = [
    "whitenoise.runserver_nostatic",  # should be first
    "common",
]

INSTALLED_APPS = CUSTOM_APPS + DJANGO_APPS + EXTERNAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]
if DEBUG_TOOLBAR:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = "{{cookiecutter.project_slug}}.urls"

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

WSGI_APPLICATION = "{{cookiecutter.project_slug}}.wsgi.application"


DATABASES = {"default": env.db()}

############################################################
# Cache configuration

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
    }
}

SOLO_CACHE = "default"
SOLO_CACHE_TIMEOUT = 60 * 10  # 10 mins

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

APP_DATA = env("APP_DATA")

STATIC_URL = "/static/"
STATIC_ROOT = env("STATIC_ROOT")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Medias
MEDIA_URL = "/media/"
MEDIA_ROOT = APP_DATA / "media"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s - %(levelname)s - %(processName)s/%(module)s.%(funcName)s:%(lineno)d] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "INFO",  # set to DEBUG for SQL log
            "propagate": False,
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

for app in CUSTOM_APPS:
    LOGGING["loggers"][app] = {
        "handlers": ["console"],
        "level": env("LOG_LEVEL"),
        "propagate": False,
    }


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "{{ cookiecutter.project_slug }}.middleware.debug_toolbar_bypass_internal_ips",
    "RESULTS_CACHE_SIZE": 100,
}

# Authentication configuration.
AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/admin/login"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "common.User"
