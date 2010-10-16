import threading
from django_mobile.conf import settings


_local = threading.local()


def get_flavour(request=None, default=None):
    request = request or getattr(_local, 'request', None)
    flavour = getattr(request, 'flavour', None)
    if flavour is None:
        flavour = getattr(_local, 'flavour', None)
    return flavour or default or settings.FLAVOURS[0]


def set_flavour(flavour):
    if flavour not in settings.FLAVOURS:
        raise ValueError(
            u"'%r' is no valid flavour. Allowed flavours are: %s" % (
                flavour,
                ', '.join(settings.FLAVOURS),))
    if hasattr(_local, 'request'):
        _local.request.flavour = flavour
    _local.flavour = flavour


def _set_request(request):
    _local.request = request
