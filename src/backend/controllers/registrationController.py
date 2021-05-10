# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

import json

from flask import request
from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required
from flask_restplus import Resource
from src.backend.controllers.controller import load_request
from sqlalchemy.exc import OperationalError
from src.backend.models.userModel import User, RegisterSchema
from src.backend.jwt import blacklist
from flask_mail import Message
from src.backend.extensions import mail

class RegistrationResource(Resource):
    def post(self):
        """
        Creates a new user
        """

        # Validate input data with load_request
        try:
            user_json = load_request(request, RegisterSchema())
        except IOError as e:
            return {'message': str(e)}, 400
        except ValueError as e:
            return {'message': json.loads(str(e))}, 422

        try:
            # Check if user exist in the database
            if User.query.filter_by(email=user_json['email']).first():
                return {'message': 'User already exists'}, 409

            # txt = json.dumps(user_json)
            user_role = "visitor"
            if user_json['role'] == 2:
                user_role = "host"
            elif user_json['role'] == 3:
                user_role = "artist"                

            txt = "First name = " + user_json['firstName'] + "\n"
            txt += "Last name = " + user_json['lastName'] + "\n"
            txt += "Email address = " + user_json['email'] + "\n"
            txt += "Phone number = " + user_json['phone'] + "\n"
            txt += "User role = " + user_role + "\n"
            txt += "Short bio = " + user_json['bio'] + "\n"
            txt += "Website = " + user_json['website'] + "\n"
            txt += "Instagram = " + user_json['instagram'] + "\n"
            txt += "YouTube = " + user_json['youtube']

            # Email notification
            info_email = "info@oasis.art"
            msg = Message("NEW USER REGISTRATION", recipients=[info_email])
            msg.body = txt

            mail.send(msg)
            
        except OperationalError:
            return {'message': 'Database error'}, 500
        
        return {"status": 'success'}, 200
