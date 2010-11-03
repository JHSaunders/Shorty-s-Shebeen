# Django settings for shortys_shebeen project.
import os
import sys

import logging
logging.basicConfig(stream=sys.stdout,level=logging.ERROR)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('James Saunders', 'james.h.saunders@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'shortys.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Africa/Johannesburg'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

#The Space home, usefulfor development
SPACE_HOME = os.environ['PWD']

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = SPACE_HOME+"/media/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4=q1bqx0z=)brmyb(i0^14+ens949&fhi0wu-=-ksn5=dmm*@)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'shortys_shebeen.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'stories',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',    
    'django.contrib.comments',
    'registration',
    'djangoratings',
    'popularity',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'popularity.context_processors.most_popular',
    'popularity.context_processors.most_viewed',
    'popularity.context_processors.recently_viewed',
    'popularity.context_processors.recently_added',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'stories.AuthorProfile'

LOGIN_REDIRECT_URL = '/author/dashboard/'

LOGIN_URL = '/accounts/login/'

ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#Import facebook settings from a seperate file that is not in the repository
#This keeps the secret key secret
try:
    import facebook_settings   
    FACEBOOK_API_KEY = facebook_settings.FACEBOOK_API_KEY
    FACEBOOK_SECRET_KEY = facebook_settings.FACEBOOK_SECRET_KEY
    FACEBOOK_INTERNAL = facebook_settings.FACEBOOK_INTERNAL    
except:
    FACEBOOK_API_KEY = '00000000000000000000000000000000'
    FACEBOOK_SECRET_KEY = '00000000000000000000000000000000'
    FACEBOOK_INTERNAL = True



