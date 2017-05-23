# -*- coding: utf-8 -*-
#!python3
# this file contains settings overrides that are meant to be used on real server
# but don't abuse this file as most other files rely on the original setting file's content.


__author__ = 'lostcoaster'

from .settings import *

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     },
# }

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_ipc.IPCChannelLayer",
        "ROUTING": "hubserver.routing.channel_routing",
        "CONFIG": {
            "prefix": "hubserver",
        },
    },
}