import threading
from django_mobile.conf import settings


_local = threading.local()


def get_flavour(request=None, default=None):
    request = request or getattr(_local, 'request', None)
    flavour = getattr(request, 'flavour', None)
    if flavour is None:
        flavour = getattr(_local, 'flavour', None)
    return flavour or default or settings.FLAVOURS[0]


def set_flavour(flavour, request=None, permanent=True):
    if flavour not in settings.FLAVOURS:
        raise ValueError(
            u"'%r' is no valid flavour. Allowed flavours are: %s" % (
                flavour,
                ', '.join(settings.FLAVOURS),))
    request = request or getattr(_local, 'request', None)
    if request:
        request.flavour = flavour
        if permanent:
            request.session[settings.FLAVOURS_SESSION_KEY] = flavour
    _local.flavour = flavour


def _set_request(request):
    _local.request = request
