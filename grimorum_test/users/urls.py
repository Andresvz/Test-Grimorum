# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from .views import Login,Register


urlpatterns = [
        url(r'^$', Login.as_view(), name='login'),
        url(r'^register/$', Register.as_view(), name='register'),
        url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
]
