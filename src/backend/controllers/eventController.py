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
from datetime import datetime

from src.backend.controllers.controller import load_request
from src.backend.models.eventModel import EventSchema, Event
from src.backend.models.eventModel import artists_association_table
from src.backend.models.eventModel import artworks_association_table
from src.backend.models.placeModel import Place
from src.backend.models.userModel import User
from src.backend.models.artworkModel import Artwork
from src.backend.extensions import storage

from src.backend.extensions import db

event_schema = EventSchema()


class EventResource(Resource):
    def get(self, event_id=None, event_date=None, place_event_id=None, event_artist_id=None, event_artwork_id=None):
        """
        Gets a list of events
        """
        try:
            # Return all events of place with ID place_event_id
            if place_event_id:
                place_events = Event.query.filter_by(place_id=place_event_id).all()
                return {"status": "success", "events": event_schema.dump(place_events, many=True).data}, 200

             # Return all events involving artist with ID event_artist_id
            if event_artist_id:
                q = Event.query.join(artists_association_table).join(User)
                artist_events = q.filter((artists_association_table.c.artist == event_artist_id)).all()
                return {"status": "success", "events": event_schema.dump(artist_events, many=True).data}, 200

             # Return all events involving artwork with ID event_artwork_id
            if event_artwork_id:
                q = Event.query.join(artworks_association_table).join(Artwork)
                artwork_events = q.filter((artworks_association_table.c.artwork == event_artwork_id)).all()
                return {"status": "success", "events": event_schema.dump(artwork_events, many=True).data}, 200

            # Return current and upcoming events based on date provided in request
            if event_date:
                date0 = datetime.strptime(event_date + "T23:59:59", "%Y-%m-%dT%H:%M:%S")
                date1 = datetime.strptime(event_date + "T00:00:00", "%Y-%m-%dT%H:%M:%S")
                past_events = Event.query.filter(Event.endTime<date1).all()
                current_events = Event.query.filter(Event.startTime<=date0, date1<=Event.endTime).all()
                upcoming_events = Event.query.filter(date0<Event.startTime).all()
                past_data = event_schema.dump(past_events, many=True).data
                current_data = event_schema.dump(current_events, many=True).data
                upcoming_data = event_schema.dump(upcoming_events, many=True).data
                return {"status": "success", "past_events": past_data,
                                             "current_events": current_data,
                                             "upcoming_events": upcoming_data}, 200

            # Return a specific event with ID event_id
            if event_id:
                event = Event.query.options(joinedload("place")).filter_by(id=event_id).first()
                data = event_schema.dump(event).data
                if not event:
                    return {'message': 'Event does not exist'}, 400

                return {"status": "success", 'event': data}, 200

            # If no arguments passed, return all events
            else:
                events = Event.query.options(joinedload("place")).all()
                data = EventSchema(many=True).dump(events).data
                return {"status": "success", 'events': data}, 200

        except OperationalError:
            return {'message': 'Database error'}, 500

    @jwt_required
    def post(self):
        """
        Creates an event
        """

        # Validate input data with load_request
        try:
            event_json = load_request(request, EventSchema())
        except IOError as e:
            return {'message': str(e)}, 400
        except ValueError as e:
            return {'message': json.loads(str(e))}, 422

        # Check if there is ID in place field, since event has to have a place,
        # If not, check authorization for create an event
        if "place" not in event_json and "id" not in event_json["place"]:
            return {'message': "Event has to have a place"}, 400
        elif (current_user.id != Place.get_by_id(event_json['place']['id']).host.id or not current_user.is_host())\
                and not current_user.is_admin():
            return {'message': 'Not enough privileges'}, 401

        # Check if end time of the event is not earlier than start time
        if "endTime" in event_json and event_json["startTime"] > event_json["endTime"]:
            return {'message': "The end date can't be earlier then event starts"}, 400

        # Save a new event
        try:
            event = EventSchema().load(event_json).data.save()
        except OperationalError:
            return {'message': 'Database error'}, 500

        storage.create_event_folder(event.id)

        return {"status": 'success', 'id': event.id}, 201

    @jwt_required
    def put(self):
        """
        Edits an event
        """

        # Validate input data with load_request
        try:
            event_json = load_request(request, EventSchema(), update=True)
        except IOError as e:
            return {'message': str(e)}, 400
        except ValueError as e:
            return {'message': json.loads(str(e))}, 422

        # Check if end time of the event is not earlier than start time
        if "endTime" in event_json and event_json["startTime"] > event_json["endTime"]:
            return {'message': "The end date can't be earlier then event starts"}, 400

        try:
            # Get event from db
            event_from_db = Event.get_by_id(event_json["id"])

            # If not exists, raise an error
            if not event_from_db:
                return {'message': 'Event does not exist'}, 400

            # Check if user authorized to make edits
            if (current_user.id != event_from_db.place.host.id or not current_user.is_host()) \
                    and not current_user.is_admin():
                return {'message': 'Not enough privileges'}, 401

            # Save updated in the db
            EventSchema().load(event_json, partial=True).data.save()
        except IOError as e:
            return {'message': str(e)}, 400
        except OperationalError:
            return {'message': 'Database error'}, 500

        return {'status': "success"}, 200

    @jwt_required
    def delete(self):
        """
        Deletes an event
        """

        # Validate data from the request
        if 'id' not in request.form:
            return {'message': 'No input data provided'}, 400

        event_id = request.form['id']

        try:
            # Get event from db
            event = Event.get_by_id(event_id)

            # If not exists, raise an error
            if not event:
                return {'message': 'Event does not exist'}, 400

            # Check if user authorized to delete an event
            if current_user.id != event.place.host.id and not current_user.is_admin():
                return {'message': 'Not enough privileges'}, 401

            # Delete event
            event.delete()

            # Delete storage
            storage.delete_event_folder(event.id)

        except OperationalError:
            return {'message': 'Database error'}, 500

        return {'status': "success"}, 200