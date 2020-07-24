#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner
from functools import wraps


def measure_memory(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if sys.version_info[:2] >= (3, 4):
            import tracemalloc
            tracemalloc.start()

        return_value = f(*args, **kwds)

        if sys.version_info[:2] >= (3, 4):
            peak = tracemalloc.get_traced_memory()[1]
            print("Peak memory usage: {:.3f} MB".format(peak / 10**6))
            tracemalloc.stop()

        return return_value
    return wrapper


@measure_memory
def run_tests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'fstest.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    # failures = test_runner.run_tests(["minimalapp.tests"])
    failures = test_runner.run_tests(None)
    return failures


if __name__ == "__main__":  # pragma: no branch
    failures = run_tests()
    sys.exit(bool(failures))
