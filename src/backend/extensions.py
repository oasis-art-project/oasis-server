# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-art
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


# Create extension instances
db = SQLAlchemy(model_class=CRUDMixin)
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()
manager = Manager()

# Create and register Api (Flask-Restplus)
# TODO: doc can be used for Swagger docs generation
api_bp = Blueprint('api', __name__)
api = CustomApi(api_bp, doc='/docs/', version='1.0', title='OASIS API')
