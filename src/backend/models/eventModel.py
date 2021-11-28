# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from marshmallow import fields, validate, post_dump

from src.backend.extensions import db
from src.backend.models.model import SurrogatePK, BaseSchema
from src.backend.models.placeModel import PlaceSchema, Place
from src.backend.models.userModel import UserSchema, User
from src.backend.models.artworkModel import ArtworkSchema, Artwork
from src.backend.controllers.controller import build_image_list

artists_association_table = db.Table("artists_association",
                                     db.Column("artist", db.Integer, db.ForeignKey("users.id")),
                                     db.Column("event", db.Integer, db.ForeignKey("events.id")))

artworks_association_table = db.Table("artworks_association",
                                      db.Column("artwork", db.Integer, db.ForeignKey("artworks.id")),
                                      db.Column("event", db.Integer, db.ForeignKey("events.id")))

class Event(SurrogatePK, db.Model):
    __tablename__ = 'events'
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    alias = db.Column(db.String(50), nullable=True)

    link = db.Column(db.String(100), nullable=True)

    hubs_link = db.Column(db.String(10), nullable=True)
    youtube_link = db.Column(db.String(15), nullable=True)

    # gather_link = db.Column(db.String(10), nullable=True)    
    # zoom_link = db.Column(db.String(80), nullable=True)

    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    place = db.relationship('Place', backref=db.backref('events'))
    artists = db.relationship('User',
                              secondary="artists_association",
                              backref=db.backref('artists'))
    artworks = db.relationship('Artwork',
                               secondary="artworks_association",
                               backref=db.backref('artworks'))

    def __init__(self, **kwargs):
        super(Event, self).__init__(**kwargs)


class EventSchema(BaseSchema):
    # Overwritten fields
    place = fields.Nested(PlaceSchema, only=('id',), required=True)
    artists = fields.Nested(UserSchema, many=True, only=('id',))
    artworks = fields.Nested(ArtworkSchema, many=True, only=('id',))

    name = fields.Str(required=True, validate=validate.Length(max=100))
    description = fields.Str(validate=validate.Length(max=1000))
    alias = fields.Str(validate=validate.Length(max=50))

    link = fields.Str(validate=validate.Length(max=100))
    
    hubs_link = fields.Str(validate=validate.Length(max=10))
    youtube_link = fields.Str(validate=validate.Length(max=15))

    # gather_link = fields.Str(validate=validate.Length(max=10))    
    # zoom_link = fields.Str(validate=validate.Length(max=80))

    class Meta:
        # BaseSchema automatically generates fields based on the model
        model = Event

    # Since according to Nested schema loading is only with ID,
    # dump loads other non-sensitive data from DB, enumerated below
    @post_dump
    def get(self, data):
        if 'place' in data:
            place = Place.get_by_id(data['place']['id'])
            if not place:
                raise ValueError
            data['place'] = PlaceSchema(only=('id', 'tags', 'host', 'name', 'description', 'files', 'address', 'location', 'homepage', 'instagram', 'facebook', 'matterport_link', 'active')).dump(place).data

        if 'artists' in data:
            for index in range(len(data['artists'])):
                artist = User.get_by_id(data['artists'][index]['id'])
                if not artist:
                    raise ValueError
                d = UserSchema(only=('id', 'tags', 'firstName', 'lastName', 'bio', 'files', 'homepage', 'instagram', 'youtube', 'showChat', 'confirmed')).dump(artist).data
                data['artists'][index] = d

        if 'artworks' in data:
            for index in range(len(data['artworks'])):
                artwork = Artwork.get_by_id(data['artworks'][index]['id'])
                if not artwork:
                    raise ValueError
                d = ArtworkSchema(only=('id', 'tags', 'name', 'description', 'medium', 'size', 'year', 'link', 'creation_date', 'artist', 'files')).dump(artwork).data
                data['artworks'][index] = d

        if 'files' in data:
            data['fullImages'] = build_image_list('event', data['id'], data['files'], 'f')
            data['prevImages'] = build_image_list('event', data['id'], data['files'], 'p')

        return data
