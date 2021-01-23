# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

import json

from flask import request
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from flask_restplus import Resource
from sqlalchemy.exc import OperationalError
from src.backend.controllers.controller import load_request
from src.backend.models.tokenModel import Token
from src.backend.models.userModel import User, UserSchema
from src.backend.models.placeModel import PlaceSchema, Place
from src.backend.models.eventModel import artists_association_table
from src.backend.extensions import storage

user_schema = UserSchema()
place_schema = PlaceSchema()


class HostResource(Resource):
    @jwt_optional
    def get(self, host_id=None):
        """
        Gets a list of hosts
        """
        try:
            # Get a specific artist by id
            if host_id:
                user = User.get_by_id(host_id)

                if not user:
                    return {'message': 'User does not exist'}, 400

                if current_user and current_user.is_admin():
                    return {'message': 'Admin user is not a host'}, 500

                else:
                    host_data = UserSchema(exclude=('email',)).dump(user).data

                    host_places = Place.query.filter_by(host_id=host_id).all()
                    place_data = place_schema.dump(host_places, many=True).data

                    all_data = host_data
                    all_data["places"] = place_data

                return {"status": 'success', 'user': all_data}, 200

            # If no arguments passed, return all artists
            else:
                users = User.query.filter_by(role=2).all()
                if current_user and current_user.is_admin():
                    data = UserSchema(many=True).dump(users).data                    
                else:
                    data = UserSchema(many=True, exclude=('email',)).dump(users).data
                return {"status": 'success', 'users': data}, 200

        except OperationalError:
            return {'message': 'Database error'}, 500
