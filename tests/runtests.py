#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner


def run_tests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'fstest.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    # failures = test_runner.run_tests(["minimalapp.tests"])
    failures = test_runner.run_tests(None)
    sys.exit(bool(failures))


if __name__ == "__main__":  # pragma: no branch
    run_tests()
