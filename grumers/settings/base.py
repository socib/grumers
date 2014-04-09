# coding: utf-8

"""Base settings shared by all environments"""
# Import global settings to make it easier to extend settings.
from django.conf.global_settings import *   # pylint: disable=W0614,W0401

#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'UTC'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
    ('ca', 'Catalan'),
    ('es', 'Español'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w3v&86e$)27nq+rvs1hhc!^-6)iw69b*=w!gt0xej+rj9k&4)*'

INSTALLED_APPS = (
    'grumers.apps.data',
    'grumers.apps.web',

    'south',
    'compressor',
    'ckeditor',
    'mptt',
    'django_tables2',
    'crispy_forms',
    'bootstrap3_datetime',
    'djgeojson',
    'localeurl',
    'modeltranslation',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.gis',
    'django.contrib.flatpages',
)

#==============================================================================
# Calculation of directories relative to the project module location
#==============================================================================

import os
import sys
import grumers as project_module

PROJECT_DIR = os.path.dirname(os.path.realpath(project_module.__file__))

PYTHON_BIN = os.path.dirname(sys.executable)
ve_path = os.path.dirname(os.path.dirname(os.path.dirname(PROJECT_DIR)))
# Assume that the presence of 'activate_this.py' in the python bin/
# directory means that we're running in a virtual environment.
if os.path.exists(os.path.join(PYTHON_BIN, 'activate_this.py')):
    # We're running with a virtualenv python executable.
    VAR_ROOT = os.path.join(os.path.dirname(PYTHON_BIN), 'var')
elif ve_path and os.path.exists(os.path.join(ve_path, 'bin',
                                'activate_this.py')):
    # We're running in [virtualenv_root]/src/[project_name].
    VAR_ROOT = os.path.join(ve_path, 'var')
else:
    # Set the variable root to a path in the project which is
    # ignored by the repository.
    VAR_ROOT = os.path.join(PROJECT_DIR, 'var')

if not os.path.exists(VAR_ROOT):
    os.mkdir(VAR_ROOT)

#==============================================================================
# Project URLS and media settings
#==============================================================================

ROOT_URLCONF = 'grumers.urls'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(VAR_ROOT, 'static')
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)


#==============================================================================
# Templates
#==============================================================================

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
)

#==============================================================================
# Middleware
#==============================================================================

MIDDLEWARE_CLASSES += (
    'localeurl.middleware.LocaleURLMiddleware',
)

#==============================================================================
# Auth / security
#==============================================================================

AUTHENTICATION_BACKENDS += (
)

#==============================================================================
# Miscellaneous project settings
#==============================================================================

#==============================================================================
# Third party app settings
#==============================================================================
CRISPY_TEMPLATE_PACK = 'bootstrap3'
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
COMPRESS_OUTPUT_DIR = 'CACHE'
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
    },
}
LOCALEURL_USE_ACCEPT_LANGUAGE = True
LOCALEURL_USE_SESSION = True
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('en', 'ca', 'es'),
    'es': ('ca',),
    'ca': ('es',),
}
