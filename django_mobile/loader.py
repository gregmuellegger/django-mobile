from django.template.exceptions import TemplateDoesNotExist
from django.template.loaders.cached import Loader as DjangoCachedLoader
from django_mobile import get_flavour
from django_mobile.conf import settings

from django.template.engine import Engine
from django.template.loaders.base import Loader as BaseLoader


class Loader(BaseLoader):
    is_usable = True
    _template_source_loaders = None

    def get_contents(self, origin):
        return origin.loader.get_contents(origin)

    def get_template_sources(self, template_name):
        template_name = self.prepare_template_name(template_name)
        for loader in self.template_source_loaders:
            try:
                for result in loader.get_template_sources(template_name):
                    yield result
            except ValueError:
                # The joined path was located outside this particular
                # template_dir (it might be inside another one, so this isn't
                # fatal).
                pass

    def prepare_template_name(self, template_name):
        template_name = u'%s/%s' % (get_flavour(), template_name)
        if settings.FLAVOURS_TEMPLATE_PREFIX:
            template_name = settings.FLAVOURS_TEMPLATE_PREFIX + template_name
        return template_name

    def get_template(self, template_name, skip=None):
        template_name = self.prepare_template_name(template_name)
        for loader in self.template_source_loaders:
            try:
                return loader.get_template(template_name, skip=skip)
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist("Tried %s" % template_name)

    @property
    def template_source_loaders(self):
        if not self._template_source_loaders:
            loaders = []
            for loader_name in settings.FLAVOURS_TEMPLATE_LOADERS:
                loader = Engine.get_default().find_template_loader(loader_name)
                if loader is not None:
                    loaders.append(loader)
            self._template_source_loaders = tuple(loaders)
        return self._template_source_loaders


class CachedLoader(DjangoCachedLoader):
    is_usable = True

    def cache_key(self, template_name, *args, **kwargs):
        if len(args) > 0:  # Django >= 1.9
            key = super(CachedLoader, self).cache_key(template_name, *args, **kwargs)
        else:
            key = template_name

        return '{0}:{1}'.format(get_flavour(), key)

    def get_template(self, template_name, skip=None):
        key = self.cache_key(template_name)
        template_tuple = self.get_template_cache.get(key)

        if template_tuple is TemplateDoesNotExist:
            raise TemplateDoesNotExist('Template not found: %s' % template_name)
        elif template_tuple is None:
            template, origin = self.get_template(template_name, skip=skip)
            if not hasattr(template, 'render'):
                try:
                    template = Engine.get_default().from_string(template)
                except TemplateDoesNotExist:
                    # If compiling the template we found raises TemplateDoesNotExist,
                    # back off to returning the source and display name for the template
                    # we were asked to load. This allows for correct identification (later)
                    # of the actual template that does not exist.
                    self.get_template_cache[key] = (template, origin)

            self.get_template_cache[key] = (template, None)

        return self.get_template_cache[key]
