from django.test import TestCase
from mock import Mock
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
