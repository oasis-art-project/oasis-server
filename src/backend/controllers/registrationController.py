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
                return {'message': 'User already exists'}, 400

            txt = json.dumps(user_json)

            # Email notification
            info_email = "info@oasis.art"
            print("SENDING EMAIL TO USER", info_email)
            msg = Message("New user request", recipients=[info_email])
            msg.body = txt
            mail.send(msg)
            
        except OperationalError:
            return {'message': 'Database error'}, 500
        
        return {"status": 'success'}, 200
