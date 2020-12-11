# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from flask_socketio import Namespace, emit, join_room
from flask import request

roomId = 1
NEW_CHAT_MESSAGE_EVENT = "send_message"

# Namespace with socket-io events for chatting system
class CustomNamespace(Namespace):
    def on_connect(self):
        roomId = request.args.get('roomId')
        print('user connected to room', roomId)
        join_room(roomId)

    def on_disconnect(self):
        print('Client disconnected')

    def on_send_message(self, data):
        print('Received message in room', roomId, data)
        emit(NEW_CHAT_MESSAGE_EVENT, data, broadcast=True)