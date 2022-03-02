# -*- coding: utf-8 -*-

"""
Part of the OASIS ART PROJECT - https://github.com/orgs/oasis-art-project
Copyright (c) 2019-22 TEAM OASIS
License Artistic-2.0
"""

import json

from flask import request
from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required
from flask_restplus import Resource
from sqlalchemy.exc import OperationalError
from src.backend.models.userModel import User
from src.backend.jwt import blacklist


class LoginResource(Resource):
    def post(self):
        """
        User login
        """

        # Validate data from the request
        if 'request' not in request.form \
                or 'email' not in request.form['request'] \
                or 'password' not in request.form['request']:
            return {'message': "No input data provided"}, 400

        try:
            login_json = json.loads(request.form['request'])

            # Check if user exist in the database
            user_from_db = User.query.filter_by(email=login_json["email"]).first()
            if not user_from_db:
                return {'message': 'User does not exist'}, 400

            # Check if password correct
            if not user_from_db.check_password(login_json["password"]):
                return {'message': 'Wrong password'}, 401
        except ValueError:
            return {"message": "Request is not valid json"}, 400
        except OperationalError:
            return {"message": "Database error"}, 500

        # If reached this point, everything is correct, then create a token
        user_full_name = (user_from_db.firstName + " " + user_from_db.lastName).strip()
        token = create_access_token(identity=user_from_db.id, user_claims={'fullName': user_full_name, 'email': user_from_db.email})

        # Return the token
        return {"status": 'success', 'token': token}, 200

    @jwt_required
    def delete(self):
        """
        User logout
        """

        # Adds current user token to blacklist
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)

        return {"status": 'success'}, 200
