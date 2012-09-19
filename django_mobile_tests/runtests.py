#!/usr/bin/env python
import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_mobile_tests.settings'
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, parent)


def runtests(*args):
    from django.conf import settings
    from django.test.utils import get_runner

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1)
    failures = test_runner.run_tests(
        args or [
            'django_mobile',
            'django_mobile_tests',
        ])
    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    runtests(*sys.argv[1:])
