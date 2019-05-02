"""
Boston University. Spring 2019
@author: Maxim Tsybanov (oasis@tsybanov.com)
"""

import json

from flask import request
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from flask_restplus import Resource
from sqlalchemy.exc import OperationalError
from src.backend.controllers.controller import upload_files, load_request, delete_files
from src.backend.models.tokenModel import Token
from src.backend.models.userModel import User, UserSchema

user_schema = UserSchema()


class UserResource(Resource):
    @jwt_optional
    def get(self, user_id=None, user_email=None):
        """
        Gets a list of users
        """
        try:
            # Get all users
            if not user_id and not user_email:
                users = User.query.all()
                if current_user and current_user.is_admin():
                    return {"status": 'success', 'users': UserSchema(many=True).dump(users).data}, 200
                else:
                    return {"status": 'success',
                            'users': UserSchema(many=True, exclude=('email',)).dump(users).data}, 200

            # Get a specific user by id
            if user_id:
                user = User.get_by_id(user_id)

                if not user:
                    return {'message': 'User does not exist'}, 400

                if current_user and current_user.is_admin():
                    return {"status": 'success', 'user': user_schema.dump(user).data}, 200
                else:
                    return {"status": 'success', 'user': UserSchema(exclude=('email',)).dump(user).data}, 200

            # Get a specific user by email
            if user_email:
                if not current_user.is_admin():
                    return {'message': 'Not enough privileges'}, 401

                user = User.query.filter_by(email=user_email).first()

                if not user:
                    return {'message': 'User does not exist'}, 400

                return {"status": 'success', 'user': user_schema.dump(user).data}, 200

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
                return {'message': 'User already exists'}, 400

            # Check if current user tries to make himself as admin without authorization
            if user_json['role'] == 1 and (not current_user or not current_user.is_admin()):
                return {'message': 'Not enough privileges'}, 401

            # Process avatar from the request
            if 'files' in request.files:
                user_json['avatar'] = upload_files(request, 1)

            # Create a new user
            user = UserSchema().load(user_json).data
            user.save()
        except OperationalError:
            return {'message': 'Database error'}, 500

        token = Token.create_token(user.id)

        return {"status": 'success', 'token': token}, 201

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

            # Process avatar from the request
            if 'files' in request.files:
                if user_from_db.avatar:
                    delete_files(json.loads(user_from_db.avatar))
                user_json["avatar"] = upload_files(request, 1)

            # Save updated in the db
            user_from_db.update(**user_json)
        except OperationalError:
            return {'message': 'Database error'}, 500

        # Revoke old token of the user
        Token.revoke_token_by_user_identity(user_json["id"])

        # Create a new one
        token = Token.create_token(user_json["id"])

        # Return the new token
        return {"status": 'success', 'token': token}, 200

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

            # If avatar in the request, means just delete a specific photo instead of the whole user
            if 'avatar' in request.form and (str(current_user.id) == user_id or current_user.is_admin()):
                if user.avatar:
                    delete_files(json.loads(user.avatar))
                return {"status": 'success'}, 200

            # Deleting of users is available only for admins
            if not current_user.is_admin():
                return {'message': 'Not enough privileges'}, 401

            # Revoke the user's token
            Token.revoke_token_by_user_identity(user.id)

            # Delete the use
            user.delete()

            # Delete avatar from the disk after deleting of the user
            if user.avatar:
                delete_files(json.loads(user.avatar))

        except OperationalError:
            return {'message': 'Database error'}, 500

        return {"status": 'success'}, 200