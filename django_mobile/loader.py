from django.template import TemplateDoesNotExist
from django.template.loader import find_template_loader, BaseLoader
from django_mobile import get_flavour
from django_mobile.conf import settings


class Loader(BaseLoader):
    is_usable = True

    def __init__(self, *args, **kwargs):
        loaders = []
        for loader_name in settings.FLAVOURS_TEMPLATE_LOADERS:
            loader = find_template_loader(loader_name)
            if loader is not None:
                loaders.append(loader)
        self.template_source_loaders = tuple(loaders)
        super(BaseLoader, self).__init__(*args, **kwargs)

    def prepare_template_name(self, template_name):
        template_name = u'%s/%s' % (get_flavour(), template_name)
        if settings.FLAVOURS_TEMPLATE_PREFIX:
            template_name = settings.FLAVOURS_TEMPLATE_PREFIX + template_name
        return template_name

    def load_template(self, template_name, template_dirs=None):
        template_name = self.prepare_template_name(template_name)
        for loader in self.template_source_loaders:
            try:
                return loader(template_name, template_dirs)
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist("Tried %s" % template_name)

    def load_template_source(self, template_name, template_dirs=None):
        template_name = self.prepare_template_name(template_name)
        for loader in self.template_source_loaders:
            if hasattr(loader, 'load_template_source'):
                try:
                    return loader.load_template_source(template_name, template_dirs)
                except TemplateDoesNotExist:
                    pass
        raise TemplateDoesNotExist("Tried %s" % template_name)
