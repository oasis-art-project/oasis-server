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

import boto3
import json

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
class UserResources(object):
    def __init__(self):
        self.s3 = None
        self.bucket = None

    def init_app(self, app):
        self.s3 = boto3.resource(
            "s3",
            aws_access_key_id=app.config["S3_KEY"],
            aws_secret_access_key=app.config["S3_SECRET"])
        self.bucket = self.s3.Bucket(app.config["S3_BUCKET"])

    def generate_presigned_post(self, file_name, file_type):
        post_data = self.s3.generate_presigned_post(
            Bucket = self.bucket,
            Key = file_name,
            Fields = {"acl": "public-read", "Content-Type": file_type},
            Conditions = [
                {"acl": "public-read"},
                {"Content-Type": file_type}
            ],
            ExpiresIn = 3600
        )
        
        return json.dumps({
            'data': post_data,
            'url': 'https://%s.s3.amazonaws.com/%s' % (self.bucket, file_name)
        })

    def create_user_folder(self, email):
        status = self.bucket.put_object(Key="users/" + email + "/")
        print(status)            

    def create_place_folder(self, email, name):
        status = self.bucket.put_object(Key="users/" + email + "/places/" + name + "/")
        print(status)


# Create extension instances
db = SQLAlchemy(model_class=CRUDMixin)
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()
manager = Manager()
resources = UserResources()

# Create and register Api (Flask-Restplus)
# TODO: doc can be used for Swagger docs generation
api_bp = Blueprint('api', __name__)
api = CustomApi(api_bp, doc='/docs/', version='1.0', title='OASIS API')
