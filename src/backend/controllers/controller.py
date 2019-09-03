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

                url = storage.passthrough_upload(resource_kind, resource_id, file_object)
                uploaded_images[file_object.filename] = {'url':url, 'type':file_object.mimetype}

            return uploaded_images

        except Exception as e:
            raise e

    else:
        raise ValueError('Request does not contain images')

def delete_images(resource_kind, resource_id):
    print("Remove images associated to the specified resource")






def upload_files(request, maximum_files, files_in_db=None):
    """
    Uploader of files help to manage loading of file
    :param request: class with .form and .files fields with data received from the client
    :param maximum_files: integer with maximum files allowed to save
    :param files_in_db: list with information about current files on the server for calculation purpose
    :return: json (dict) of new list of files
    """
    if 'files' not in request.files and len(request.files.getlist('files')) == 0:
        return

    files = request.files.getlist('files')

    if files_in_db and len(files_in_db) + len(files) > maximum_files:
        raise IOError('Total number of files can be only {}'.format(maximum_files))

    if len(files) > maximum_files:
        raise IOError('Maximum number of files is {}'.format(maximum_files))

    photos = list()

    for file in files:
        # imghdr reads headers of the file to determine the real type of the file, even the extension of it is different
        image_type = imghdr.what(file)

        # If image type is not in the list of allowed extensions, raise the error
        if image_type is None or image_type not in flask.current_app.config['ALLOWED_EXTENSIONS']:
            raise IOError("Only {} files are allowed".format(", ".join(flask.current_app.config['ALLOWED_EXTENSIONS'])))

        # Get path /uploads/ folder
        file_path = os.path.join(flask.current_app.root_path, flask.current_app.config['UPLOAD_FOLDER'])

        # Generate a unique name for the file, add its extension
        filename = str(uuid.uuid4()) + "." + image_type

        # Save file
        file.save(os.path.join(file_path, filename))

        # Add file to the list
        photos.append(filename)

    if files_in_db:
        # Update the final list of files with data from db
        photos += files_in_db

    return json.dumps(photos)


def delete_files(files):
    """
    Method deletes all passed files
    :param files: a list of files to delete
    """
    file_path = os.path.join(flask.current_app.root_path, flask.current_app.config['UPLOAD_FOLDER'])

    for file in files:
        os.remove(os.path.join(file_path, file))
