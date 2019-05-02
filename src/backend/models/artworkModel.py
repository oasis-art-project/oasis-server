"""
Boston University. Spring 2019
@author: Maxim Tsybanov (oasis@tsybanov.com)
"""

from marshmallow import fields, validate, post_dump

from src.backend.extensions import db
from src.backend.models.model import BaseSchema, SurrogatePK
from src.backend.models.userModel import UserSchema, User


class Artwork(SurrogatePK, db.Model):
    __tablename__ = 'artworks'
    artist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    photo = db.Column(db.String(1000), nullable=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    artist = db.relationship('User', backref=db.backref('artworks'))

    def __init__(self, **kwargs):
        super(Artwork, self).__init__(**kwargs)


class ArtworkSchema(BaseSchema):
    # Overwritten fields
    artist = fields.Nested(UserSchema, only=('id',), required=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    description = fields.Str(validate=validate.Length(max=1000))

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
            data['artist'] = UserSchema(only=('id', 'firstName', 'lastName', 'bio', 'avatar', 'twitter', 'flickr', 'instagram')).dump(host).data
        return data