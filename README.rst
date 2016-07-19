=============
django-mobile
=============

|build| |package|

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
   ``loaders`` list for ``TEMPLATES`` setting in ``settings.py``.
6. Add ``django_mobile.context_processors.flavour`` to your
   ``context_processors`` list for ``TEMPLATES`` setting. You can read more about ``loaders`` and ``context_processors`` in `Django docs`_.

*Note:* If you are using Django 1.7 or older, you need to change step 5 and 6 slightly. Use the ``TEMPLATE_LOADERS`` and ``TEMPLATE_CONTEXT_PROCESSORS`` settings instead of ``TEMPLATES``.

Now you should be able to use **django-mobile** in its glory. Read below of how
things work and which settings can be tweaked to modify **django-mobile**'s
behaviour.


Usage
=====

.. _flavours:

The concept of **django-mobile** is build around the ideas of different
*flavours* for your site. For example the *mobile* version is described as
one possible *flavour*, the desktop version as another.

This makes it possible to provide many possible designs instead of just
differentiating between a full desktop experience and one mobile version.  You
can make multiple mobile flavours available e.g. one for mobile safari on the
iPhone and Android as well as one for Opera and an extra one for the internet
tablets like the iPad.

*Note:* By default **django-mobile** only distinguishes between *full* and
*mobile* flavour.

After the correct flavour is somehow chosen by the middlewares, it's
assigned to the ``request.flavour`` attribute. You can use this in your views
to provide separate logic.

This flavour is then use to transparently choose custom templates for this
special flavour. The selected template will have the current flavour prefixed
to the template name you actually want to render. This means when
``render_to_response('index.html', ...)`` is called with the *mobile* flavour
being active will actually return a response rendered with the
``mobile/index.html`` template. However if this flavoured template is not
available it will gracefully fallback to the default ``index.html`` template.

In some cases its not the desired way to have a completely separate templates
for each flavour. You can also use the ``{{ flavour }}`` template variable to
only change small aspects of a single template. A short example:

.. code-block:: html+django

    <html>
    <head>
        <title>My site {% if flavour == "mobile" %}(mobile version){% endif %}</title>
    </head>
    <body>
        ...
    </body>
    </html>

This will add ``(mobile version)`` to the title of your site if viewed with
the mobile flavour enabled.

*Note:* The ``flavour`` template variable is only available if you have set up the
``django_mobile.context_processors.flavour`` context processor and used
django's ``RequestContext`` as context instance to render the template.

Changing the current flavour
----------------------------

The basic use case of **django-mobile** is obviously to serve a mobile version
of your site to users. The selection of the correct flavour is usually already
done in the middlewares when your own views are called. In some cases you want
to change the currently used flavour in your view or somewhere else. You can
do this by simply calling ``django_mobile.set_flavour(flavour[,
permanent=True])``. The first argument is self explaining. But keep in mind
that you only can pass in a flavour that you is also in your ``FLAVOURS``
setting. Otherwise ``set_flavour`` will raise a ``ValueError``. The optional
``permanent`` parameters defines if the change of the flavour is remember for
future requests of the same client.

Your users can set their desired flavour them self. They just need to specify
the ``flavour`` GET parameter on a request to your site. This will permanently
choose this flavour as their preference to view the site.

You can use this GET parameter to let the user select from your available
flavours:

.. code-block:: html+django

    <ul>
        <li><a href="?flavour=full">Get the full experience</a>
        <li><a href="?flavour=mobile">View our mobile version</a>
        <li><a href="?flavour=ipad">View our iPad version</a>
    </ul>

Notes on caching
----------------

.. _caching:

Django is shipping with some convenience methods to easily cache your views.
One of them is ``django.views.decorators.cache.cache_page``. The problem with
caching a whole page in conjunction with **django-mobile** is, that django's
caching system is not aware of flavours. This means that if the first request
to a page is served with a mobile flavour, the second request might also
get a page rendered with the mobile flavour from the cache -- even if the
second one was requested by a desktop browser.

