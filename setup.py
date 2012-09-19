#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


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


long_description = u'\n\n'.join((
    file('README.rst', 'r').read().decode('utf-8'),
    file('CHANGES.rst', 'r').read().decode('utf-8'),
))
long_description = long_description.encode('utf-8')
long_description = UltraMagicString(long_description)


setup(
    name = 'django-mobile',
    version = '0.2.4',
    url = 'https://github.com/gregmuellegger/django-mobile',
    license = 'BSD',
    description = u'Detect mobile browsers and serve different template flavours to them.',
    long_description = long_description,
    author = UltraMagicString('Gregor Müllegger'),
    author_email = 'gregor@muellegger.de',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages = [
        'django_mobile',
        'django_mobile.cache',
    ],
    install_requires = ['setuptools'],
    tests_require = ['Django', 'mock'],
    test_suite = 'django_mobile_tests.runtests.runtests',
)
