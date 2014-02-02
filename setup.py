#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
from setuptools import setup


def get_author(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    author = re.search("__author__ = u?['\"]([^'\"]+)['\"]", init_py).group(1)
    return author


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


long_description = u'\n\n'.join((
    open('README.rst', 'r').read(),
    open('CHANGES.rst', 'r').read(),
))


setup(
    name = 'django-mobile',
    version = get_version('django_mobile'),
    url = 'https://github.com/gregmuellegger/django-mobile',
    license = 'BSD',
    description = u'Detect mobile browsers and serve different template flavours to them.',
    long_description = long_description,
    author = get_author('django_mobile'),
    author_email = 'gregor@muellegger.de',
    keywords='django,mobile',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages = [
        'django_mobile',
        'django_mobile.cache',
    ],
    tests_require = ['Django', 'mock'],
    test_suite = 'django_mobile_tests.runtests.runtests',
)
