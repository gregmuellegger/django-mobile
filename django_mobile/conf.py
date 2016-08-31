# -*- coding: utf-8 -*-
from django.conf import settings as django_settings
import django

CACHE_LOADER_NAME = 'django_mobile.loader.CachedLoader'
DJANGO_MOBILE_LOADER = 'django_mobile.loader.Loader'


class SettingsProxy(object):
    def __init__(self, settings, defaults):
        self.settings = settings
        self.defaults = defaults

    def __getattr__(self, attr):
        try:
            return getattr(self.settings, attr)
        except AttributeError:
            try:
                return getattr(self.defaults, attr)
            except AttributeError:
                raise AttributeError(u'settings object has no attribute "%s"' % attr)


class defaults(object):
    FLAVOURS = (u'full', u'mobile',)
    DEFAULT_MOBILE_FLAVOUR = u'mobile'
    FLAVOURS_TEMPLATE_PREFIX = u''
    FLAVOURS_GET_PARAMETER = u'flavour'
    FLAVOURS_STORAGE_BACKEND = u'cookie'
    FLAVOURS_COOKIE_KEY = u'flavour'
    FLAVOURS_COOKIE_HTTPONLY = False
    FLAVOURS_SESSION_KEY = u'flavour'
    FLAVOURS_TEMPLATE_LOADERS = []
    if django.VERSION[0] < 2 and django.VERSION[1] < 8 :
        TEMPLATES = django_settings.TEMPLATE_LOADERS
    else:
        TEMPLATES = django_settings.TEMPLATES[0]['OPTIONS']['loaders']
    for loader in TEMPLATES:
        if isinstance(loader, (tuple, list)) and loader[0] == CACHE_LOADER_NAME:
            for cached_loader in loader[1]:
                if cached_loader != DJANGO_MOBILE_LOADER:
                    FLAVOURS_TEMPLATE_LOADERS.append(cached_loader)
        elif loader != DJANGO_MOBILE_LOADER:
            FLAVOURS_TEMPLATE_LOADERS.append(loader)
    FLAVOURS_TEMPLATE_LOADERS = tuple(FLAVOURS_TEMPLATE_LOADERS)

settings = SettingsProxy(django_settings, defaults)
