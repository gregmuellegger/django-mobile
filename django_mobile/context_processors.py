from django_mobile import get_flavour,get_device_name
from django_mobile.conf import settings


def flavour(request):
    return {
        'flavour': get_flavour(),
    }

def get_device(request):
	return {
        'device_info': get_device_name(),
    }


def is_mobile(request):
    return {
        'is_mobile': get_flavour() == settings.DEFAULT_MOBILE_FLAVOUR,
    }
