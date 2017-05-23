#!python3
# -*- coding: utf-8 -*-

# In consumers.py
from channels import Group
from channels.sessions import channel_session


@channel_session
def ws_message(message):
    if message.content['text'].startswith('role'):
        if 'role' not in message.channel_session:
            message.channel_session['role'] = message.content['text'][4:]
            Group(message.channel_session['role']).add(message.reply_channel)
    elif message.content['text'].startswith('d'):
        # just to ignore pings
        if message.channel_session['role'] == 'manager':
            Group('player').send({'text': message['text'][1:]})
        else:
            Group('manager').send({'text': message['text'][1:]})


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    if 'role' in message.channel_session:
        Group(message.channel_session['role']).discard(message.reply_channel)
