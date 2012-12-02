from django_mobile import get_flavour
from django_mobile.conf import settings

DEFAULT_MOBILE_FLAVOUR = settings.DEFAULT_MOBILE_FLAVOUR


def flavour(request):
    return {
        'flavour': get_flavour(),
    }


def is_mobile(request):
    return {
        'is_mobile': get_flavour() == DEFAULT_MOBILE_FLAVOUR,
    }
