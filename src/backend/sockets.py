# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from flask_socketio import Namespace, emit, join_room
from flask_mail import Message
from flask import request
from src.backend.extensions import mail

from copy import deepcopy

# Namespace with socket-io events for chatting system
class CustomNamespace(Namespace):
    def __init__(self, namespace=None):
        super(Namespace, self).__init__(namespace)
        self.rooms = {}
        self.unsent = {}

    def on_connect(self):
        id = request.args.get('roomId')
        print('>>>> user connected to room', id)
        join_room(id)
        count = 0
        if id in self.rooms:
            count = self.rooms[id]
        count += 1
        self.rooms[id] = count
        if 1 < count and id in self.unsent:
            print("Sending unsent messages")
            msgs = self.unsent[id]
            for data in msgs:
                emit("send_message", data, room=id)
            del self.unsent[id]
        print("Rooms", self.rooms)

    def on_disconnect(self):
        id = request.args.get('roomId')
        if id in self.rooms:
            count = self.rooms[id]
            count -= 1            
            if count < 1:
                print("Removing room data")
                # del self.rooms[id]
                self.rooms.pop(id, None)
                self.unsent.pop(id, None)
            else:
                self.rooms[id] = count
        print('Client disconnected')
        print("Rooms", self.rooms)

    def on_send_message(self, data):
        roomId = data['roomId']
        userId = data['userId']
        count = 0
        if roomId in self.rooms:
            count = self.rooms[roomId]            
        print('>>>> Received message in room', roomId, 'from user', userId, ':', data)
        print("Rooms", self.rooms)
        print("Count", count)
        if 1 < count:
            print("Sending message to room", roomId)
            emit("send_message", data, room=roomId)
        else:             
            orig_data = deepcopy(data)
            data['body'] = "User is offline, sending notification..."
            data['senderId'] = ''
            emit("send_message", data, room=roomId)

            ids = roomId.split('-')
            ids.remove(userId)

            # Sent message notification if user ids[0] is logged in
            print("Saving message to unsent list, sending notification to", ids[0])
            notif = {'from': userId, 'to': ids[0], 'roomId': roomId}
            emit("send_notification", notif, broadcast=True)

            # Sent email notification if user ids[0] is not logged in
            msg = Message("Chat Notification", recipients=['andres.colubri@gmail.com'])
            msg.body = "Join OASIS chat room " + roomId
            mail.send(msg)

            # Other notifications, SMS, WhatsApp...?

            msgs = []
            if roomId in self.unsent:
                msgs = self.unsent[roomId]
            msgs += [orig_data]
            self.unsent[roomId] = msgs