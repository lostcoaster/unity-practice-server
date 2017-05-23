#!python3
# -*- coding: utf-8 -*-

# In consumers.py
from channels import Group
from channels.sessions import channel_session


@channel_session
def ws_message(message):
    if 'role' not in message.channel_session:
        import json
        data = json.loads(message.content['text'])
        if 'role' in data:
            message.channel_session['role'] = data['role']
            Group(data['role']).add(message.reply_channel)
    elif message.channel_session['role'] == 'manager':
        Group('player').send({'text': message['text']})
    else:
        Group('manager').send({'text': message['text']})


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    if 'role' in message.channel_session:
        Group(message.channel_session['role']).discard(message.reply_channel)
