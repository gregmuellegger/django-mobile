try:
    from django.template.engine import Engine
    from django.template.loaders.base import Loader as BaseLoader
except ImportError:  # Django < 1.8
    Engine = None
    from django.template.loader import BaseLoader, find_template_loader, get_template_from_string


def template_loader(loader_name):
    if Engine:
        return Engine.get_default().find_template_loader(loader_name)
    else:  # Django < 1.8
        return find_template_loader(loader_name)


def template_from_string(template_code):
    if Engine:
        return Engine().from_string(template_code)
    else:  # Django < 1.8
        return get_template_from_string(template_code)


def get_engine():
    if Engine:
        return Engine.get_default()
    else:  # Django < 1.8
        return None
