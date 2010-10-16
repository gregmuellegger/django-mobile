from django.template.loaders import filesystem
from django.utils._os import safe_join
from django_mobile import get_flavour
from django_mobile.conf import settings


class Loader(filesystem.Loader):
    def load_template_source(self, template_name, template_dirs=None):
        template_name = safe_join(get_flavour(), template_name)
        if settings.FLAVOURS_TEMPLATE_DIRS_PREFIX:
            template_name = settings.FLAVOURS_TEMPLATE_DIRS_PREFIX + template_name
        return super(Loader, self).load_template_source(template_name, template_dirs)
