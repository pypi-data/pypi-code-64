# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views


app_name = 'search'
urlpatterns = [
    url(r'^$', views.SearchView(), name='search'),
]
