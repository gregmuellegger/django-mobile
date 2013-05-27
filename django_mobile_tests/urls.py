try:
    from django.conf.urls.defaults import *
except ImportError:
    from django.conf.urls import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_mobile.cache import cache_page


def index(request):
    return render_to_response('index.html', {
    }, context_instance=RequestContext(request))


urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^cached/$', cache_page(60*10)(index)),
)
