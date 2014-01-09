#!/usr/bin/env python
import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_mobile_tests.settings'
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, parent)


def runtests(*args):
    from django.core import management

    if not args:
        args = [
            'django_mobile',
            'django_mobile_tests',
        ]
    args = ['runtests.py', 'test'] + list(args)
    management.execute_from_command_line(args)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
