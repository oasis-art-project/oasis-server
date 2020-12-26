# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from flask_socketio import Namespace, emit, join_room
from flask_mail import Message
from flask import request
from src.backend.extensions import mail, sms
from src.backend.models.userModel import User, UserSchema

from copy import deepcopy

# Namespace with socket-io events for chatting system
class CustomNamespace(Namespace):
    def __init__(self, namespace=None):
        super(Namespace, self).__init__(namespace)
        self.rooms = {}
        self.users = {}
        self.unsent = {}

    def add_user(self, uid):
        count = 0
        if uid in self.users:
            count = self.users[uid]
        count += 1
        self.users[uid] = count
        return count

    def rem_user(self, uid):
        count = 0
        if uid in self.users:
            count = self.users[uid]
            count -= 1            
            if count < 1:
                self.users.pop(uid, None)
            else:
                self.users[uid] = count
        return count

    def inc_room(self, rid):
        count = 0
        if rid in self.rooms:
            count = self.rooms[rid]
        count += 1
        self.rooms[rid] = count
        return count

    def dec_room(self, rid):
        count = 0
        if rid in self.rooms:
            count = self.rooms[rid]
            count -= 1            
            if count < 1:
                print("Removing room data")
                self.rooms.pop(rid, None)
                self.unsent.pop(rid, None)
            else:
                self.rooms[rid] = count
        return count

    def on_connect(self):
        rid = request.args.get('roomId')
        uid = int(request.args.get('userId'))
        join_room(rid)
        print('>>>> user', uid, 'connected to room', rid)                
        self.add_user(uid)
        count = self.inc_room(rid)
        if 1 < count and rid in self.unsent:
            print("Sending unsent messages")
            msgs = self.unsent[rid]
            for data in msgs:
                emit("send_message", data, room=rid)
            del self.unsent[rid]
        print("Rooms", self.rooms)
        print("Users", self.users)

    def on_disconnect(self):
        rid = request.args.get('roomId')
        uid = int(request.args.get('userId'))
        self.dec_room(rid)
        self.rem_user(uid)
        print('>>>> user', uid, 'disconnected from room', rid)
        print("Rooms", self.rooms)
        print("Users", self.users)

    def on_send_message(self, data):
        rid = data['roomId']
        uid = int(data['userId'])
        count = 0
        if rid in self.rooms:
            count = self.rooms[rid]            
        print('>>>> Received message in room', rid, 'from user', uid, ':', data)
        print("Rooms", self.rooms)
        print("Count", count)
        if 1 < count:
            print("Sending message to room", rid)
            emit("send_message", data, room=rid)
        else:             
            orig_data = deepcopy(data)
            data['body'] = "User is offline, sending notification..."
            data['senderId'] = ''
            emit("send_message", data, room=rid)

            ids = [int(s) for s in rid.split('-')]
            if uid in ids: 
                ids.remove(uid)
            uid0 = ids[0]    

            if uid0 in self.users:
                # Sending in-app notification if user uid0 is logged in

                notif = {'from': uid, 'to': uid0, 'room': rid}
                emit("send_notification", notif, room="default")
            else:
                # Sending email/sms notification if user uid0 is not logged in
                user0 = User.get_by_id(uid0)

                txt = "Join OASIS chat room " + rid
                to_user_email = user0.email
                to_user_number = user0.phone

                # Email notification
                print("SENDING EMAIL TO USER", uid, to_user_email)
                msg = Message("Chat Notification", recipients=[to_user_email])
                msg.body = txt
                mail.send(msg)

                # SMS notification
                if to_user_number:
                    print("SENDING TEXT MESSAGE TO USER", uid, to_user_number)
                    sms.send(txt, to_user_number)

            print("Saving message to unsent list, sending notification from", uid, "to", uid0, "room", rid)
            msgs = []
            if rid in self.unsent:
                msgs = self.unsent[rid]
            msgs += [orig_data]
            self.unsent[rid] = msgs