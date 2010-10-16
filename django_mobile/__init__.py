import threading
from django_mobile.conf import settings


_local = threading.local()


def get_default_flavour(request):
    if getattr(request, 'is_mobile', False):
        return settings.DEFAULT_MOBILE_FLAVOUR
    return settings.FLAVOURS[0]


def get_flavour(request=None, default=None):
    if default is None:
        default = settings.FLAVOURS[0]
    return getattr(_local, 'flavour', default)


def set_flavour(flavour):
    if flavour not in settings.FLAVOURS:
        raise ValueError(
            u"'%r' is no valid flavour. Allowed flavours are: %s" % (
                flavour,
                ', '.join(settings.FLAVOURS),))
    _local.flavour = flavour
