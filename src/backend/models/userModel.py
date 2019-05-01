"""
Boston University. Spring 2019
@author: Maxim Tsybanov (oasis@tsybanov.com)
"""

import flask_bcrypt

from marshmallow import validate, fields
from src.backend.extensions import db
from src.backend.models.model import SurrogatePK, BaseSchema


class User(SurrogatePK, db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.String(1000), nullable=True)
    role = db.Column(db.Integer, nullable=False)
    twitter = db.Column(db.String(30), nullable=True)
    flickr = db.Column(db.String(30), nullable=True)
    instagram = db.Column(db.String(30), nullable=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    token = ''

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if kwargs.get('password') is not None:
            self.password = flask_bcrypt.generate_password_hash(self.password)

    def __repr__(self):
        return "<User %s>" % self.email

    def set_password(self, password):
        self.password = flask_bcrypt.generate_password_hash(password)

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
    firstName = fields.Str(required=True, validate=[
        validate.Regexp('^[a-zA-Z]+$'),
        validate.Length(max=50)])
    lastName = fields.Str(required=True, validate=[
        validate.Regexp('^[a-zA-Z]+$'),
        validate.Length(max=50)])
    bio = fields.Str(allow_none=True, validate=validate.Length(max=1000))
    role = fields.Int(required=True, validate=validate.Range(min=1, max=4))
    twitter = fields.Str(allow_none=True, validate=[validate.Regexp('^[a-zA-Z0-9_]+$'), validate.Length(max=30)])
    flickr = fields.Str(allow_none=True, validate=[validate.Regexp('^[a-zA-Z0-9@]+$'), validate.Length(max=30)])
    instagram = fields.Str(allow_none=True, validate=[validate.Regexp('^[a-zA-Z0-9._]+$'), validate.Length(max=30)])
    token = fields.Str(load_only=True)
    creation_date = fields.DateTime(load_only=True)

    class Meta:
        # BaseSchema automatically generates fields based on the model
        model = User
