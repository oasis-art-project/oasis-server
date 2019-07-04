# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from src.backend.controllers.artworkController import ArtworkResource
from src.backend.controllers.eventController import EventResource
from src.backend.controllers.loginController import LoginResource
from src.backend.controllers.placeController import PlaceResource
from src.backend.controllers.userController import UserResource


def init_router(api):
    """
    Register all router resources
    :param api: api instance passed from extensions.py
    """
    api.add_resource(UserResource, '/user/')
    api.add_resource(UserResource, '/user/<int:user_id>', endpoint='user_id')
    api.add_resource(UserResource, '/user/<string:user_email>', endpoint='user_email')
    api.add_resource(LoginResource, '/login/')
    api.add_resource(ArtworkResource, '/artwork/')
    api.add_resource(ArtworkResource, '/artwork/<int:artwork_id>', endpoint='artwork_id')
    api.add_resource(ArtworkResource, '/artwork/artist/<int:artist_id>', endpoint='artist_id')
    api.add_resource(PlaceResource, '/place/')
    api.add_resource(PlaceResource, '/place/<int:place_id>', endpoint='place_id')
    api.add_resource(PlaceResource, '/place/host/<int:host_id>', endpoint='host_id')
    api.add_resource(EventResource, '/event/')
    api.add_resource(EventResource, '/event/<int:event_id>', endpoint='event_id')
    api.add_resource(EventResource, '/event/place/<int:place_event_id>', endpoint='place_event_id')

