..

INSTALL GRUMERS DJANGO APPLICATION
==================================


Requirements
------------

This project includes bootstrap less files, which are compiled into css via django-compressor and nodejs package lessc (see `lessc <http://lesscss.org>`_ ). You should install nodejs and lessc from node package manager::

    npm install -g less

You will also need an spatial database (see `geodjango requirements <https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#requirements>`_ ).


System packages::

    libgeos-3.2.0
    libgeos-dev
    binutils libproj-dev gdal-bin
    libldap2-dev libsasl2-dev (for LDAP Authentication)


Quickstart
----------

To configure the project in development::

    mkvirtualenv grumers --no-site-packages
    workon grumers
    cd path/to/grumers/repository
    pip install -r requirements/dev.pip
    pip install -e .
    cp grumers/settings/local.py.example grumers/settings/local.py
    python manage.py syncdb
    python manage.py migrate
    python manage.py runserver_plus


Production deployment
---------------------

This application can be deployed as any other django application.