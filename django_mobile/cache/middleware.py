import warnings

from django.utils.cache import patch_vary_headers
from django_mobile import get_flavour, _set_request_header
from django.utils.deprecation import MiddlewareMixin


class CacheFlavourMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        warnings.warn('CacheFlavourMiddleware does nothing and should be abandoned.'
                      'The intended behavior cannot be implemented using one middleware.'
                      'Use separate FetchFromCacheFlavourMiddleware and UpdateCacheFlavourMiddleware instead.'
                      'Refer to https://github.com/gregmuellegger/django-mobile/pull/64 for details',
                      category=DeprecationWarning)
        super(CacheFlavourMiddleware, self).__init__()


class FetchFromCacheFlavourMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _set_request_header(request, get_flavour(request))


class UpdateCacheFlavourMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        patch_vary_headers(response, ['X-Flavour'])
        return response
