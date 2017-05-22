#!python3
# -*- coding: utf-8 -*-

from channels.routing import route


channel_routing = [
    route("websocket.connect", 'testgameserver.wsconsumer.ws_connect'),
    route("websocket.receive", 'testgameserver.wsconsumer.ws_message'),
    route("websocket.disconnect", 'testgameserver.wsconsumer.ws_disconnect'),
]