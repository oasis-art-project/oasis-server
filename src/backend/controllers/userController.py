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
from src.backend.models.tokenModel import Token
from src.backend.models.userModel import User, UserSchema
from src.backend.extensions import storage

user_schema = UserSchema()


class UserResource(Resource):
    @jwt_optional
    def get(self, user_id=None, user_email=None, user_role=None):
        """
        Gets a list of users
        """
        try:
            # Return all users with the given role
            if user_role:
                users = User.query.filter_by(role=user_role).all()
                if current_user and current_user.is_admin():
                    data = UserSchema(many=True).dump(users).data                    
                else:
                    data = UserSchema(many=True, exclude=('email',)).dump(users).data
                return {"status": 'success', 'users': data}, 200

            # Get a specific user by id
            if user_id:
                user = User.get_by_id(user_id)

                if not user:
                    return {'message': 'User does not exist'}, 400

                if current_user and current_user.is_admin():
                    data = user_schema.dump(user).data
                else:
                    data = UserSchema(exclude=('email',)).dump(user).data
                return {"status": 'success', 'user': data}, 200

            # Get a specific user by email
            if user_email:
                if not current_user or not current_user.is_admin():
                    return {'message': 'Not enough privileges'}, 401

                user = User.query.filter_by(email=user_email).first()

                if not user:
                    return {'message': 'User does not exist'}, 400

                data = user_schema.dump(user).data
                return {"status": 'success', 'user': data}, 200

            # If no arguments passed, return all users
            else:
                users = User.query.all()
                if current_user and current_user.is_admin():
                    data = UserSchema(many=True).dump(users).data                    
                else:
                    data = UserSchema(many=True, exclude=('email',)).dump(users).data
                return {"status": 'success', 'users': data}, 200


        except OperationalError:
            return {'message': 'Database error'}, 500

    @jwt_optional
    def post(self):
        """
        Creates a new user
        """

        # Validate input data with load_request
        try:
            user_json = load_request(request, UserSchema())
        except IOError as e:
            return {'message': str(e)}, 400
        except ValueError as e:
            return {'message': json.loads(str(e))}, 422

        try:
            # Check if user exist in the database
            if User.query.filter_by(email=user_json['email']).first():
                return {'message': 'User already exists'}, 409

            # Check if current user tries to make himself as admin without authorization
            if user_json['role'] == 1 and (not current_user or not current_user.is_admin()):
                return {'message': 'Not enough privileges'}, 401

            # Create a new user
            user = UserSchema().load(user_json).data
            user.save()
            
        except OperationalError:
            return {'message': 'Database error'}, 500
        
        token = Token.create_token(user)
        storage.create_user_folder(user.id)

        return {"status": 'success', 'token': token, 'id': user.id}, 201

    @jwt_required
    def put(self):
        """
        Edits a user
        """

        # Validate input data with load_request
        try:
            user_json = load_request(request, UserSchema(), update=True, user=True)
        except IOError as e:
            return {'message': str(e)}, 400
        except ValueError as e:
            return {'message': json.loads(str(e))}, 422

        try:
            # Get user from db
            user_from_db = User.get_by_id(user_json["id"])

            # If not exists, raise an error
            if not user_from_db:
                return {'message': 'User does not exist'}, 400

            # Check if use tries to make himself as an admin without authorization
            if "role" in user_json:
                if user_json["role"] == 1 and not current_user.is_admin() \
                        or (not user_json["role"] == 1 and current_user.id != user_json["id"]):
                    return {'message': 'Not enough privileges'}, 401

            # If password in the request to update, generate hash before saving to db
            if "password" in user_json:
                user_from_db.set_password(user_json["password"])
                del user_json['password']

            # Save updated in the db
            user_from_db.update(**user_json)
        except OperationalError:
            return {'message': 'Database error'}, 500

        # Revoke old token of the user
        #Token.revoke_token_by_user_identity(user_json["id"])

        # Create a new one
        #token = Token.create_token(user_from_db)

        # Return the new token
        #return {"status": 'success', 'token': token, 'user': user_from_db}, 200
        return {"status": 'success'}, 200

    @jwt_required
    def delete(self):
        """
        Deletes a user
        """

        # Validate data from the request
        if 'id' not in request.form:
            return {'message': 'No input data provided'}, 400

        user_id = request.form['id']

        try:
            # Get user from db
            user = User.get_by_id(user_id)

            # If not exists, raise an error
            if not user:
                return {'message': 'User does not exist'}, 400

            # Deleting of users is available only for admins
            if not current_user.is_admin():
                return {'message': 'Not enough privileges'}, 401

            # Revoke the user's token
            Token.revoke_token_by_user_identity(user.id)

            # Delete the user
            user.delete()

             # Delete storage
            storage.delete_user_folder(user.id)

        except OperationalError:
            return {'message': 'Database error'}, 500

        return {"status": 'success'}, 200
