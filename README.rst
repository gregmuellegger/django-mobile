django-mobile
=============

**django-mobile** provides a simple way to detect mobile browsers and gives
you tools at your hand to render some different templates to deliver a mobile
version of your site to the user.

The idea is to keep your views exactly the same but to transparently
interchange the templates used to render a response. This is done in two
steps:

1. A middleware determines the client's preference to view your site. E.g. if
he wants to use the mobile flavour or the full desktop flavour.

2. The template loader takes then care of choosing the correct templates based
on the flavour detected in the middleware.


Installation
============

*Pre-Requirements:* ``django_mobile`` depends on django's session framework. So
before you try to use ``django_mobile`` make sure that the sessions framework
is enabled and working.

1. Install ``django_mobile`` with your favourite python tool, e.g. with
``easy_install django_mobile`` or ``pip install django_mobile``.

2. Add ``django_mobile`` to your ``INSTALLED_APPS`` setting in the
``settings.py``.

3. Add ``django_mobile.middleware.MobileDetectionMiddleware`` to your
``MIDDLEWARE_CLASSES`` setting.

4. Add ``django_mobile.middleware.SwitchFlavourMiddleware`` to your
``MIDDLEWARE_CLASSES`` setting. Make sure it's listed *after*
``MobileDetectionMiddleware`` and also after ``SessionMiddleware``.

5. Add ``django_mobile.loader.Loader`` as first item to your
``TEMPLATE_LOADERS`` list in ``settings.py``.

No you should be able to use **django-mobile** in its glory. Read below of how
things work and which settings can be tweaked to modify **django-mobile**'s
behviour.

Usage
=====

Coming soon ...

Customization
=============

Coming soon ...

Settings
--------

FLAVOURS
^^^^^^^^

Default: ``('full', 'mobile')``

DEFAULT_MOBILE_FLAVOUR
^^^^^^^^^^^^^^^^^^^^^^

Default: ``mobile``

FLAVOURS_TEMPLATE_DIRS_PREFIX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default: ``''`` (empty string)

FLAVOURS_GET_PARAMETER
^^^^^^^^^^^^^^^^^^^^^^

Default: ``'flavour'``

FLAVOURS_SESSION_KEY
^^^^^^^^^^^^^^^^^^^^

Default: ``'flavour'``
