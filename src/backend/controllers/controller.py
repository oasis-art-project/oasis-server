# -*- coding: utf-8 -*-

"""
Part of the OASIS ART PROJECT - https://github.com/orgs/oasis-art-project
Copyright (c) 2019-22 TEAM OASIS
License Artistic-2.0
"""

import imghdr
import json
import os
import uuid
import flask
from io import BytesIO
from PIL import Image, ImageOps
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

def resize_image(img, max_res):
    w = img.width
    h = img.height
    mx = max(w, h)
    if max_res < mx:
        r = float(w) / float(h)
        if h < w:
            w = max_res
            h = int(w / r)
        else:
            h = max_res
            w = int(r * h)
        resized_img = img.resize((w, h), Image.Resampling.LANCZOS)
        fixed_image = ImageOps.exif_transpose(resized_img)
        return fixed_image
    else:
        return img    

def upload_images(request, resource_kind, resource_id):
    allowed_ext = flask.current_app.config['ALLOWED_IMAGE_EXTENSIONS']
    max_prev_res = flask.current_app.config['MAX_IMAGE_PREV_RES']
    max_full_res = flask.current_app.config['MAX_IMAGE_FULL_RES']

    uploaded_images = {}
    files_dict = request.files.to_dict()
    for file_object in files_dict.values():
        try:      
            # imghdr reads headers of the file to determine the real type of the file, even the extension of it is different
            image_type = imghdr.what(file_object)

            # If image type is not in the list of allowed extensions, raise the error
            if image_type is None or image_type not in allowed_ext:
                raise IOError("Only {} files are allowed".format(", ".join(allowed_ext)))

            src_filename = secure_filename(file_object.filename)
            dst_name = ''
            make_unique = False
            if resource_kind == 'user':
                dst_name = "profile"                    
            elif resource_kind == 'place':
                dst_name = "place"
                make_unique = True
            elif resource_kind == 'event':
                dst_name = "event"                    
            elif resource_kind == 'artwork':
                dst_name = "artwork"
                make_unique = True

            src_file = BytesIO(file_object.read())
            file_object.seek(0)
            src_img = Image.open(src_file)

            if image_type != 'jpeg' or max_full_res < src_img.width or max_full_res < src_img.height:
                # Generate full-res and preview images
                rgb_img = src_img.convert('RGB')

                # Save full-res image
                full_img = resize_image(rgb_img, max_full_res)
                dst_ffile = BytesIO()                    
                full_img.save(dst_ffile, format='JPEG')
                dst_ffile.seek(0)
                ffile_object = FileStorage(dst_ffile, dst_name + ".jpg")

                # Save preview
                prev_img = resize_image(rgb_img, max_prev_res)
                dst_pfile = BytesIO()
                prev_img.save(dst_pfile, format='JPEG')
                dst_pfile.seek(0)
                pfile_object = FileStorage(dst_pfile, dst_name + "p.jpg")
            else:
                ffile_object = file_object

                # Save preview
                rgb_img = src_img.convert('RGB')
                prev_img = resize_image(rgb_img, max_prev_res)
                dst_pfile = BytesIO()
                prev_img.save(dst_pfile, format='JPEG')
                dst_pfile.seek(0)
                pfile_object = FileStorage(dst_pfile, dst_name + "p.jpg")

            src_img.close()
            
            if make_unique:
                dst_name = storage.create_unique_filename(resource_kind, resource_id, 'f', dst_name)

            furl = storage.file_upload(resource_kind, resource_id, 'f', ffile_object, 'image/jpeg', dst_name + ".jpg")
            purl = storage.file_upload(resource_kind, resource_id, 'p', pfile_object, 'image/jpeg', dst_name + ".jpg")
            uploaded_images[src_filename] = {'url':furl, 'preview':purl, 'type':ffile_object.mimetype}

        except Exception as e:
            print("Image conversion error:", e)
            raise e
  
    if not uploaded_images:
        raise ValueError('Request does not contain images')

    return uploaded_images

def list_images(resource_kind, resource_id, file_type):
    res = storage.list_folder_contents(resource_kind, resource_id, file_type)
    return res
    
def build_image_list(resource_kind, resource_id, resource_files, file_type):
    if not resource_files: return []
    prefix = resource_kind + 's'
    res = []
    filenames = resource_files.split(":")
    for fn in filenames:
        image_path = '%s/%d/%s/%s' % (prefix, resource_id, file_type, fn)
        res.append(image_path)
    return res
