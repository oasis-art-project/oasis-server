# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

import imghdr
import json
import os
import uuid
import flask
from io import BytesIO
from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask_jwt_extended import current_user
from src.backend.extensions import storage


def load_request(request, schema, update=False, user=False):
    """
    Base loader helps to reuse same logic for each data loading
    :param request: class with .form and .files fields with data received from the client
    :param schema: schema that has to be used with the data (UserSchema, ArtworkSchema etc.)
    :param update: if true, checks if field 'id' in the request since updating is happening by id
    :param user: if true, assign ID of the current user (authorized) as 'id' in the request
    :return: processed json (dict) data
    """

    # Check the field 'request' in request
    if 'request' not in request.form:
        raise IOError("No input data provided")
    json_data = request.form['request']
    if json_data == "null":
        raise IOError("No request")

    # Check if data is valid json
    try:
        json_data = json.loads(json_data)
    except ValueError as e:
        raise IOError("Request is not valid json. {}".format(e))

    # Check for ID if its updating
    if update and 'id' not in json_data:
        if user:
            json_data['id'] = current_user.id
        else:
            raise IOError("Id is missing")

    # Validate data with model schema
    errors = schema.validate(json_data, partial=update)
    if errors:
        raise ValueError(json.dumps(errors))

    return json_data

def upload_images(request, resource_kind, resource_id):
    if 'images' not in request.files:
        raise IOError('Request contains an invalid argument')
        
    if 'images' in request.files:
        try:
            images = request.files.getlist('images')

            uploaded_images = {}
            for file_object in images:
                # imghdr reads headers of the file to determine the real type of the file, even the extension of it is different
                image_type = imghdr.what(file_object)
 
                # If image type is not in the list of allowed extensions, raise the error
                if image_type is None or image_type not in flask.current_app.config['ALLOWED_EXTENSIONS']:
                    raise IOError("Only {} files are allowed".format(", ".join(flask.current_app.config['ALLOWED_EXTENSIONS'])))

                src_filename = secure_filename(file_object.filename)
                dst_name = ''
                make_unique = True
                if resource_kind == 'user':
                    dst_name = "profile"
                    make_unique = False
                elif resource_kind == 'place':
                    dst_name = "place"
                elif resource_kind == 'event':
                    dst_name = "event"
                elif resource_kind == 'artwork':
                    dst_name = "artwork"

                if image_type != 'jpeg':
                    # Convert image into jpeg in memory using BytesIO
                    src_file = BytesIO(file_object.read())
                    src_img = Image.open(src_file)
                    rgb_img = src_img.convert('RGB')
                    dst_file = BytesIO()                    
                    rgb_img.save(dst_file, format='JPEG')
                    # Return the file pointer to the beginning after saving, otherwise it will be uploaded empty
                    dst_file.seek(0)
                    # Wrap the memory file holding the converted file as a FileStorage object for upload
                    file_object = FileStorage(dst_file, dst_name + ".jpg")

                if make_unique:
                    dst_name = storage.create_unique_filename(resource_kind, resource_id, dst_name)

                url = storage.passthrough_upload(resource_kind, resource_id, file_object, 'image/jpeg', dst_name + ".jpg")
                uploaded_images[src_filename] = {'url':url, 'type':file_object.mimetype}

            return uploaded_images

        except Exception as e:
            raise e

    else:
        raise ValueError('Request does not contain images')


def list_images(request, resource_kind, resource_id):
    res = storage.list_folder_contents(resource_kind, resource_id)
    return res
