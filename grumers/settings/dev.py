"""Settings for Development Server"""
from grumers.settings.base import *   # pylint: disable=W0614,W0401

DEBUG = True
TEMPLATE_DEBUG = DEBUG

VAR_ROOT = '/var/www/grumers'
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'grumers',
        # 'USER': 'dbuser',
        # 'PASSWORD': 'dbpassword',
    }
}

# WSGI_APPLICATION = 'grumers.wsgi.dev.application'
