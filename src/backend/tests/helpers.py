# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

import json
import os

import flask

from src.backend.controllers.artworkController import artwork_schema
from src.backend.controllers.eventController import event_schema
from src.backend.controllers.placeController import place_schema
from src.backend.controllers.userController import user_schema
from src.backend.models.tokenModel import Token
from src.backend.models.userModel import User


#
# Header
#
def auth_header(token):
    return {
        'Content-type': 'multipart/form-data',
        'Authorization': 'Bearer {}'.format(token)
    }


#
# Params
#
def params(request):
    """
    Prepares request

    :param request: string request
    :return: processed json
    """
    parameters = {"request": json.dumps(request)}

    return parameters


###
# All methods below create according objects into the DB rather than make a request, return created objects
###

#
# User
#
def user_json():
    return {
        "email": "foo@bar.com",
        "password": "foobar",
        "firstName": "foo",
        "lastName": "bar",
        "twitter": "twitterLogin",
        "flickr": "flickrLogin",
        "instagram": "instagramLogin",
        "role": 2
    }


def create_user(**kwargs):
    data = user_json()

    if kwargs.get("json") is None:
        for arg in kwargs:
            data[arg] = kwargs.get(arg)
    else:
        data = kwargs.get("json")

    user, errors = user_schema.load(data)
    user.save()

    token = Token.create_token(user)
    dump = user_schema.dump(User.get_by_id(user.id)).data

    return user, token, dump


#
# Artwork
#
def artwork_json(artist):
    return {
        "artist": artist,
        "name": "foobar",
        "description": "foobar foobar",
    }


def create_artwork(artist, **kwargs):
    data = artwork_json(artist)

    if kwargs.get("json") is None:
        for arg in kwargs:
            data[arg] = kwargs.get(arg)
    else:
        data = kwargs.get("json")

    artwork = artwork_schema.load(data).data
    artwork.save()

    return artwork


#
# Place
#
def place_json(host):
    return {
        "host": host,
        "name": "foobar",
        "description": "foobar foobar",
        "address": "The long address"
    }


def create_place(host, **kwargs):
    data = place_json(host)

    if kwargs.get("json") is None:
        for arg in kwargs:
            data[arg] = kwargs.get(arg)
    else:
        data = kwargs.get("json")

    place = place_schema.load(data).data
    place.save()

    return place


#
# Event
#
def event_json(place, artists=None):
    _json = {
            "place": place,
            "artists": artists,
            "name": "foobar",
            "description": "foobar foobar",
            "startTime": "2019-01-01T20:00:00",
            "endTime": "2019-01-02T18:00:00"
            }

    if _json["artists"] is None:
        del _json["artists"]

    return _json


def create_event(place, artists=None, **kwargs):
    data = event_json(place, artists)

    if kwargs.get("json") is None:
        for arg in kwargs:
            data[arg] = kwargs.get(arg)
    else:
        data = kwargs.get("json")

    event = event_schema.load(data).data
    event.save()

    return event


#
# Images
#