**django-mobile** is shipping with it's own implementation of ``cache_page``
to resolve this issue. Please use ``django_mobile.cache.cache_page`` instead
of django's own ``cache_page`` decorator.

You can also use django's caching middlewares
``django.middleware.cache.UpdateCacheMiddleware`` and
``FetchFromCacheMiddleware`` like you already do. But to make them aware of
flavours, you need to add
``django_mobile.cache.middleware.FetchFromCacheFlavourMiddleware`` item before standard Django ``FetchFromCacheMiddleware``
in the ``MIDDLEWARE_CLASSES`` settings and ``django_mobile.cache.middleware.UpdateCacheFlavourMiddleware`` before 
``django_mobile.cache.middleware.UpdateCacheMiddleware`` correspondingly.

It is necessary to split the usage of ``CacheMiddleware`` because some additional work should be done on request and response *before* standard caching behavior and that is not possible while using two complete middlewares in either order

Reference
=========

``django_mobile.get_flavour([request,] [default])``
    Get the currently active flavour. If no flavour can be determined it will
    return *default*. This can happen if ``set_flavour`` was not called before
    in the current request-response cycle. *default* defaults to the first
    item in the ``FLAVOURS`` setting.

``django_mobile.set_flavour(flavour, [request,] [permanent])``
    Set the *flavour* to be used for *request*. This will raise ``ValueError``
    if *flavour* is not in the ``FLAVOURS`` setting. You can try to set the
    flavour permanently for *request* by passing ``permanent=True``. This may
    fail if you are out of a request-response cycle. *request* defaults to the
    currently active request.

``django_mobile.context_processors.flavour``
    Context processor that adds the current flavour as *flavour* to the
    context.

``django_mobile.context_processors.is_mobile``
    This context processor will add a *is_mobile* variable to the context
    which is ``True`` if the current flavour equals the
    ``DEFAULT_MOBILE_FLAVOUR`` setting.

``django_mobile.middleware.SetFlavourMiddleware``
    Takes care of loading the stored flavour from the user's session or
    cookies (depending on ``FLAVOURS_STORAGE_BACKEND``) if set. Also sets the
    current request to a thread-local variable. This is needed to provide
    ``get_flavour()`` functionality without having access to the request
    object.

``django_mobile.middleware.MobileDetectionMiddleware``
    Detects if a mobile browser tries to access the site and sets the flavour
    to ``DEFAULT_MOBILE_FLAVOUR`` settings value in case.

``django_mobile.cache.cache_page``
    Same as django's ``cache_page`` decorator, but wraps the view into
    additional decorators before and after that. Makes it possible to serve multiple
    flavours without getting into trouble with django's caching that doesn't
    know about flavours.

``django_mobile.cache.vary_on_flavour_fetch`` ``django_mobile.cache.vary_on_flavour_update``
    Decorators created from the ``FetchFromCacheFlavourMiddleware`` and ``UpdateCacheFlavourMiddleware`` middleware.

``django_mobile.cache.middleware.FetchFromCacheFlavourMiddleware``
    Adds ``X-Flavour`` header to ``request.META`` in ``process_request``

``django_mobile.cache.middleware.UpdateCacheFlavourMiddleware``
    Adds ``X-Flavour`` header to ``response['Vary']`` in ``process_response`` so that Django's ``CacheMiddleware`` know that it should take into account the content of this header when looking up the cached content on next request to this URL.


Customization
=============

.. _customization:

There are some points available that let you customize the behaviour of
**django-mobile**. Here are some possibilities listed:

``MobileDetectionMiddleware``
-----------------------------

The built-in middleware to detect if the user is using a mobile browser served
well in production but is far from perfect and also implemented in a very
simplistic way. You can safely remove this middleware from your settings and
add your own version instead. Just make sure that it calls
``django_mobile.set_flavour`` at some point to set the correct flavour for
you.

If you need example how tablet detection can be implemented, you can checkout the `middleware.py`_ file in directory `examples`. Feel free to modify it as you like!

Settings
--------

