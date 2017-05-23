#!python3
# -*- coding: utf-8 -*-

# In consumers.py
from channels import Group
from channels.sessions import channel_session


@channel_session
def ws_message(message):
    if 'role' not in message.channel_session:
        if message['text'].startswith('role'):
            message.channel_session['role'] = message['text'][4:]
            Group(message.channel_session['role']).add(message.reply_channel)
    elif message.channel_session['role'] == 'manager':
        Group('player').send({'text': message['text']})
    else:
        Group('manager').send({'text': message['text']})


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    if 'role' in message.channel_session:
        Group(message.channel_session['role']).discard(message.reply_channel)
