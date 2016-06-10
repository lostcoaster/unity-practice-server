#!python3
# -*- coding: utf-8 -*-
from django.conf.urls import url
import shironeko.views

__author__ = 'lc'

urlpatterns = [
    url(r'^upload/', shironeko.views.upload_data),
    url(r'^$', shironeko.views.browse),
]