# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

import flask
from flask import Blueprint
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restplus import Api
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy, Model

from os.path import exists, join, expanduser
from os import listdir, remove, makedirs
from shutil import copy, rmtree
from geopy.geocoders import Nominatim
import boto3
import botocore
import json
import os

# Mixin adds CRUD operations to all models
class CRUDMixin(Model):
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


# Custom Api since it doesn't support correct error handling yet
class CustomApi(Api):
    def handle_error(self, e):
        for val in flask.current_app.error_handler_spec.values():
            for handler in val.values():
                registered_error_handlers = list(filter(lambda x: isinstance(e, x), handler.keys()))
                if len(registered_error_handlers) > 0:
                    raise e
        return super().handle_error(e)


# Object wrapping an S3 bucket to store user resources
class Storage(object):
    def __init__(self):
        self.local = False
        self.upload_folder = ''
        self.resource = None
        self.client = None
        self.bucket_name = ''
        self.bucket = None

    def init_app(self, app):
        self.local = not app.config["S3_BUCKET"] or not app.config["AWS_ACCESS_KEY_ID"] or not app.config["AWS_SECRET_ACCESS_KEY"]
        if self.local: 
            self.upload_folder = expanduser(app.config["IMAGE_UPLOAD_FOLDER"])
            return

        self.resource = boto3.resource(
            "s3",
            aws_access_key_id = app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key = app.config["AWS_SECRET_ACCESS_KEY"])
        
        self.client = boto3.client(
            "s3",
            aws_access_key_id = app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key = app.config["AWS_SECRET_ACCESS_KEY"])
        
        self.bucket_name = app.config["S3_BUCKET"]
        self.bucket = self.resource.Bucket(self.bucket_name)

    def file_upload(self, resource_kind, resource_id, file_object, content_type, dest_name):
        prefix = resource_kind + 's'
        dest_path = '%s/%d/%s' % (prefix, resource_id, dest_name)

        if self.local: 
            fn = file_object
            url = join(self.upload_folder, dest_path)
            # copy(fn, url)
            with open(url, 'wb') as out: ## Open temporary file as bytes
                out.write(file_object.stream.read())            
        else:
            self.client.upload_fileobj(
                Fileobj = file_object,
                Bucket = self.bucket_name,
                Key = dest_path,
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": content_type
                }
            )
            url = 'https://%s.s3.amazonaws.com/%s' % (self.bucket_name, dest_path)

        return url

    def create_unique_filename(self, resource_kind, resource_id, filename):
        lst = self.list_folder_contents(resource_kind, resource_id)    

        parts = filename.split('.')
        if not parts: 
            return filename
        name0 = parts[0].lower()

        count = 0
        for fn in lst:
            bname = os.path.basename(fn)
            parts = bname.split('.')
            if parts:
                name = parts[0].lower()
                name = name.rsplit("-")[0]
                if name == name0:
                    count += 1

        res = name0 + "-" + str(count)

        return res

    def list_folder_contents(self, resource_kind, resource_id):
        prefix = resource_kind + 's'
        folder_path = '%s/%d/' % (prefix, resource_id)

        if self.local: 
            full_path = join(self.upload_folder, folder_path)
            images = listdir(full_path)
        else:
            res = self.bucket.objects.filter(Prefix=folder_path)
            images = []
            for it in res:
                if it.key == folder_path: continue
                url = 'https://%s.s3.amazonaws.com/%s' % (self.bucket_name, it.key)
                images += [url]

        return images

    def create_user_folder(self, uid):
        return self.create_folder("users/" + str(uid) + "/")

    def create_place_folder(self, pid):
        return self.create_folder("places/" + str(pid) + "/")

    def create_event_folder(self, eid):
        return self.create_folder("events/" + str(eid) + "/")

    def create_artwork_folder(self, aid):
        return self.create_folder("artworks/" + str(aid) + "/")

    def delete_user_folder(self, uid):
        return self.delete_folder("users/" + str(uid) + "/")

    def delete_place_folder(self, pid):
        return self.delete_folder("places/" + str(pid) + "/")

    def delete_event_folder(self, eid):
        return self.delete_folder("events/" + str(eid) + "/")

    def delete_artwork_folder(self, aid):
        return self.delete_folder("artworks/" + str(aid) + "/")

    def create_folder(self, folder_path):
        if self.local:
            fpath = join(self.upload_folder, folder_path)
            if not os.path.exists(fpath):
                makedirs(fpath)
            return None    
        else:
            status = self.bucket.put_object(Key=folder_path)
            return status  

    def delete_folder(self, folder_path):
        if self.local:
            if os.path.exists(folder_path):
                return rmtree(folder_path)
            return None    
        else:    
            try:
                self.resource.Object(self.bucket_name, folder_path).load()
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    return None
            except Exception as e:
                raise e

            objects_to_delete = self.resource.meta.client.list_objects(Bucket=self.bucket_name, Prefix=folder_path)
            delete_keys = {'Objects' : []}
            delete_keys['Objects'] = [{'Key' : k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]]
            status = self.resource.meta.client.delete_objects(Bucket=self.bucket_name, Delete=delete_keys)
            return status

    def delete_image_file(self, res, rid, fn):
        prefix = res + 's'
        full_path = '%s/%d/%s' % (prefix, rid, fn)

        if self.local: 
            remove(join(self.upload_folder, full_path))
        else:
            try:
                self.resource.Object(self.bucket_name, full_path).delete()
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    return None
            except Exception as e:
                raise e

# Create extension instances
db = SQLAlchemy(model_class=CRUDMixin)
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()
manager = Manager()
storage = Storage()
geolocator = Nominatim(user_agent="OASIS server")

# Create and register Api (Flask-Restplus)
# TODO: doc can be used for Swagger docs generation
api_bp = Blueprint('api', __name__)
api = CustomApi(api_bp, doc='/docs/', version='1.0', title='OASIS API')
