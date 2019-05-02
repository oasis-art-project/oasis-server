"""
Boston University. Spring 2019
@author: Maxim Tsybanov (oasis@tsybanov.com)
"""

from marshmallow import fields, validate, post_dump

from src.backend.extensions import db
from src.backend.models.model import SurrogatePK, BaseSchema
from src.backend.models.userModel import UserSchema, User


class Place(SurrogatePK, db.Model):
    __tablename__ = 'places'
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    address = db.Column(db.String(300), nullable=False)
    photo = db.Column(db.String(1000), nullable=True)
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
            data['host'] = UserSchema(only=('id', 'firstName', 'lastName', 'bio', 'avatar', 'twitter', 'flickr', 'instagram')).dump(host).data
        return data