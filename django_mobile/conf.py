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
                raise AttributeError, 'settings object has no attribute "%s"' % attr


class defaults(object):
    FLAVOURS = ('full', 'mobile',)
    DEFAULT_MOBILE_FLAVOUR = 'mobile'
    FLAVOURS_TEMPLATE_DIRS_PREFIX = ''
    FLAVOURS_GET_PARAMETER = 'flavour'
    FLAVOURS_SESSION_KEY = 'flavour'


settings = SettingsProxy(django_settings, defaults)
