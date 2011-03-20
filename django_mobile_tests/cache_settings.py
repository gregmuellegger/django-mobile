from settings import *


MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
) + MIDDLEWARE_CLASSES + (
    'django_mobile.cache.middleware.CacheFlavourMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)
