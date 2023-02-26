import warnings

from django.utils.deprecation import MiddlewareMixin
from django.utils.cache import patch_vary_headers
from django_mobile import get_flavour, _set_request_header


class CacheFlavourMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        warnings.warn('CacheFlavourMiddleware does nothing and should be abandoned.'
                      'The intended behavior cannot be implemented using one middleware.'
                      'Use separate FetchFromCacheFlavourMiddleware and UpdateCacheFlavourMiddleware instead.'
                      'Refer to https://github.com/gregmuellegger/django-mobile/pull/64 for details',
                      category=DeprecationWarning)


class FetchFromCacheFlavourMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _set_request_header(request, get_flavour(request))


class UpdateCacheFlavourMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        patch_vary_headers(response, ['X-Flavour'])
        return response
