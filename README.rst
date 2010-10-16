django-mobile
=============

.. _introduction:

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

.. _installation:

*Pre-Requirements:* ``django_mobile`` depends on django's session framework. So
before you try to use ``django_mobile`` make sure that the sessions framework
is enabled and working.

1. Install ``django_mobile`` with your favourite python tool, e.g. with
``easy_install django_mobile`` or ``pip install django_mobile``.

2. Add ``django_mobile`` to your ``INSTALLED_APPS`` setting in the
``settings.py``.

3. Add ``django_mobile.middleware.MobileDetectionMiddleware`` to your
``MIDDLEWARE_CLASSES`` setting.

4. Add ``django_mobile.middleware.SetFlavourMiddleware`` to your
``MIDDLEWARE_CLASSES`` setting. Make sure it's listed *after*
``MobileDetectionMiddleware`` and also after ``SessionMiddleware``.

5. Add ``django_mobile.loader.Loader`` as first item to your
``TEMPLATE_LOADERS`` list in ``settings.py``.

6. Add ``django_mobile.context_processors.flavour`` to your
``TEMPLATE_CONTEXT_PROCESSORS`` setting.

No you should be able to use **django-mobile** in its glory. Read below of how
things work and which settings can be tweaked to modify **django-mobile**'s
behviour.


Usage
=====

.. _flavours:

The concept of **django-mobile** is build around the ideas of different
*flavours* of your site. For example the *mobile* version is described as
one possible *flavour* of your site.

This makes it possible to provide many possible *flavours* instead of just
differentiating between a full desktop experience and one mobile version. You
can make multiple mobile flavours available e.g. one for mobile safari on the
iPhone and Android as well as one for Opera and an extra one for the internet
tablets like the iPad.

.. note:
    By default **django-mobile** only distinguish between the flavours
    *full* and *mobile*.

After the correct flavour is somehow chosen by the middlewares, it's
assigned to the ``request.flavour`` attribute. You can use this in your views
to provide seperate logic for each flavour.

This flavour is then use to transparently choose custom templates for this
special flavour. The selected template will have the current flavour prefixed
to the template name you actually want to render. This means when
``render_to_response('index.html', ...)`` is called with the *mobile* flavour
beeing active will actually return a response rendered with the
``mobile/index.html`` template. However if this flavoured template is not
available it will gracefully fallback to the default ``index.html`` template.

In some cases its not the desired way to have a completly seperate templates
for each flavour. You can also use the ``{{ flavour }}`` template variable to
only change small aspects of a single template. A short example::

    <html>
    <head>
        <title>My site {% if flavour == "mobile" %}(mobile version){% endif %}</title>
    </head>
    <body>
        ...
    </body>
    </html>

This will add ``(mobile version)`` to the title of your site if viewed with
the *mobile* flavour enabled.

.. note:
   The ``flavour`` template variable is only available if you have setup the
   ``django_mobile.context_processors.flavour`` context processor and used
   django's ``RequestContext`` as context instance to render the template.


Customization
=============

Settings
--------

.. _settings:

FLAVOURS
^^^^^^^^

A list of available flavours for your site.

Default: ``('full', 'mobile')``

DEFAULT_MOBILE_FLAVOUR
^^^^^^^^^^^^^^^^^^^^^^

The flavour which is choosen if the builtin ``MobileDetectionMiddleware``
detects a mobile browser.

Default: ``mobile``

FLAVOURS_TEMPLATE_DIRS_PREFIX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This string will be prefixed to the template names when searching for
flavoured templates. This is usefull if have many flavours and want to store
them in a common subdirectory. Example::

    from django.conf import settings
    from django.template.loader import render_to_string
    from django_mobile import set_flavour

    set_flavour('mobile')
    render_to_string('index.html') # will render 'mobile/index.html'

    # now add this to settings.py
    FLAVOURS_TEMPLATE_DIRS_PREFIX = 'flavours/'

    # and try again

    set_flavour('mobile')
    render_to_string('index.html') # will render 'flavours/mobile/index.html'

Default: ``''`` (empty string)

FLAVOURS_GET_PARAMETER
^^^^^^^^^^^^^^^^^^^^^^

Users can change the flavour they want to look at with a HTTP GET parameter.
This determines the name of this parameter.

Default: ``'flavour'``

FLAVOURS_SESSION_KEY
^^^^^^^^^^^^^^^^^^^^

The user's prefernce set with the GET parameter is stored in the user's
session. This setting determines which session key is used to hold this
information.

Default: ``'flavour'``
