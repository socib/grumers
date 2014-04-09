#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='grumers',
    version='1.0',
    description="",
    author="Biel Frontera",
    author_email='data.centre@socib.es',
    url='',
    packages=find_packages(),
    package_data={'grumers': ['static/*.*', 'templates/*.*']},
    scripts=['manage.py'],
)
