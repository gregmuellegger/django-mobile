#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys
from setuptools import setup

README_PATH = os.path.join(os.path.dirname(__file__), 'README.rst')
CHANGES_PATH = os.path.join(os.path.dirname(__file__), 'README.rst')

def get_author(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    author = re.search("__author__ = u?['\"]([^'\"]+)['\"]", init_py).group(1)
    return UltraMagicString(author)


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


class UltraMagicString(object):
    '''
    Taken from
    http://stackoverflow.com/questions/1162338/whats-the-right-way-to-use-unicode-metadata-in-setup-py
    '''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __unicode__(self):
        return self.value.decode('UTF-8')

    def __add__(self, other):
        return UltraMagicString(self.value + str(other))

    def split(self, *args, **kw):
        return self.value.split(*args, **kw)

if sys.version_info[0] >= 3 :
    long_description = u'\n\n'.join((
        open(README_PATH, 'r').read(),
        open(CHANGES_PATH, 'r').read(),
    ))
else :
    long_description = u'\n\n'.join((
        open(README_PATH, 'r').read().decode('utf-8'),
        open(CHANGES_PATH, 'r').read().decode('utf-8'),
    ))
    long_description = long_description.encode('utf-8')
    long_description = UltraMagicString(long_description)


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
