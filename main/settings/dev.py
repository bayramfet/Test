from .base import *

ALLOWED_HOSTS = ["*"]

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []
 
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG") 

THIRD_PARTY_APPS = ["debug_toolbar"] 
INSTALLED_APPS += THIRD_PARTY_APPS 
 
THIRD_PARTY_MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] 
MIDDLEWARE += THIRD_PARTY_MIDDLEWARE 
 
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases 
DATABASES = { 
    "default": { 
        "ENGINE": "django.db.backends.sqlite3", 
        "NAME": BASE_DIR / "db.sqlite3", 
    } 
} 
 
INTERNAL_IPS = [ 
    "127.0.0.1", 
]

