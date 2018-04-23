from django.conf.urls import url
from django.shortcuts import render
from django_mobile.cache import cache_page


def index(request):
    return render(request, 'index.html')


urlpatterns = [
    url(r'^$', index),
    url(r'^cached/$', cache_page(60*10)(index)),
]
