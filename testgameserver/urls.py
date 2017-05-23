#!python3
# -*- coding: utf-8 -*-

import testgameserver.views
from django.conf.urls import url

__author__ = 'lc'

urlpatterns = [
    # url(r'^update/', 'testgameserver.views.update'),
    url(r'^$', testgameserver.views.view),
]
