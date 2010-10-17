from django.conf import settings as django_settings
from django.template import TemplateDoesNotExist
from django.template.loaders import app_directories, filesystem
from django.test import TestCase
from mock import patch
from django_mobile import get_flavour, set_flavour
from django_mobile.conf import settings


class BasicTests(TestCase):
    def test_set_flavour(self):
        set_flavour('full')
        self.assertEqual(get_flavour(), 'full')
        set_flavour('mobile')
        self.assertEqual(get_flavour(), 'mobile')

        self.assertRaises(ValueError, set_flavour, 'spam')


class TemplateLoaderTests(TestCase):
    def setUp(self):
        self.original_TEMPLATE_LOADERS = settings.TEMPLATE_LOADERS
        self.original_FLAVOURS_TEMPLATE_LOADERS = settings.FLAVOURS_TEMPLATE_LOADERS
        django_settings.TEMPLATE_LOADERS = (
            'django_mobile.loader.Loader',
        )
        django_settings.FLAVOURS_TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.load_template_source',
            'django.template.loaders.app_directories.load_template_source',
        )

    def tearDown(self):
        django_settings.TEMPLATE_LOADERS = self.original_TEMPLATE_LOADERS
        django_settings.FLAVOURS_TEMPLATE_LOADERS = self.original_FLAVOURS_TEMPLATE_LOADERS

    @patch.object(app_directories.Loader, 'load_template_source')
    @patch.object(filesystem.Loader, 'load_template_source')
    def test_loader_on_filesystem(self, filesystem_loader, app_directories_loader):
        filesystem_loader.side_effect = TemplateDoesNotExist()
        app_directories_loader.side_effect = TemplateDoesNotExist()

        from django_mobile.loader import Loader
        loader = Loader()

        set_flavour('mobile')

        try:
            loader.load_template_source('base.html', template_dirs=None)
        except TemplateDoesNotExist:
            pass

        self.assertEqual(filesystem_loader.call_args[0][0], 'mobile/base.html')
        self.assertEqual(app_directories_loader.call_args[0][0], 'mobile/base.html')

        set_flavour('full')
        try:
            loader.load_template_source('base.html', template_dirs=None)
        except TemplateDoesNotExist:
            pass

        self.assertEqual(filesystem_loader.call_args[0][0], 'full/base.html')
        self.assertEqual(app_directories_loader.call_args[0][0], 'full/base.html')
