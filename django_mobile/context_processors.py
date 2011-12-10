from django_mobile import get_flavour, get_platform
from django_mobile.conf import settings


def flavour(request):
    return {
        'flavour': get_flavour(),
    }


def platform(request):
    return {
        'client_platform': get_platform(request),
    }


def is_mobile(request):
    return {
        'is_mobile': get_flavour() == settings.DEFAULT_MOBILE_FLAVOUR,
    }
