from django_mobile import get_flavour
from django_mobile.ua_detector import UADetector
from django_mobile.conf import settings


def flavour(request):
    return {
        'flavour': get_flavour(),
    }


def is_mobile(request):
    return {
        'is_mobile': get_flavour() == settings.DEFAULT_MOBILE_FLAVOUR,
    }


def is_mobile_user_agent(request):
    return {
        'is_mobile_user_agent': UADetector(request).is_user_agent_mobile()
    }
