from django_mobile import get_flavour
from django_mobile.conf import settings

DEFAULT_MOBILE_FLAVOUR = settings.DEFAULT_MOBILE_FLAVOUR
TEMPLATE_FLAVOUR_KEY = settings.FLAVOURS_TEMPLATE_FLAVOUR_KEY
TEMPLATE_IS_MOBILE_KEY = settings.FLAVOURS_TEMPLATE_IS_MOBILE_KEY


def flavour(request):
    return {
        TEMPLATE_FLAVOUR_KEY: get_flavour(),
    }


def is_mobile(request):
    return {
        TEMPLATE_IS_MOBILE_KEY: get_flavour() == DEFAULT_MOBILE_FLAVOUR,
    }
