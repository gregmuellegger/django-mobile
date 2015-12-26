from django.views.decorators.cache import cache_page as _cache_page
from django.utils.decorators import decorator_from_middleware

from django_mobile.cache.middleware import CacheFlavourMiddleware, CacheFlavourRequestMiddleware, \
    CacheFlavourResponseMiddleware


__all__ = ('cache_page', 'vary_on_flavour')

vary_on_flavour = decorator_from_middleware(CacheFlavourMiddleware)
vary_on_flavour_request = decorator_from_middleware(CacheFlavourRequestMiddleware)
vary_on_flavour_response = decorator_from_middleware(CacheFlavourResponseMiddleware)


def cache_page(*args, **kwargs):
    '''
    Same as django's ``cache_page`` decorator, but wraps the view into
    ``vary_on_flavour_request`` and ``vary_on_flavour_response`` decorators.
    Makes it possible to serve multiple flavours without getting into trouble with django's caching that doesn't
    know about flavours.
    '''

    def flavoured_decorator(func):
        return vary_on_flavour_request(_cache_page(*args, **kwargs)(vary_on_flavour_response(func)))

    return flavoured_decorator
