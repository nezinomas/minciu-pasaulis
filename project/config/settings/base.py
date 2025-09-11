import os
import tomllib as toml
from pathlib import Path

# ================   PATH CONFIGURATION
BASE_DIR = Path(__file__).absolute()
PROJECT_ROOT = BASE_DIR.parent.parent.parent.parent
SITE_ROOT = BASE_DIR.parent.parent.parent

# Take environment variables from .conf file
with open(PROJECT_ROOT / ".conf", "rb") as f:
    toml = toml.load(f)

    ENV = toml["django"]
    DB = toml["database"]



# ================   MEDIA CONFIGURATION
MEDIA_ROOT = Path(PROJECT_ROOT) / 'media'
MEDIA_URL = "/media/"


# ================   STATIC FILE CONFIGURATION
STATIC_URL = '/static/'
STATIC_ROOT = Path(SITE_ROOT) / 'static'


# ================   DEBUG CONFIGURATION
DEBUG = False
TEMPLATE_DEBUG = DEBUG


# ================   SECRET CONFIGURATION
SECRET_KEY = ENV["SECRET_KEY"]


# ================   project CONFIGURATION
ALLOWED_HOSTS = []


# ================   DATABASE CONFIGURATION
DATABASES = {"default": DB}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# ================   GENERAL CONFIGURATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ================   TEMPLATE CONFIGURATION
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SITE_ROOT, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'project.thoughts.context.show_categories',
            ],
        },
    },
]


# ================   MIDDLEWARE CONFIGURATION
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]


# ================   APP CONFIGURATION
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'slippers',
    'project.thoughts',
    'project.core'
]


# ================   URL CONFIGURATION
ROOT_URLCONF = 'project.config.urls'


# ================   WSGI CONFIGURATION
WSGI_APPLICATION = 'project.config.wsgi.application'


# ================   PASSWORD VALIDATORS CONFIGURATION
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

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
