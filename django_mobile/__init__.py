import threading
from django.core.exceptions import ImproperlyConfigured
from django_mobile.conf import settings


_local = threading.local()


if getattr(settings, 'FLAVOURS_SESSION_KEY', None):
    PLATFORM_NAME_SESSION_KEY = '%s_device_name' % settings.FLAVOURS_SESSION_KEY
else:
    PLATFORM_NAME_SESSION_KEY = None


def get_flavour(request=None, default=None):
    flavour = None
    request = request or getattr(_local, 'request', None)
    # get flavour from session if enabled
    if request and settings.FLAVOURS_SESSION_KEY:
        flavour = request.session.get(settings.FLAVOURS_SESSION_KEY, None)
    # check if flavour is set on request
    if not flavour and hasattr(request, 'flavour'):
        flavour = request.flavour
    # if set out of a request-response cycle its stored on the thread local
    if not flavour:
        flavour = getattr(_local, 'flavour', default)
    # if something went wrong we return the very default flavour
    if flavour not in settings.FLAVOURS:
        flavour = settings.FLAVOURS[0]
    return flavour


def set_flavour(flavour, request=None, permanent=False):
    if flavour not in settings.FLAVOURS:
        raise ValueError(
            u"'%r' is no valid flavour. Allowed flavours are: %s" % (
                flavour,
                ', '.join(settings.FLAVOURS),))
    request = request or getattr(_local, 'request', None)
    if request:
        request.flavour = flavour
        if permanent:
            if not settings.FLAVOURS_SESSION_KEY:
                raise ImproperlyConfigured(
                    u"You must specify the FLAVOURS_SESSION_KEY setting to "
                    u"use the 'permanent' parameter.")
            request.session[settings.FLAVOURS_SESSION_KEY] = flavour
    elif permanent:
        raise ValueError(
            u'Cannot set flavour permanently, no request available.')
    _local.flavour = flavour


def _set_request_header(request, flavour):
    request.META['HTTP_X_FLAVOUR'] = flavour


def _init_flavour(request):
    global _local
    _local = threading.local()
    _local.request = request
    if hasattr(request, 'flavour'):
        _local.flavour = request.flavour
    if not hasattr(_local, 'flavour'):
        _local.flavour = settings.FLAVOURS[0]


def get_platform(request=None, default=None):
    if getattr(_local, 'client_platform', None) is not None:
        return _local.client_platform
    request = request or getattr(_local, 'request', None)
    if getattr(request, 'client_platform', None) is not None:
        return request.client_platform
    if PLATFORM_NAME_SESSION_KEY and PLATFORM_NAME_SESSION_KEY in request.session:
        return request.session[PLATFORM_NAME_SESSION_KEY]
    return default


def set_platform(platform, request=None):
    _local.client_platform = platform
    request = request or getattr(_local, 'request', None)
    if request:
        request.client_platform = platform
        if PLATFORM_NAME_SESSION_KEY:
            request.session[PLATFORM_NAME_SESSION_KEY] = platform
