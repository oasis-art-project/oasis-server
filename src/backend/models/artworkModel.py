# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from marshmallow import fields, validate, post_dump

from src.backend.extensions import db
from src.backend.models.model import BaseSchema, SurrogatePK
from src.backend.models.userModel import UserSchema, User
from src.backend.controllers.controller import build_image_list


class Artwork(SurrogatePK, db.Model):
    __tablename__ = 'artworks'
    artist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    link = db.Column(db.String(100), nullable=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    artist = db.relationship('User', backref=db.backref('artworks'))

    def __init__(self, **kwargs):
        super(Artwork, self).__init__(**kwargs)


class ArtworkSchema(BaseSchema):
    # Overwritten fields
    artist = fields.Nested(UserSchema, only=('id',), required=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    description = fields.Str(validate=validate.Length(max=1000))
    link = fields.Str(validate=validate.Length(max=100))

    class Meta:
        # BaseSchema automatically generates fields based on the model
        model = Artwork

    # Since according to Nested schema loading is only with ID,
    # dump loads other non-sensitive data from DB, enumerated below
    @post_dump
    def get(self, data):
        if 'artist' in data:
            host = User.get_by_id(data['artist']['id'])
            if not host:
                raise ValueError
            d = UserSchema(only=('id', 'tags', 'firstName', 'lastName', 'bio', 'files', 'homepage', 'instagram', 'venmo')).dump(host).data
            data['artist'] = d
        if 'files' in data:
            data['images'] = build_image_list('artwork', data['id'], data['files'])
        return data
