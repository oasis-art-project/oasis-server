# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from flask import request
from flask_jwt_extended import jwt_required, jwt_optional, current_user
from flask_restplus import Resource
from src.backend.models.userModel import User
from src.backend.models.placeModel import Place
from src.backend.models.eventModel import Event
from src.backend.models.artworkModel import Artwork
from src.backend.controllers.controller import upload_images
from src.backend.extensions import storage

import json

class S3Resource(Resource):
    @jwt_optional
    def get(self, resource_id=None):
        """
        Retrieves an appropriate signed request for the file object. Adapted from        
        https://github.com/willwebberley/FlaskDirectUploader
        https://devcenter.heroku.com/articles/s3-upload-python
        """

        if not resource_id:
            return {'message': 'No input data provided'}, 400

        # Get a specific user by id
        resource_kind = request.args.get('resource-kind')

        resource = None
        if resource_kind == 'user':
            resource = User.get_by_id(resource_id)
            if resource.is_admin():
                return {'message': 'Not enough privileges'}, 401
        elif resource_kind == 'place':
            resource = Place.get_by_id(resource_id)
        elif resource_kind == 'event':
            resource = Event.get_by_id(resource_id)
        elif resource_kind == 'artwork':
            resource = Artwork.get_by_id(resource_id) 
        else:
            return {'message': 'Request contains an invalid argument'}, 400

        # If not exists, raise an error
        if not resource:
            return {'message': 'The requested %s does not exist' % (resource_kind)}, 400      

        # Load required data from the request
        file_name = request.args.get('file-name')
        file_type = request.args.get('file-type')
        
        try:
            req_dict = storage.generate_presigned_post(resource_kind, resource_id, file_name, file_type)

            return req_dict, 200

        except Exception as e:
            return {'message': str(e)}, 400

    @jwt_optional
    def post(self, resource_id=None):
        """
        Pass-through upload to S3
        """

        if not resource_id:
            return {'message': 'No input data provided'}, 400

        # Get a specific user by id
        resource_kind = request.args.get('resource-kind')

        resource = None
        if resource_kind == 'user':
            resource = User.get_by_id(resource_id)
            if resource.is_admin():
                return {'message': 'Not enough privileges'}, 401
        elif resource_kind == 'place':
            resource = Place.get_by_id(resource_id)
        elif resource_kind == 'event':
            resource = Event.get_by_id(resource_id)
        elif resource_kind == 'artwork':
            resource = Artwork.get_by_id(resource_id) 
        else:
            return {'message': 'Request contains an invalid argument'}, 400

        if not resource:
            return {'message': 'The requested %s does not exist' % (resource_kind)}, 400      

        try:
            upload_dict = upload_images(request, resource_kind, resource_id)            
            return {"status": 'success', "images": json.dumps(upload_dict)}, 200 

        except Exception as e:
            return {'message': str(e)}, 400