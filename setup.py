#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
from setuptools import setup


README_PATH = os.path.join(os.path.dirname(__file__), "README.rst")
CHANGES_PATH = os.path.join(os.path.dirname(__file__), "CHANGES.rst")


def readfile(filename):
    if sys.version_info[0] >= 3:
        return open(filename, "r", encoding="utf-8").read()
    else:
        return open(filename, "r").read()


def get_author(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = readfile(os.path.join(package, "__init__.py"))
    author = re.search("__author__ = u?['\"]([^'\"]+)['\"]", init_py).group(1)
    return UltraMagicString(author)


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = readfile(os.path.join(package, "__init__.py"))
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


class UltraMagicString(object):
    """
    Taken from
    http://stackoverflow.com/questions/1162338/whats-the-right-way-to-use-unicode-metadata-in-setup-py
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __unicode__(self):
        return self.value.decode("UTF-8")

    def __add__(self, other):
        return UltraMagicString(self.value + str(other))

    def split(self, *args, **kw):
        return self.value.split(*args, **kw)


long_description = "\n\n".join((readfile(README_PATH), readfile(CHANGES_PATH),))


setup(
    name="django-mobile",
    version=get_version("django_mobile"),
    url="https://github.com/gregmuellegger/django-mobile",
    license="BSD",
    description=u"Detect mobile browsers and serve different template flavours to them.",
    long_description=long_description,
    author=get_author("django_mobile"),
    author_email="gregor@muellegger.de",
    keywords="django,mobile",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=["django_mobile", "django_mobile.cache",],
    install_requires=[
        "argparse",
        "coverage",
        "django<3 ; python_version<'3.8'",
        "django<4 ; python_version=='3.8'",
        "django-discover-runner",
        "mock",
        "pytest",
        "pytest-django",
    ],
    tests_require=["django", "mock"],
    test_suite="django_mobile_tests.runtests.runtests",
)
