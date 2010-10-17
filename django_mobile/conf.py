# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings


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
                raise AttributeError, u'settings object has no attribute "%s"' % attr


class defaults(object):
    FLAVOURS = (u'full', u'mobile',)
    DEFAULT_MOBILE_FLAVOUR = u'mobile'
    FLAVOURS_TEMPLATE_PREFIX = u''
    FLAVOURS_GET_PARAMETER = u'flavour'
    FLAVOURS_SESSION_KEY = u'flavour'
    FLAVOURS_TEMPLATE_LOADERS = []
    for loader in django_settings.TEMPLATE_LOADERS:
        if loader != 'django_mobile.loader.Loader':
            FLAVOURS_TEMPLATE_LOADERS.append(loader)
    FLAVOURS_TEMPLATE_LOADERS = tuple(FLAVOURS_TEMPLATE_LOADERS)


settings = SettingsProxy(django_settings, defaults)
