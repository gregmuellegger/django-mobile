from functools import wraps

from django.views.decorators.cache import cache_page as _django_cache_page
from django.utils.decorators import decorator_from_middleware
from django_mobile.cache.middleware import FetchFromCacheFlavourMiddleware, UpdateCacheFlavourMiddleware

__all__ = ('cache_page', 'vary_on_flavour_fetch', 'vary_on_flavour_update')


vary_on_flavour_fetch = decorator_from_middleware(FetchFromCacheFlavourMiddleware)
vary_on_flavour_update = decorator_from_middleware(UpdateCacheFlavourMiddleware)


def cache_page(*args, **kwargs):
    '''
    Same as django's ``cache_page`` decorator, but wraps the view into
    additional decorators before and after that. Makes it possible to serve multiple
    flavours without getting into trouble with django's caching that doesn't
    know about flavours.
    '''
    decorator = _django_cache_page(*args, **kwargs)
    def flavoured_decorator(func):
        return vary_on_flavour_fetch(decorator(vary_on_flavour_update(func)))
    return flavoured_decorator
