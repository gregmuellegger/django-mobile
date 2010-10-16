from django.template import TemplateDoesNotExist
from django.template.loaders import filesystem
from django.test import TestCase
from mock import Mock, patch
from django_mobile import get_flavour, set_flavour, get_default_flavour
from django_mobile.conf import settings


class BasicTests(TestCase):
    def test_set_flavour(self):
        set_flavour('full')
        self.assertEqual(get_flavour(), 'full')
        set_flavour('mobile')
        self.assertEqual(get_flavour(), 'mobile')

        self.assertRaises(ValueError, set_flavour, 'spam')

    def test_get_default_flavour(self):
        request = Mock()
        request.is_mobile = False
        self.assertEqual(get_default_flavour(request), settings.FLAVOURS[0])
        request.is_mobile = True
        self.assertEqual(get_default_flavour(request), settings.DEFAULT_MOBILE_FLAVOUR)


class TemplateLoaderTests(TestCase):
    def setUp(self):
        from django.conf import settings
        self.original_TEMPLATE_LOADERS = settings.TEMPLATE_LOADERS
        settings.TEMPLATE_LOADERS = ('django_mobile.loader.Loader',)

    def tearDown(self):
        settings.TEMPLATE_LOADERS = self.original_TEMPLATE_LOADERS

    def test_loader(self):
        from django_mobile.loader import Loader
        loader = Loader()

        with patch.object(filesystem.Loader, 'load_template_source') as method:
            set_flavour('mobile')
            try:
                loader.load_template_source('base.html', template_dirs=None)
            except TemplateDoesNotExist:
                pass

            self.assertEqual(method.call_count, 1)
            self.assertEqual(method.call_args[0][0], 'mobile/base.html')

        with patch.object(filesystem.Loader, 'load_template_source') as method:
            set_flavour('full')
            try:
                loader.load_template_source('base.html', template_dirs=None)
            except TemplateDoesNotExist:
                pass

            self.assertEqual(method.call_count, 1)
            self.assertEqual(method.call_args[0][0], 'full/base.html')
