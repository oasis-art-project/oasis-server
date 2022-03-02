# -*- coding: utf-8 -*-

"""
Part of the OASIS ART PROJECT - https://github.com/orgs/oasis-art-project
Copyright (c) 2019-22 TEAM OASIS
License Artistic-2.0
"""

import flask_bcrypt

from marshmallow import fields, validate, post_dump

from src.backend.extensions import db
from src.backend.models.model import SurrogatePK, BaseSchema
from src.backend.controllers.controller import build_image_list


class User(SurrogatePK, db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)    
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.String(2000), nullable=True)
    role = db.Column(db.Integer, nullable=False)    
    homepage = db.Column(db.String(100), nullable=True)
    instagram = db.Column(db.String(30), nullable=True)
    youtube = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(10), nullable=True)
    showChat = db.Column(db.Boolean, nullable=True)
    confirmed = db.Column(db.Boolean, nullable=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    token = ''

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if kwargs.get('password') is not None:
            self.password = flask_bcrypt.generate_password_hash(self.password).decode("utf-8", "ignore")

    def __repr__(self):
        return "<User %s>" % self.email

    def set_password(self, password):
        self.password = flask_bcrypt.generate_password_hash(password).decode("utf-8", "ignore")

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    def is_admin(self):
        return self.role == 1

    def is_host(self):
        return self.role == 2

    def is_artist(self):
        return self.role == 3

    def is_visitor(self):
        return self.role == 4


class UserSchema(BaseSchema):
    # Overwritten fields
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True)
    firstName = fields.Str(required=True, validate=validate.Length(max=50))
    lastName = fields.Str(allow_none=True, validate=validate.Length(max=50))
    bio = fields.Str(allow_none=True, validate=validate.Length(max=2000))
    role = fields.Int(required=True, validate=validate.Range(min=1, max=4))        
    homepage = fields.Str(allow_none=True, validate=validate.Length(max=100))
    instagram = fields.Str(allow_none=True, validate=validate.Length(max=30))
    youtube = fields.Str(allow_none=True, validate=validate.Length(max=30))
    phone = fields.Str(allow_none=True, validate=validate.Length(max=10))
    showChat = fields.Boolean(allow_none=True)
    confirmed = fields.Boolean(allow_none=False)
    creation_date = fields.DateTime(load_only=True)
    token = fields.Str(load_only=True)

    class Meta:
        # BaseSchema automatically generates fields based on the model
        model = User

    # dump list of images
    @post_dump
    def get(self, data):
        if 'files' in data:
            data['fullImages'] = build_image_list('user', data['id'], data['files'], 'f')
            data['prevImages'] = build_image_list('user', data['id'], data['files'], 'p')
        return data

class RegisterSchema(BaseSchema):
    # Overwritten fields
    email = fields.Email(required=True)
    password = fields.Str(allow_none=True, validate=validate.Length(min=6), load_only=True)
    firstName = fields.Str(required=True, validate=validate.Length(max=50))
    lastName = fields.Str(allow_none=True, validate=validate.Length(max=50))
    bio = fields.Str(allow_none=True, validate=validate.Length(max=2000))
    role = fields.Int(required=True, validate=validate.Range(min=1, max=4))        
    homepage = fields.Str(allow_none=True, validate=validate.Length(max=100))
    instagram = fields.Str(allow_none=True, validate=validate.Length(max=30))
    youtube = fields.Str(allow_none=True, validate=validate.Length(max=30))
    phone = fields.Str(allow_none=True, validate=validate.Length(max=10))
    showChat = fields.Boolean(allow_none=True)
    creation_date = fields.DateTime(load_only=True)
    token = fields.Str(load_only=True)

    class Meta:
        # BaseSchema automatically generates fields based on the model
        model = User