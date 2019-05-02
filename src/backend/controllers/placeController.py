"""
Boston University. Spring 2019
@author: Maxim Tsybanov (oasis@tsybanov.com)
"""

import json

from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import joinedload

from src.backend.controllers.controller import load_request, upload_files, delete_files
from src.backend.models.placeModel import PlaceSchema, Place

place_schema = PlaceSchema()


class PlaceResource(Resource):
    def get(self, place_id=None, host_id=None):
        """
        Gets a list of places
        """
        try:
            # Return all places of host with ID host_id
            if host_id:
                user_places = Place.query.filter_by(host_id=host_id).all()
                return {"status": "success", 'places': place_schema.dump(user_places, many=True).data}, 200

            # Return a specific place with ID place_id
            if place_id:
                place = Place.query.options(joinedload("host")).filter_by(id=place_id).first()

                if not place:
                    return {'message': 'Place does not exist'}, 400

                return {"status": "success", 'place': place_schema.dump(place).data}, 200

            # If no arguments passed, return all artworks
            else:
                places = Place.query.options(joinedload("host")).all()
                return {"status": "success", 'places': PlaceSchema(many=True).dump(places).data}, 200

        except OperationalError:
            return {'message': 'Database error'}, 500

    @jwt_required
    def post(self):
        """
        Creates a place
        """

        # Validate input data with load_request
        try:
            place_json = load_request(request, PlaceSchema())
        except IOError as e:
            return {"message": str(e)}, 400
        except ValueError as e:
            return {"message": json.loads(str(e))}, 422

        # Check if there is ID in host field, since place has to have an owner,
        # If not and current user is not host - raise error
        if "host" not in place_json or "id" not in place_json["host"]:
            if current_user.is_admin():
                return {'message': "Place has to have a host"}, 400
            if not current_user.is_host():
                return {'message': "Only hosts can create places"}, 401
            else:
                place_json["host"] = {"id": current_user.id}
        # Otherwise, check authorization for create a place
        else:
            if (current_user.id != place_json["host"]["id"] or not current_user.is_host()) \
                    and not current_user.is_admin():
                return {'message': 'Not enough privileges'}, 401

        # Process files from the request
        if 'files' in request.files:
                place_json['photo'] = upload_files(request, 10)

        # Save a new place
        try:
            PlaceSchema().load(place_json).data.save()
        except OperationalError:
            return {'message': 'Database error'}, 500

        return {"status": 'success'}, 201

    @jwt_required
    def put(self):
        """
        Edits a place
        """

        # Validate input data with load_request
        try:
            place_json = load_request(request, PlaceSchema(), update=True)
        except IOError as e:
            return {"message": str(e)}, 400
        except ValueError as e:
            return {"message": json.loads(str(e))}, 422

        try:
            # Get place from db
            place_from_db = Place.get_by_id(place_json['id'])

            # If not exists, raise an error
            if not place_from_db:
                return {'message': 'Place does not exist'}, 400

            # Check if user authorized to make edits
            if (current_user.id != place_from_db.host.id or not current_user.is_host()) \
                    and not current_user.is_admin():
                return {'message': 'Not enough privileges'}, 401

            # Process files from the request
            if 'files' in request.files:
                photo_from_db = None
                if place_from_db.photo:
                    photo_from_db = json.loads(place_from_db.photo)
                place_json["photo"] = upload_files(request, 10, photo_from_db)

            # Save updated in the db
            place_from_db.update(**place_json)
        except IOError as e:
            return {'message': str(e)}, 400
        except OperationalError:
            return {'message': 'Database error'}, 500

        return {'status': "success"}, 200

    @jwt_required
    def delete(self):
        """
        Deletes a place
        """

        # Validate data from the request
        if 'id' not in request.form:
            return {'message': 'No input data provided'}, 400

        place_id = request.form['id']

        try:
            # Get place from db
            place = Place.get_by_id(place_id)

            # If not exists, raise an error
            if not place:
                return {'message': 'Place does not exist'}, 400

            # Check if user authorized to delete a place
            if current_user.id != place.host.id and not current_user.is_admin():
                return {'message': 'Not enough privileges'}, 401

            # If photo in the request, means just delete a specific photo instead of the whole place
            if 'photo' in request.form:
                photo = request.form['photo']
                if photo not in place.photo:
                    return {'message': '{} does not have {} picture'}, 400

                # Delete file from the disk
                delete_files([photo])
                return {'status': "success"}, 200

            # Delete artwork
            place.delete()

            # Delete all files from the disk after deleting of a place
            if place.photo:
                delete_files(json.loads(place.photo))

        except OperationalError:
            return {'message': 'Database error'}, 500

        return {'status': "success"}, 200