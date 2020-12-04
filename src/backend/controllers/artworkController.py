# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

import json

from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import joinedload

from src.backend.controllers.controller import load_request
from src.backend.models.artworkModel import Artwork, ArtworkSchema
from src.backend.extensions import storage

artwork_schema = ArtworkSchema()


class ArtworkResource(Resource):
    def get(self, artwork_id=None, artist_id=None):
        """
        Gets a list of artworks
        """
        try:
            # Return all artworks of artist with ID artist_id
            if artist_id:
                user_artworks = Artwork.query.filter_by(artist_id=artist_id).all()
                data = artwork_schema.dump(user_artworks, many=True).data
                return {"status": "success", 'artworks': data}, 200

            # Return a specific artwork with ID artwork_id
            if artwork_id:
                artwork = Artwork.query.options(joinedload("artist")).filter_by(id=artwork_id).first()
                data = artwork_schema.dump(artwork).data
                if not artwork:
                    return {'message': 'Artwork does not exist'}, 400

                return {"status": "success", 'artwork': data}, 200

            # If no arguments passed, return all artworks
            else:
                artworks = Artwork.query.options(joinedload("artist")).all()
                data = ArtworkSchema(many=True).dump(artworks).data
                return {"status": "success", 'artworks': data}, 200

        except OperationalError:
            return {'message': 'Database error'}, 500

    @jwt_required
    def post(self):
        """
        Creates a new artwork
        """

        # Validate input data with load_request
        try:
            artwork_json = load_request(request, ArtworkSchema())
        except IOError as e:
            return {'message': str(e)}, 400
        except ValueError as e:
            return {"message": json.loads(str(e))}, 422

        # Check if there is ID in artist field, since artwork has to have an author,
        # If not and current user is not artist - raise error
        if "artist" not in artwork_json or "id" not in artwork_json["artist"]:
            if current_user.is_admin():
                return {'message': "Artwork has to have an artist"}, 400
            if not current_user.is_artist():
                return {'message': "Only artists can create artworks"}, 401
            else:
                artwork_json["artist"] = {"id": current_user.id}
        # Otherwise, check authorization for create an artwork
        else:
            if (current_user.id != artwork_json["artist"]["id"] or not current_user.is_artist()) \
                    and not current_user.is_admin():
                return {'message': 'Not enough privileges'}, 401

        # Save a new artwork
        try:
            artwork = ArtworkSchema().load(artwork_json).data.save()
        except OperationalError:
            return {'message': 'Database error'}, 500

        storage.create_artwork_folder(artwork.id)

        return {"status": 'success', 'id': artwork.id}, 201

    @jwt_required
    def put(self):
        """
        Edits an artwork
        """

        # Validate input data with load_request
        try:
            artwork_json = load_request(request, ArtworkSchema(), update=True)
        except IOError as e:
            return {'message': str(e)}, 400
        except ValueError as e:
            return {"message": json.loads(str(e))}, 422

        try:
            # Get artwork from db
            artwork_from_db = Artwork.get_by_id(artwork_json['id'])

            # If not exists, raise an error
            if not artwork_from_db:
                return {'message': 'Artwork does not exist'}, 400

            # Check if user authorized to make edits
            if (current_user.id != artwork_from_db.artist.id or not current_user.is_artist()) \
                    and not current_user.is_admin():
                return {'message': 'Not enough privileges'}, 401

            # Save updated in the db
            artwork_from_db.update(**artwork_json)
        except IOError as e:
            return {'message': str(e)}, 400
        except OperationalError:
            return {'message': 'Database error'}, 500

        return {'status': "success"}, 200

    @jwt_required
    def delete(self):
        """
        Deletes an artwork
        """

        # Validate data from the request
        if 'id' not in request.form:
            return {'message': 'No input data provided'}, 400

        artwork_id = request.form['id']

        try:
            # Get artwork from db
            artwork = Artwork.get_by_id(artwork_id)

            # If not exists, raise an error
            if not artwork:
                return {'message': 'Artwork does not exist'}, 400

            # Check if user authorized to delete an artwork
            if current_user.id != artwork.artist.id and not current_user.is_admin():
                return {'message': 'Not enough privileges'}, 401

            # Delete artwork
            artwork.delete()

            # Delete storage
            storage.delete_artwork_folder(artwork.id)

        except OperationalError:
            return {'message': 'Database error'}, 500

        return {'status': "success"}, 200
