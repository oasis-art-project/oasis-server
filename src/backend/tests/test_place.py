"""
Boston University. Spring 2019
@author: Maxim Tsybanov (oasis@tsybanov.com)
"""

import json
import os

import flask

from src.backend.models.placeModel import Place
from src.backend.tests.helpers import \
    params as _params, \
    remove_files as _remove_files, \
    create_user as _create_user, \
    auth_header as _auth_header, \
    create_place as _create_place, \
    place_json as _place_json

_url = '/api/place'


class TestPlace:
    """
    Test CRUD operations edge cases of the Place model
    """

    #
    # Get
    #
    def test_get_place(self, client):
        host, _, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        r = client.get("{}/{}".format(_url, place.id))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert r.json['place']['host']['firstName'] == host.firstName
        assert r.json['place']['host']['lastName'] == host.lastName
        assert r.json['place']['host']['avatar'] == host.avatar
        assert r.json['place']['name'] == place.name
        assert r.json['place']['description'] == place.description
        assert r.json['place']['address'] == place.address
        assert r.json['place']['photo'] == place.photo

    def test_get_not_exists_place(self, client):
        r = client.get("{}/{}".format(_url, 1))

        assert r.status_code == 400
        assert r.json['message'] == "Place does not exist"

    def test_get_places(self, client):
        host1, _, host1_dump = _create_user(role=2,
                                            firstName="hostFirstFirstName",
                                            lastName="hostFirstLastName",
                                            avatar="hostFirstAvatar")
        host2, _, host2_dump = _create_user(role=2,
                                            email="bar@foo.com",
                                            firstName="hostSecondFirstName",
                                            lastName="hostSecondLastName",
                                            avatar="hostSecondAvatar")

        place1 = _create_place(host1_dump,
                               name="place1Name",
                               description="place1Description",
                               address="place1Address",
                               photo="place1photo.jpg")
        place2 = _create_place(host2_dump,
                               name="place2Name",
                               description="place2Description",
                               address="place2Address",
                               photo="place2photo.jpg")

        r = client.get(_url)

        assert r.status_code == 200

        assert r.json['places'][0]['host']['id']
        assert r.json['places'][0]['host']['firstName'] == host1.firstName
        assert r.json['places'][0]['host']['lastName'] == host1.lastName
        assert r.json['places'][0]['host']['avatar'] == host1.avatar
        assert r.json['places'][0]['id'] == place1.id
        assert r.json['places'][0]['name'] == place1.name
        assert r.json['places'][0]['description'] == place1.description
        assert r.json['places'][0]['address'] == place1.address
        assert r.json['places'][0]['photo'] == place1.photo
        assert 'email' not in r.json['places'][0]['host']
        assert 'password' not in r.json['places'][0]['host']
        assert 'token' not in r.json['places'][0]['host']

        assert r.json['places'][1]['host']['id']
        assert r.json['places'][1]['host']['firstName'] == host2.firstName
        assert r.json['places'][1]['host']['lastName'] == host2.lastName
        assert r.json['places'][1]['host']['avatar'] == host2.avatar
        assert r.json['places'][1]['id'] == place2.id
        assert r.json['places'][1]['name'] == place2.name
        assert r.json['places'][1]['description'] == place2.description
        assert r.json['places'][1]['address'] == place2.address
        assert r.json['places'][1]['photo'] == place2.photo
        assert 'email' not in r.json['places'][1]['host']
        assert 'password' not in r.json['places'][1]['host']
        assert 'token' not in r.json['places'][1]['host']

    def test_get_places_of_specific_host(self, client):
        host, _, host_dump = _create_user(role=2)
        place1 = _create_place(host_dump,
                               name="place1Name",
                               description="place1Description",
                               address="place1Address",
                               photo="place1photo.jpg")
        place2 = _create_place(host_dump,
                               name="place2Name",
                               description="place2Description",
                               address="place2Address",
                               photo="place2photo.jpg")

        r = client.get(_url + "/host/{}".format(host.id))

        assert r.status_code == 200
        assert r.json['places'][0]['id'] == place1.id
        assert r.json['places'][0]['name'] == place1.name
        assert r.json['places'][0]['description'] == place1.description
        assert r.json['places'][0]['address'] == place1.address
        assert r.json['places'][0]['photo'] == place1.photo
        assert r.json['places'][1]['id'] == place2.id
        assert r.json['places'][1]['name'] == place2.name
        assert r.json['places'][1]['description'] == place2.description
        assert r.json['places'][1]['address'] == place2.address
        assert r.json['places'][1]['photo'] == place2.photo

    #
    # Create
    #
    def test_create_place(self, client):
        _, host_token, host_dump = _create_user(role=2)

        r = client.post(_url, data=_params(_place_json(host_dump), 2), headers=_auth_header(host_token))

        assert r.status_code == 201
        assert r.json['status'] == 'success'

        _remove_files(json.loads(Place.get_by_id(1).photo))

    def test_create_place_by_admin(self, client):
        _, _, _ = _create_user(role=2)
        _, admin_token, _ = _create_user(email='bar@foo.com', role=1)

        r = client.post(_url, data=_params(_place_json({"id": 1}), 2), headers=_auth_header(admin_token))
        # TODO: !!! check in db if code 200 or 201 everywhere. Like in updated
        assert r.status_code == 201
        assert r.json['status'] == 'success'

        _remove_files(json.loads(Place.get_by_id(1).photo))

    def test_create_place_no_input(self, client):
        host, host_token, _ = _create_user(role=2)

        r = client.post(_url, data={}, headers=_auth_header(host_token))

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_create_place_miss_input(self, client):
        host, host_token, _ = _create_user(role=2)

        r = client.post(_url, data=_params({"foo": "bar"}), headers=_auth_header(host_token))
        assert r.status_code == 422
        assert r.json['message']['name'] == ["Missing data for required field."]
        assert r.json['message']['address'] == ["Missing data for required field."]
        assert r.json['message']['host'] == ["Missing data for required field."]

    def test_create_place_without_access(self, client):
        _, not_host_token, pseudo_host_dump = _create_user(role=4)

        r = client.post(_url, data=_params(_place_json(pseudo_host_dump), 2), headers=_auth_header(not_host_token))

        assert r.status_code == 401
        assert r.json['message'] == "Not enough privileges"

    def test_create_place_no_header(self, client):
        r = client.put(_url, data={})

        assert r.status_code == 401
        assert r.json['msg'] == "Missing Authorization Header"

    def test_create_place_photos_created(self, client):
        _, host_token, host_dump = _create_user(role=2)

        r = client.post(_url, data=_params(_place_json(host_dump), 2), headers=_auth_header(host_token))

        assert r.status_code == 201
        assert r.json['status'] == 'success'

        file_path = os.path.join(flask.current_app.root_path, flask.current_app.config['UPLOAD_FOLDER'])

        photo = json.loads(Place.get_by_id(1).photo)

        assert os.path.isfile(os.path.join(file_path, photo[0]))
        assert os.path.isfile(os.path.join(file_path, photo[1]))

        _remove_files(photo)

    def test_create_place_with_fake_host_input(self, client):
        _, host_token, host_dump = _create_user(role=2)

        fake_host = {'firstName': "FakeFirstName", 'lastName': "FakeLastName"}
        host_dump.update(fake_host)

        r = client.post(_url, data=_params(_place_json(host_dump), 2), headers=_auth_header(host_token))

        place = Place.get_by_id(1)

        assert r.status_code == 201
        assert r.json['status'] == 'success'
        assert place.host.firstName != host_dump['firstName']
        assert place.host.lastName != host_dump['lastName']

        _remove_files(json.loads(Place.get_by_id(1).photo))

    #
    # Update
    #
    def test_update_place(self, client):
        _, host_token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        place_dump = {
            'id': place.id,
            'name': "updated name",
            'description': "updated description",
            'address': "updated address"
        }

        r = client.put(_url, data=_params(place_dump, 2), headers=_auth_header(host_token))

        updated_place = Place.get_by_id(place.id)

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert updated_place is not None
        assert updated_place.name == place_dump['name']
        assert updated_place.description == place_dump['description']
        assert updated_place.address == place_dump['address']

        _remove_files(json.loads(updated_place.photo))

    def test_update_place_no_input(self, client):
        _, token, _ = _create_user()

        r = client.put(_url, data={}, headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_update_place_no_header(self, client):
        r = client.put(_url, data={})

        assert r.status_code == 401
        assert r.json['msg'] == "Missing Authorization Header"

    def test_update_place_partly_input(self, client):
        _, host_token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        old_description = place.description
        old_address = place.address

        place_dump = {
            'id': place.id,
            'name': "updated name"
        }

        r = client.put(_url, data=_params(place_dump), headers=_auth_header(host_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert place.name == place_dump['name']
        assert place.description == old_description
        assert place.address == old_address

        place_dump2 = {
            'id': place.id,
            'description': 'updated description'
        }

        r = client.put(_url, data=_params(place_dump2), headers=_auth_header(host_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert place.name == place_dump['name']
        assert place.description == place_dump2['description']
        assert place.address == old_address

    def test_update_place_missing_id(self, client):
        _, host_token, host_dump = _create_user(role=2)
        _ = _create_place(host_dump)

        place_dump = {
            'name': "updated name",
            'description': "updated description",
            'address': "updated address"
        }

        r = client.put(_url, data=_params(place_dump, 2), headers=_auth_header(host_token))

        assert r.status_code == 400
        assert r.json['message'] == 'Id is missing'

    def test_update_place_by_admin(self, client):
        _, _, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        _, admin_token, _ = _create_user(email='bar@foo.com', role=1)

        place_dump = {
            'id': place.id,
            'name': "updated name",
            'description': "updated description",
            'address': "updated address"
        }

        r = client.put(_url, data=_params(place_dump, 2), headers=_auth_header(admin_token))

        updated_place = Place.get_by_id(place.id)

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert updated_place is not None
        assert updated_place.name == place_dump['name']
        assert updated_place.description == place_dump['description']
        assert updated_place.address == place_dump['address']

        _remove_files(json.loads(updated_place.photo))

    def test_update_place_not_exists_place(self, client):
        host, token, host_dump = _create_user(role=2)
        _ = _create_place(host_dump)

        place_dump = {'id': 2, 'name': "new name"}

        r = client.put(_url, data=_params(place_dump, 2), headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "Place does not exist"

    def test_update_place_without_access(self, client):
        _, token, pseudo_host_dump = _create_user(role=4)
        _ = _create_place(pseudo_host_dump)

        place_dump = {'id': 1, 'name': 'new name'}

        r = client.put(_url, data=_params(place_dump, 2), headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == "Not enough privileges"

        _, _, host_dump = _create_user(role=2, email="bar@foo.com")
        _ = _create_place(host_dump)

        host_place_dump = {'id': 1, 'name': 'new name'}

        r = client.put(_url, data=_params(host_place_dump, 2), headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == 'Not enough privileges'

    def test_update_place_photos_updated(self, client):
        _, host_token, host_dump = _create_user(role=2)

        client.post(_url, data=_params(_place_json(host_dump), 2), headers=_auth_header(host_token))

        r = client.put(_url, data=_params({"id": 1}, 2), headers=_auth_header(host_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'

        file_path = os.path.join(flask.current_app.root_path, flask.current_app.config['UPLOAD_FOLDER'])

        photo = json.loads(Place.get_by_id(1).photo)

        assert os.path.isfile(os.path.join(file_path, photo[0]))
        assert os.path.isfile(os.path.join(file_path, photo[1]))
        assert os.path.isfile(os.path.join(file_path, photo[2]))
        assert os.path.isfile(os.path.join(file_path, photo[3]))

        _remove_files(photo)

    def test_update_place_photos_maximum_reached(self, client):
        _, host_token, host_dump = _create_user(role=2)

        client.post(_url, data=_params(_place_json(host_dump), 2), headers=_auth_header(host_token))

        client.put(_url, data=_params({"id": 1}, 2), headers=_auth_header(host_token))
        client.put(_url, data=_params({"id": 1}, 2), headers=_auth_header(host_token))
        client.put(_url, data=_params({"id": 1}, 2), headers=_auth_header(host_token))
        client.put(_url, data=_params({"id": 1}, 2), headers=_auth_header(host_token))
        r = client.put(_url, data=_params({"id": 1}, 2), headers=_auth_header(host_token))

        assert r.status_code == 400
        assert r.json['message'][:33] == 'Total number of files can be only'

        photo = json.loads(Place.get_by_id(1).photo)

        _remove_files(photo)

    #
    # Delete
    #
    def test_delete_place(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        r = client.delete(_url, data={'id': place.id}, headers=_auth_header(token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'

    def test_delete_place_by_admin(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        _, admin_token, _ = _create_user(role=1, email='bar@foo.com')

        r = client.delete(_url, data={'id': place.id}, headers=_auth_header(admin_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'

    def test_delete_place_no_input(self, client):
        _, token, host_dump = _create_user(role=2)
        _ = _create_place(host_dump)

        r = client.delete(_url, data={}, headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_delete_place_no_header(self, client):
        r = client.delete(_url, data={})

        assert r.status_code == 401
        assert r.json['msg'] == "Missing Authorization Header"

    def test_delete_place_not_exists_place(self, client):
        _, token, host_dump = _create_user(role=2)
        _ = _create_place(host_dump)

        r = client.delete(_url, data={'id': 2}, headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "Place does not exist"

    def test_delete_place_without_access(self, client):
        _, token, host1_dump = _create_user(role=2)
        _, _, host2_dump = _create_user(email="bar@foo.com", role=2)
        _ = _create_place(host1_dump)
        place2 = _create_place(host2_dump)

        r = client.delete(_url, data={'id': place2.id}, headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == "Not enough privileges"

    def test_delete_place_specific_photo(self, client):
        _, host_token, host_dump = _create_user(role=2)

        client.post(_url, data=_params(_place_json(host_dump), 2), headers=_auth_header(host_token))

        photo = json.loads(Place.get_by_id(1).photo)

        r1 = client.delete(_url, data={'id': 1, 'photo': photo[0]}, headers=_auth_header(host_token))
        r2 = client.delete(_url, data={'id': 1, 'photo': photo[1]}, headers=_auth_header(host_token))

        assert r1.status_code == 200
        assert r1.json['status'] == 'success'
        assert r2.status_code == 200
        assert r2.json['status'] == 'success'

        file_path = os.path.join(flask.current_app.root_path, flask.current_app.config['UPLOAD_FOLDER'])

        assert not os.path.isfile(os.path.join(file_path, photo[0]))
        assert not os.path.isfile(os.path.join(file_path, photo[1]))

    def test_delete_place_all_photos(self, client):
        _, host_token, host_dump = _create_user(role=2)

        client.post(_url, data=_params(_place_json(host_dump), 2), headers=_auth_header(host_token))
        photo = json.loads(Place.get_by_id(1).photo)

        r = client.delete(_url, data={'id': 1}, headers=_auth_header(host_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'

        file_path = os.path.join(flask.current_app.root_path, flask.current_app.config['UPLOAD_FOLDER'])

        assert not os.path.isfile(os.path.join(file_path, photo[0]))
        assert not os.path.isfile(os.path.join(file_path, photo[1]))
