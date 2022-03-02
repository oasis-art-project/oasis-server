# -*- coding: utf-8 -*-

"""
Part of the OASIS ART PROJECT - https://github.com/orgs/oasis-art-project
Copyright (c) 2019-22 TEAM OASIS
License Artistic-2.0
"""

import json

from flask import request
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from flask_restplus import Resource
from sqlalchemy.exc import OperationalError
from src.backend.controllers.controller import load_request
from src.backend.models.userModel import User, UserSchema
from src.backend.models.eventModel import EventSchema, Event
from src.backend.models.artworkModel import Artwork, ArtworkSchema
from src.backend.models.eventModel import artists_association_table
from src.backend.extensions import storage

user_schema = UserSchema()
artwork_schema = ArtworkSchema()
event_schema = EventSchema()

class ArtistResource(Resource):
    @jwt_optional
    def get(self, artist_id=None):
        """
        Gets a list of artists
        """
        try:
            # Get a specific artist by id
            if artist_id:
                user = User.get_by_id(artist_id)

                if not user:
                    return {'message': 'Admin user is not an artist'}, 500

                if current_user and current_user.is_admin():
                    data = user_schema.dump(user).data

                else:
                    artist_data = UserSchema(exclude=('email',)).dump(user).data
                    
                    q = Event.query.join(artists_association_table).join(User)
                    artist_events = q.filter((artists_association_table.c.artist == artist_id)).all()
                    event_data = event_schema.dump(artist_events, many=True).data

                    artist_artworks = Artwork.query.filter_by(artist_id=artist_id).all()
                    artwork_data = artwork_schema.dump(artist_artworks, many=True).data

                    all_data = artist_data
                    all_data["events"] = event_data
                    all_data["artworks"] = artwork_data

                return {"status": 'success', 'user': all_data}, 200

            # If no arguments passed, return all artists
            else:
                users = User.query.filter_by(role=3).all()
                if current_user and current_user.is_admin():
                    data = UserSchema(many=True).dump(users).data                    
                else:
                    data = UserSchema(many=True, exclude=('email',)).dump(users).data
                return {"status": 'success', 'users': data}, 200

        except OperationalError:
            return {'message': 'Database error'}, 500
