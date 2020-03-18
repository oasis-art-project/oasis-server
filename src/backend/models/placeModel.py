# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from marshmallow import fields, validate, post_dump

from sqlalchemy.types import ARRAY
from src.backend.extensions import db
from src.backend.models.model import SurrogatePK, BaseSchema
from src.backend.models.userModel import UserSchema, User


class Place(SurrogatePK, db.Model):
    __tablename__ = 'places'
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    address = db.Column(db.String(300), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    host = db.relationship('User', backref=db.backref('places'))

    def __init__(self, **kwargs):
        super(Place, self).__init__(**kwargs)


class PlaceSchema(BaseSchema):
    # Overwritten fields
    host = fields.Nested(UserSchema, only=('id',), required=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    description = fields.Str(validate=validate.Length(max=1000))
    address = fields.Str(required=True, validate=validate.Length(max=300))
    latitude = fields.Float(allow_none=True, validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(allow_none=True, validate=validate.Range(min=-180, max=180))

    class Meta:
        # BaseSchema automatically generates fields based on the model
        model = Place

    # Since according to Nested schema loading is only with ID,
    # dump loads other non-sensitive data from DB, enumerated below
    @post_dump
    def get(self, data):
        if 'host' in data:
            host = User.get_by_id(data['host']['id'])
            if not host:
                raise ValueError
            data['host'] = UserSchema(only=('id', 'tags', 'firstName', 'lastName', 'bio', 'files', 'twitter', 'flickr', 'instagram')).dump(host).data
        return data
