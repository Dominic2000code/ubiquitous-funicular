from contextlib import contextmanager
from django.conf import settings


@contextmanager
def set_testing(value):
    original_value = settings.TESTING
    settings.TESTING = value
    yield
    settings.TESTING = original_value
