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
def params(request, num_files=0):
    """
    Prepares request

    :param request: string request
    :param num_files: how many files to send simultaneously (0-2)
    :return: processed json
    """
    parameters = {"request": json.dumps(request)}

    # Prepare files for sending
    if num_files > 0:
        if num_files == 1:
            files = ("test1.png", )
        elif num_files == 2:
            files = ("test1.png", "test2.png")
        else:
            raise ValueError("Can be only 1 or 2")

        # Read files from the disk, open into File instances...
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = {"files": [open(os.path.join(dir_path, file), 'rb') for file in files]}

        # ... and save it in parameters json
        parameters.update(files)

    return parameters


#
# Remove files after a test
#
def remove_files(files):
    """
    Removes files. Usually after a test

    :param files: list of files to remove
    """
    file_path = os.path.join(flask.current_app.root_path, flask.current_app.config['UPLOAD_FOLDER'])

    for file in files:
        os.remove(os.path.join(file_path, file))

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

    token = Token.create_token(user.id)
    dump = user_schema.dump(User.get_by_id(user.id))

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

    artwork = artwork_schema.load(data)
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

    place = place_schema.load(data)
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

    event = event_schema.load(data)
    event.save()

    return event
