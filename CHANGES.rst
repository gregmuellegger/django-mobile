Changlog
========

0.1.4
-----

* Fixed issue in template loader that only implemented
  ``load_template_source`` but no ``load_template``. Thanks to tylanpince,
  rwilcox and Frédéric Roland for the report.

0.1.3
-----

* Fixed issue with ``runserver`` command that didn't handled all request
  independed from each other. Thanks to bclermont and Frédéric Roland for the
  report.

0.1.2
-----

* Fixed unreferenced variable error in ``SetFlavourMiddleware``.

0.1.1
-----

* Fixed ``is_usable`` attribute for ``django_mobile.loader.Loader``. Thanks Michela Ledwidge for the report.

0.1.0
-----

* Initial release.