.. _settings:

Here is a list of settings that are used by **django-mobile** and can be
changed in your own ``settings.py``:

``FLAVOURS``
    A list of available flavours for your site.
    
    **Default:** ``('full', 'mobile')``

``DEFAULT_MOBILE_FLAVOUR``
    The flavour which is chosen if the built-in ``MobileDetectionMiddleware``
    detects a mobile browser.
    
    **Default:** ``'mobile'``

``FLAVOURS_COOKIE_HTTPONLY``
    The value that get passed into ``HttpResponse.set_cookie``'s ``httponly``
    argument. Set this to ``True`` if you don't want the Javascript code to be
    able to read the flavour cookie.
    
    **Default:** ``False``

``FLAVOURS_COOKIE_KEY``
    The cookie name that is used for storing the selected flavour in the
    browser.  This is only used if ``FLAVOURS_STORAGE_BACKEND`` is set to
    ``'cookie'``.
    
    **Default:** ``'flavour'``

``FLAVOURS_TEMPLATE_PREFIX``
    This string will be prefixed to the template names when searching for
    flavoured templates. This is useful if you have many flavours and want to
    store them in a common subdirectory. Example:
    
    .. code-block:: python
    
        from django.template.loader import render_to_string
        from django_mobile import set_flavour

        set_flavour('mobile')
        render_to_string('index.html') # will render 'mobile/index.html'

        # now add this to settings.py
        FLAVOURS_TEMPLATE_PREFIX = 'flavours/'

        # and try again

        set_flavour('mobile')
        render_to_string('index.html') # will render 'flavours/mobile/index.html'
    
    **Default:** ``''`` (empty string)

``FLAVOURS_TEMPLATE_LOADERS``
    **django-mobile**'s template loader can load templates prefixed with the
    current flavour. Specify with this setting which loaders are used to load
    flavoured templates.
    
    **Default:** same as ``TEMPLATE_LOADERS`` setting but without
    ``'django_mobile.loader.Loader'``.

``FLAVOURS_GET_PARAMETER``
    Users can change the flavour they want to look at with a HTTP GET
    parameter.  This determines the name of this parameter.  Set it to
    ``None`` to disable.
    
    **Default:** ``'flavour'``

``FLAVOURS_SESSION_KEY``
    The user's preference set with the GET parameter is stored in the user's
    session. This setting determines which session key is used to hold this
    information.
    
    **Default:** ``'flavour'``

``FLAVOURS_STORAGE_BACKEND``
    Determines how the selected flavour is stored persistently. Available
    values: ``'session'`` and ``'cookie'``.
    
    **Default:** ``'cookie'``

Cache Settings
--------------

Django ships with the `cached template loader`_
``django.template.loaders.cached.Loader`` that doesn't require to fetch the
template from disk every time you want to render it. However it isn't aware of
django-mobile's flavours. For this purpose you can use
``'django_mobile.loader.CachedLoader'`` as a drop-in replacement that does
exactly the same django's version but takes the different flavours into
account. To use it, put the following bit into your ``settings.py`` file:

.. code-block:: python

   TEMPLATES = [
      {
         ...
         'OPTIONS': {
            ...
            'loaders': ('django_mobile.loader.CachedLoader', (
               'django_mobile.loader.Loader',
               'django.template.loaders.filesystem.Loader',
               'django.template.loaders.app_directories.Loader',
            )),
         }
      }
   ]

.. _cached template loader:
   https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader

.. _middleware.py:
   examples/middleware.py
.. _Django docs:
    https://docs.djangoproject.com/en/dev/topics/templates/#module-django.template.backends.django

.. |build| image:: https://travis-ci.org/gregmuellegger/django-mobile.svg?branch=master
    :alt: Build Status
    :scale: 100%
    :target: https://travis-ci.org/gregmuellegger/django-mobile
.. |package| image:: https://badge.fury.io/py/django-mobile.svg
    :alt: Package Version
    :scale: 100%
    :target: http://badge.fury.io/py/django-mobile
