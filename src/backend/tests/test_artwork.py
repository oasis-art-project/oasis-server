# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

import json
import os

import flask

from src.backend.models.artworkModel import Artwork

from src.backend.tests.helpers import \
    params as _params, \
    remove_files as _remove_files, \
    create_user as _create_user, \
    auth_header as _auth_header, \
    create_artwork as _create_artwork, \
    artwork_json as _artwork_json

_url = '/api/artwork/'


class TestArtwork:
    """
    Test CRUD operations edge cases of the Artwork model
    """

    #
    # Get
    #
    def test_get_artwork(self, client):
        artist, _, artist_dump = _create_user(role=3)
        artwork = _create_artwork(artist_dump)

        r = client.get("{}{}".format(_url, artwork.id))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert r.json['artwork']['artist']['firstName'] == artist.firstName
        assert r.json['artwork']['artist']['lastName'] == artist.lastName
        assert r.json['artwork']['name'] == artwork.name
        assert r.json['artwork']['description'] == artwork.description

    def test_get_not_exists_artwork(self, client):
        r = client.get("{}{}".format(_url, 1))

        assert r.status_code == 400
        assert r.json['message'] == "Artwork does not exist"

    def test_get_artworks(self, client):
        artist1, _, artist1_dump = _create_user(role=3,
                                                firstName="artistFirstFirstName",
                                                lastName="artistFirstLastName")
        artist2, _, artist2_dump = _create_user(role=3,
                                                email="bar@foo.com",
                                                firstName="artistSecondFirstName",
                                                lastName="artistSecondLastName")

        artwork1 = _create_artwork(artist1_dump,
                                   name="artwork1Name",
                                   description="artwork1Description")
        artwork2 = _create_artwork(artist2_dump,
                                   name="artwork2Name",
                                   description="artwork2Description")

        r = client.get(_url)

        assert r.status_code == 200

        assert r.json['artworks'][0]['artist']['id']
        assert r.json['artworks'][0]['artist']['firstName'] == artist1.firstName
        assert r.json['artworks'][0]['artist']['lastName'] == artist1.lastName
        assert r.json['artworks'][0]['id'] == artwork1.id
        assert r.json['artworks'][0]['name'] == artwork1.name
        assert r.json['artworks'][0]['description'] == artwork1.description
        assert 'email' not in r.json['artworks'][0]['artist']
        assert 'password' not in r.json['artworks'][0]['artist']
        assert 'token' not in r.json['artworks'][0]['artist']

        assert r.json['artworks'][1]['artist']['id']
        assert r.json['artworks'][1]['artist']['firstName'] == artist2.firstName
        assert r.json['artworks'][1]['artist']['lastName'] == artist2.lastName
        assert r.json['artworks'][1]['id'] == artwork2.id
        assert r.json['artworks'][1]['name'] == artwork2.name
        assert r.json['artworks'][1]['description'] == artwork2.description
        assert 'email' not in r.json['artworks'][1]['artist']
        assert 'password' not in r.json['artworks'][1]['artist']
        assert 'token' not in r.json['artworks'][1]['artist']

    def test_get_artworks_of_specific_artist(self, client):
        artist, _, artist_dump = _create_user(role=3)
        artwork1 = _create_artwork(artist_dump,
                                   name="artwork1Name",
                                   description="artwork1Description")
        artwork2 = _create_artwork(artist_dump,
                                   name="artwork2Name",
                                   description="artwork2Description")

        r = client.get(_url + "artist/{}".format(artist.id))

        assert r.status_code == 200
        assert r.json['artworks'][0]['id'] == artwork1.id
        assert r.json['artworks'][0]['name'] == artwork1.name
        assert r.json['artworks'][0]['description'] == artwork1.description
        assert r.json['artworks'][1]['id'] == artwork2.id
        assert r.json['artworks'][1]['name'] == artwork2.name
        assert r.json['artworks'][1]['description'] == artwork2.description

    #
    # Create
    #
    def test_create_artwork(self, client):
        _, artist_token, artist_dump = _create_user(role=3)

        r = client.post(_url, data=_params(_artwork_json(artist_dump), 2), headers=_auth_header(artist_token))

        assert r.status_code == 201
        assert r.json['status'] == 'success'

    def test_create_artwork_by_admin(self, client):
        _, _, _ = _create_user(role=2)
        _, admin_token, _ = _create_user(email='bar@foo.com', role=1)

        r = client.post(_url, data=_params(_artwork_json({"id": 1}), 2), headers=_auth_header(admin_token))

        assert r.status_code == 201
        assert r.json['status'] == 'success'

    def test_create_artwork_no_input(self, client):
        artist, artist_token, _ = _create_user(role=3)

        r = client.post(_url, data={}, headers=_auth_header(artist_token))

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_create_artwork_no_header(self, client):
        r = client.post(_url, data={})

        assert r.status_code == 401
        assert r.json['msg'] == "Missing Authorization Header"

    def test_create_artwork_miss_input(self, client):
        artist, artist_token, _ = _create_user(role=3)

        r = client.post(_url, data=_params({"foo": "bar"}), headers=_auth_header(artist_token))

        assert r.status_code == 422
        assert r.json['message']['name'] == ["Missing data for required field."]

    def test_create_artwork_without_access(self, client):
        _, not_artist_token, pseudo_artist_dump = _create_user(role=4)

        r = client.post(_url, data=_params(_artwork_json(pseudo_artist_dump), 2),
                        headers=_auth_header(not_artist_token))

        assert r.status_code == 401
        assert r.json['message'] == "Not enough privileges"

    def test_create_artwork_with_fake_artist_input(self, client):
        _, artist_token, artist_dump = _create_user(role=3)

        fake_host = {'firstName': "FakeFirstName", 'lastName': "FakeLastName"}
        artist_dump.update(fake_host)

        r = client.post(_url, data=_params(_artwork_json(artist_dump), 2), headers=_auth_header(artist_token))

        artwork = Artwork.get_by_id(1)

        assert r.status_code == 201
        assert r.json['status'] == 'success'
        assert artwork.artist.firstName != artist_dump['firstName']
        assert artwork.artist.lastName != artist_dump['lastName']

    #
    # Update
    #
    def test_update_artwork(self, client):
        _, artist_token, artist_dump = _create_user(role=3)
        artwork = _create_artwork(artist_dump)

        artwork_dump = {
            'id': artwork.id,
            'name': "updated name",
            'description': "updated description"
        }

        r = client.put(_url, data=_params(artwork_dump, 2), headers=_auth_header(artist_token))

        updated_artwork = Artwork.get_by_id(artwork.id)

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert updated_artwork is not None
        assert updated_artwork.name == artwork_dump['name']
        assert updated_artwork.description == artwork_dump['description']

    def test_update_artwork_no_input(self, client):
        _, token, _ = _create_user()

        r = client.put(_url, data={}, headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_update_artwork_no_header(self, client):
        r = client.put(_url, data={})

        assert r.status_code == 401
        assert r.json['msg'] == "Missing Authorization Header"

    def test_update_artwork_partly_input(self, client):
        _, artist_token, artist_dump = _create_user(role=3)
        artwork = _create_artwork(artist_dump)

        old_description = artwork.description

        artwork_dump = {
            'id': artwork.id,
            'name': "updated name"
        }

        r = client.put(_url, data=_params(artwork_dump), headers=_auth_header(artist_token))

        updated_artwork = Artwork.get_by_id(artwork.id)

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert updated_artwork is not None
        assert updated_artwork.name == artwork_dump['name']
        assert updated_artwork.description == old_description

        artwork_dump2 = {
            'id': artwork.id,
            'description': "updated description"
        }

        r = client.put(_url, data=_params(artwork_dump2), headers=_auth_header(artist_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert updated_artwork is not None
        assert updated_artwork.name == artwork_dump['name']
        assert updated_artwork.description == artwork_dump2['description']

    def test_update_artwork_missing_id(self, client):
        _, artist_token, artist_dump = _create_user(role=3)
        _ = _create_artwork(artist_dump)

        artwork_dump = {
            'name': "updated name",
            'description': "updated description"
        }

        r = client.put(_url, data=_params(artwork_dump, 2), headers=_auth_header(artist_token))

        assert r.status_code == 400
        assert r.json['message'] == 'Id is missing'

    def test_update_artwork_by_admin(self, client):
        _, _, artist_dump = _create_user(role=3)
        artwork = _create_artwork(artist_dump)

        _, admin_token, _ = _create_user(email='bar@foo.com', role=1)

        artwork_dump = {
            'id': artwork.id,
            'name': "updated name",
            'description': "updated description"
        }

        r = client.put(_url, data=_params(artwork_dump, 2), headers=_auth_header(admin_token))

        updated_artwork = Artwork.get_by_id(artwork.id)

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert updated_artwork is not None
        assert updated_artwork.name == artwork_dump['name']
        assert updated_artwork.description == artwork_dump['description']

    def test_update_artwork_not_exists_artwork(self, client):
        _, token, artist_dump = _create_user(role=3)
        _ = _create_artwork(artist_dump)

        artwork_dump = {'id': 2, 'name': 'new name'}

        r = client.put(_url, data=_params(artwork_dump), headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "Artwork does not exist"

    def test_update_artwork_without_access(self, client):
        _, token, pseudo_artist_dump = _create_user(role=4)
        _ = _create_artwork(pseudo_artist_dump)

        artwork_dump = {'id': 1, 'name': 'new name'}

        r = client.put(_url, data=_params(artwork_dump), headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == "Not enough privileges"

        _, _, artist_dump = _create_user(role=3, email="bar@foo.com")
        _ = _create_artwork(artist_dump)

        artist_artwork_dump = {'id': 1, 'name': 'new name'}

        r = client.put(_url, data=_params(artist_artwork_dump), headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == 'Not enough privileges'

    #
    # Delete
    #
    def test_delete_artwork(self, client):
        _, token, artist_dump = _create_user(role=3)
        artwork = _create_artwork(artist_dump)

        r = client.delete(_url, data={'id': artwork.id}, headers=_auth_header(token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'

    def test_delete_artwork_by_admin(self, client):
        _, _, artist_dump = _create_user(role=3)
        artwork = _create_artwork(artist_dump)

        _, admin_token, _ = _create_user(role=1, email='bar@foo.com')

        r = client.delete(_url, data={'id': artwork.id}, headers=_auth_header(admin_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'

    def test_delete_artwork_no_input(self, client):
        _, token, artist_dump = _create_user(role=3)
        _ = _create_artwork(artist_dump)

        r = client.delete(_url, data={}, headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_delete_artwork_no_header(self, client):
        r = client.delete(_url, data={})

        assert r.status_code == 401
        assert r.json['msg'] == "Missing Authorization Header"

    def test_delete_artwork_not_exists_artwork(self, client):
        _, token, artist_dump = _create_user(role=3)
        _ = _create_artwork(artist_dump)

        r = client.delete(_url, data={'id': 2}, headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "Artwork does not exist"

    def test_delete_artwork_without_access(self, client):
        _, token, artist1_dump = _create_user(role=3)
        _, _, artist2_dump = _create_user(email="bar@foo.com", role=3)
        _ = _create_artwork(artist1_dump)
        artwork2 = _create_artwork(artist2_dump)

        r = client.delete(_url, data={'id': artwork2.id}, headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == "Not enough privileges"
