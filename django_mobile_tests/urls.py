try:
    from django.conf.urls.defaults import *
except ImportError:
    from django.urls import *
from django.shortcuts import render
from django_mobile.cache import cache_page


def index(request):
    return render(request, 'index.html', {})


urlpatterns = [
    path('', index),
    path('cached/', cache_page(60*10)(index)),
]
