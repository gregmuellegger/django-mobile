#!/usr/bin/env python
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line()

