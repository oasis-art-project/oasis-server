# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from flask import request
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from flask_restplus import Resource
from src.backend.extensions import resources

import json


class UploadResource(Resource):
    @jwt_optional
    def get(self, user_id=None, user_email=None):
        """
        Retrieves an appropriate signed request for the file object
        """
        # try:

        # except OperationalError:
        #     return {'message': 'Unprocessable entity'}, 422
        # request_data = resources.generate_presigned_post(file_name, file_type)

        print("GET signed request") 

        return {"status": 'success'}, 200

    @jwt_optional
    def post(self, user_id=None, user_email=None):
        """
        Retrieves an appropriate signed request for the file object
        """
        # try:

        # except OperationalError:
        #     return {'message': 'Unprocessable entity'}, 422
        # request_data = resources.generate_presigned_post(file_name, file_type)

        print("POST image") 

        return {"status": 'success'}, 200        