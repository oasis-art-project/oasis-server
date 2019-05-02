"""
Boston University. Spring 2019
@author: Maxim Tsybanov (oasis@tsybanov.com)
"""

import json
import os
from datetime import datetime

import flask

from src.backend.models.eventModel import Event
from src.backend.tests.helpers import \
    params as _params, \
    remove_files as _remove_files, \
    create_user as _create_user, \
    auth_header as _auth_header, \
    create_event as _create_event, \
    event_json as _event_json, \
    create_place as _create_place

_url = '/api/event/'


class TestEvent:
    """
    Test CRUD operations edge cases of the Event model
    """

    #
    # Get
    #
    def test_get_event(self, client):
        _, _, host_dump = _create_user(role=2)
        place = _create_place(host_dump)
        artist1, _, artist1_dump = _create_user(email='bar@foo.com')
        artist2, _, artist2_dump = _create_user(email='bar2@foo.com')
        event = _create_event({"id": place.id}, [{"id": 2}, {"id": 3}])

        r = client.get("{}{}".format(_url, event.id))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert r.json['event']['place']['name'] == place.name
        assert r.json['event']['place']['description'] == place.description
        assert r.json['event']['place']['address'] == place.address
        assert r.json['event']['place']['photo'] == place.photo
        assert r.json['event']['artists'][0]['firstName'] == artist1.firstName
        assert r.json['event']['artists'][0]['lastName'] == artist1.lastName
        assert r.json['event']['artists'][1]['firstName'] == artist2.firstName
        assert r.json['event']['artists'][1]['lastName'] == artist2.lastName
        assert r.json['event']['name'] == event.name
        assert r.json['event']['description'] == event.description
        assert datetime.strptime(r.json['event']['startTime'], '%Y-%m-%dT%H:%M:%S%z').replace(
            tzinfo=None) == event.startTime
        assert datetime.strptime(r.json['event']['endTime'], '%Y-%m-%dT%H:%M:%S%z').replace(
            tzinfo=None) == event.endTime
        assert r.json['event']['photo'] == event.photo

    def test_get_not_exists_event(self, client):
        r = client.get("{}{}".format(_url, 1))

        assert r.status_code == 400
        assert r.json['message'] == "Event does not exist"

    def test_get_events(self, client):
        _, _, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        artist1, _, artist1_dump = _create_user(email='bar@foo.com')
        artist2, _, artist2_dump = _create_user(email='bar2@foo.com')

        event1 = _create_event({"id": place.id},
                               [{"id": 2}, {"id": 3}],
                               name="event1Name",
                               description="event1Description",
                               startTime="2019-02-02T10:00:00",
                               endTime="2019-03-01T15:00:00",
                               photo="event1photo.jpg")
        event2 = _create_event({"id": place.id},
                               [{"id": 2}, {"id": 3}],
                               name="event2Name",
                               description="event2Description",
                               startTime="2019-02-05T12:00:00",
                               endTime="2019-04-01T18:00:00",
                               photo="event2photo.jpg")

        r = client.get(_url)

        assert r.status_code == 200

        assert r.json['events'][0]['place']['id']
        assert r.json['events'][0]['place']['name'] == place.name
        assert r.json['events'][0]['place']['description'] == place.description
        assert r.json['events'][0]['place']['address'] == place.address
        assert r.json['events'][0]['place']['photo'] == place.photo
        assert r.json['events'][0]['artists'][0]['firstName'] == artist1.firstName
        assert r.json['events'][0]['artists'][0]['lastName'] == artist1.lastName
        assert r.json['events'][0]['artists'][1]['firstName'] == artist2.firstName
        assert r.json['events'][0]['artists'][1]['lastName'] == artist2.lastName
        assert r.json['events'][0]['id'] == event1.id
        assert r.json['events'][0]['name'] == event1.name
        assert r.json['events'][0]['description'] == event1.description
        assert r.json['events'][0]['photo'] == event1.photo
        assert datetime.strptime(r.json['events'][0]['startTime'], '%Y-%m-%dT%H:%M:%S%z').replace(
            tzinfo=None) == event1.startTime
        assert datetime.strptime(r.json['events'][0]['endTime'], '%Y-%m-%dT%H:%M:%S%z').replace(
            tzinfo=None) == event1.endTime
        assert r.json['events'][0]['photo'] == event1.photo

        assert r.json['events'][1]['place']['id']
        assert r.json['events'][1]['place']['name'] == place.name
        assert r.json['events'][1]['place']['description'] == place.description
        assert r.json['events'][1]['place']['address'] == place.address
        assert r.json['events'][1]['place']['photo'] == place.photo
        assert r.json['events'][1]['artists'][0]['firstName'] == artist1.firstName
        assert r.json['events'][1]['artists'][0]['lastName'] == artist1.lastName
        assert r.json['events'][1]['artists'][1]['firstName'] == artist2.firstName
        assert r.json['events'][1]['artists'][1]['lastName'] == artist2.lastName
        assert r.json['events'][1]['id'] == event2.id
        assert r.json['events'][1]['name'] == event2.name
        assert r.json['events'][1]['description'] == event2.description
        assert r.json['events'][1]['photo'] == event2.photo
        assert datetime.strptime(r.json['events'][1]['startTime'], '%Y-%m-%dT%H:%M:%S%z').replace(
            tzinfo=None) == event2.startTime
        assert datetime.strptime(r.json['events'][1]['endTime'], '%Y-%m-%dT%H:%M:%S%z').replace(
            tzinfo=None) == event2.endTime
        assert r.json['events'][1]['photo'] == event2.photo

    def test_get_events_of_specific_place(self, client):
        _, _, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        artist1, _, artist1_dump = _create_user(email='bar@foo.com')
        artist2, _, artist2_dump = _create_user(email='bar2@foo.com')

        event1 = _create_event({"id": place.id},
                               [{"id": 2}, {"id": 3}],
                               name="event1Name",
                               description="event1Description",
                               startTime="2019-02-02T10:00:00",
                               endTime="2019-03-01T15:00:00",
                               photo="event1photo.jpg")
        event2 = _create_event({"id": place.id},
                               [{"id": 2}, {"id": 3}],
                               name="event2Name",
                               description="event2Description",
                               startTime="2019-02-05T12:00:00",
                               endTime="2019-04-01T18:00:00",
                               photo="event2photo.jpg")

        r = client.get(_url + "place/{}".format(place.id))

        assert r.status_code == 200
        assert r.json['events'][0]['id'] == event1.id
        assert r.json['events'][0]['name'] == event1.name
        assert r.json['events'][0]['description'] == event1.description
        assert datetime.strptime(r.json['events'][0]['startTime'], '%Y-%m-%dT%H:%M:%S%z').replace(
            tzinfo=None) == event1.startTime
        assert datetime.strptime(r.json['events'][0]['endTime'], '%Y-%m-%dT%H:%M:%S%z').replace(
            tzinfo=None) == event1.endTime
        assert r.json['events'][0]['photo'] == event1.photo
        assert r.json['events'][0]['artists'][0]['firstName'] == artist1.firstName
        assert r.json['events'][0]['artists'][0]['lastName'] == artist1.lastName
        assert r.json['events'][0]['artists'][1]['firstName'] == artist2.firstName
        assert r.json['events'][0]['artists'][1]['lastName'] == artist2.lastName

        assert r.json['events'][1]['id'] == event2.id
        assert r.json['events'][1]['name'] == event2.name
        assert r.json['events'][1]['description'] == event2.description
        assert datetime.strptime(r.json['events'][1]['startTime'], '%Y-%m-%dT%H:%M:%S%z').replace(
            tzinfo=None) == event2.startTime
        assert datetime.strptime(r.json['events'][1]['endTime'], '%Y-%m-%dT%H:%M:%S%z').replace(
            tzinfo=None) == event2.endTime
        assert r.json['events'][1]['photo'] == event2.photo
        assert r.json['events'][1]['artists'][0]['firstName'] == artist1.firstName
        assert r.json['events'][1]['artists'][0]['lastName'] == artist1.lastName
        assert r.json['events'][1]['artists'][1]['firstName'] == artist2.firstName
        assert r.json['events'][1]['artists'][1]['lastName'] == artist2.lastName

    #
    # Create
    #
    def test_create_event(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        _, _, artist1_dump = _create_user(email='bar@foo.com')
        _, _, artist2_dump = _create_user(email='bar2@foo.com')

        r = client.post(_url,
                        data=_params(_event_json({"id": place.id}, [{"id": 2}, {"id": 3}]), 2),
                        headers=_auth_header(token))

        assert r.status_code == 201
        assert r.json['status'] == 'success'

        _remove_files(json.loads(Event.get_by_id(1).photo))

    def test_create_event_by_admin(self, client):
        _, _, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        _, _, artist1_dump = _create_user(email='bar@foo.com')
        _, _, artist2_dump = _create_user(email='bar2@foo.com')

        _, admin_token, _ = _create_user(email='bar3@foo.com', role=1)

        r = client.post(_url, data=_params(_event_json({"id": place.id}, [{"id": 2}, {"id": 3}]), 2),
                        headers=_auth_header(admin_token))

        assert r.status_code == 201
        assert r.json['status'] == 'success'

        _remove_files(json.loads(Event.get_by_id(1).photo))

    def test_create_event_no_input(self, client):
        host, token, _ = _create_user(role=2)

        r = client.post(_url, data={}, headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_create_event_no_header(self, client):
        r = client.put(_url, data={})

        assert r.status_code == 401
        assert r.json['msg'] == "Missing Authorization Header"

    def test_create_event_miss_input(self, client):
        _, token, host_dump = _create_user(role=2)
        _ = _create_place(host_dump)

        r = client.post(_url, data=_params({"foo": "bar"}), headers=_auth_header(token))

        assert r.status_code == 422
        assert r.json['message']['name'] == ["Missing data for required field."]
        assert r.json['message']['startTime'] == ["Missing data for required field."]
        assert r.json['message']['place'] == ["Missing data for required field."]

    def test_create_event_end_time_earlier_than_start_time(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)
        event_dump = {
            "place": {"id": place.id},
            "name": "event1Name",
            "startTime": "2020-01-01T20:00:00",
            "endTime": "2019-01-01T20:00:00"
        }

        r = client.post(_url, data=_params(event_dump), headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "The end date can't be earlier then event starts"

    def test_create_event_without_end_time(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        event_json = _event_json({"id": place.id})
        del event_json['endTime']

        r = client.post(_url, data=_params(event_json, 2), headers=_auth_header(token))

        event = Event.get_by_id(1)

        assert r.status_code == 201
        assert r.json['status'] == 'success'
        assert event.startTime == datetime.strptime(event_json['startTime'], '%Y-%m-%dT%H:%M:%S')
        assert not event.endTime

        _remove_files(json.loads(event.photo))

    def test_create_event_wrong_format_time(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        event_json = _event_json({"id": place.id})
        event_json['startTime'] = "2018"
        event_json['endTime'] = "20189"

        r = client.post(_url, data=_params(event_json), headers=_auth_header(token))

        assert r.status_code == 422
        assert r.json['message']['startTime'] == ['Not a valid datetime.']
        assert r.json['message']['endTime'] == ['Not a valid datetime.']

    def test_create_event_without_access(self, client):
        _, token, pseudo_host_dump = _create_user(role=4)
        pseudo_place = _create_place(pseudo_host_dump)

        r = client.post(_url, data=_params(_event_json({"id": pseudo_place.id})), headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == "Not enough privileges"

    def test_create_event_photos_created(self, client):
        _, host_token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        r = client.post(_url, data=_params(_event_json({"id": place.id}), 2), headers=_auth_header(host_token))

        assert r.status_code == 201
        assert r.json['status'] == 'success'

        file_path = os.path.join(flask.current_app.root_path, flask.current_app.config['UPLOAD_FOLDER'])

        photo = json.loads(Event.get_by_id(1).photo)

        assert os.path.isfile(os.path.join(file_path, photo[0]))
        assert os.path.isfile(os.path.join(file_path, photo[1]))

        _remove_files(photo)

    def test_create_event_with_fake_host_input(self, client):
        _, host_token, host_dump = _create_user(role=2)
        _ = _create_place(host_dump)

        fake_host = {'firstName': "FakeFirstName", 'lastName': "FakeLastName"}
        host_dump.update(fake_host)

        r = client.post(_url, data=_params(_event_json(host_dump), 2), headers=_auth_header(host_token))

        event = Event.get_by_id(1)

        assert r.status_code == 201
        assert r.json['status'] == 'success'
        assert event.place.host.firstName != host_dump['firstName']
        assert event.place.host.lastName != host_dump['lastName']

        _remove_files(json.loads(Event.get_by_id(1).photo))

    #
    # Update
    #
    def test_update_event(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        artist1, _, artist1_dump = _create_user(email='bar@foo.com')
        artist2, _, artist2_dump = _create_user(email='bar2@foo.com',
                                                firstName='artistSecondFirstName',
                                                lastName='artistSecondLastName')

        event = _create_event({"id": place.id}, [{"id": 2}])

        event_dump = {
            'id': event.id,
            'artists': [artist2_dump],
            'name': "updated name",
            'description': "updated description",
            'startTime': "2020-01-01T05:00:00",
            'endTime': "2020-01-03T08:00:00"
        }

        r = client.put(_url, data=_params(event_dump, 2), headers=_auth_header(token))

        updated_event = Event.get_by_id(event.id)

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert updated_event is not None
        assert updated_event.name == event_dump['name']
        assert updated_event.description == event_dump['description']
        assert updated_event.startTime == datetime.strptime(event_dump['startTime'],
                                                            '%Y-%m-%dT%H:%M:%S').replace(tzinfo=None)
        assert updated_event.endTime == datetime.strptime(event_dump['endTime'],
                                                          '%Y-%m-%dT%H:%M:%S').replace(tzinfo=None)
        assert updated_event.artists[0].id == artist2_dump['id']
        assert updated_event.artists[0].firstName == artist2_dump['firstName']
        assert updated_event.artists[0].lastName == artist2_dump['lastName']

        _remove_files(json.loads(updated_event.photo))

    def test_update_event_no_input(self, client):
        _, token, _ = _create_user()

        r = client.put(_url, data={}, headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_update_event_no_header(self, client):
        r = client.put(_url, data={})

        assert r.status_code == 401
        assert r.json['msg'] == "Missing Authorization Header"

    def test_update_event_partly_input(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)
        event = _create_event({"id": place.id})

        old_description = event.description
        old_start_time = event.startTime

        event_dump = {
            'id': event.id,
            'name': "updated name"
        }

        r = client.put(_url, data=_params(event_dump, 2), headers=_auth_header(token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert event.name == event_dump['name']
        assert event.description == old_description
        assert event.startTime == old_start_time

        event_dump2 = {
            'id': place.id,
            'startTime': '2018-01-01T05:00:00'
        }

        r = client.put(_url, data=_params(event_dump2), headers=_auth_header(token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert event.name == event_dump['name']
        assert event.description == old_description
        assert event.startTime == datetime.strptime(event_dump2['startTime'],
                                                    '%Y-%m-%dT%H:%M:%S').replace(tzinfo=None)

        _remove_files(json.loads(event.photo))

    def test_update_event_missing_id(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)
        _ = _create_event({"id": place.id})

        event_dump = {
            'name': "updated name",
            'description': "updated description",
            'startTime': "2020-01-01T05:00:00",
            'endTime': "2020-01-03T08:00:00"
        }

        r = client.put(_url, data=_params(event_dump), headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == 'Id is missing'

    def test_update_event_by_admin(self, client):
        _, _, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        artist1, _, artist1_dump = _create_user(email='bar@foo.com')
        artist2, _, artist2_dump = _create_user(email='bar2@foo.com',
                                                firstName='artistSecondFirstName',
                                                lastName='artistSecondLastName')

        event = _create_event({"id": place.id}, [{"id": 2}])

        _, admin_token, _ = _create_user(email='bar3@foo.com', role=1)

        event_dump = {
            'id': event.id,
            'artists': [artist2_dump],
            'name': "updated name",
            'description': "updated description",
            'startTime': "2020-01-01T05:00:00",
            'endTime': "2020-01-03T08:00:00"
        }

        r = client.put(_url, data=_params(event_dump, 2), headers=_auth_header(admin_token))

        updated_event = Event.get_by_id(event.id)

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert updated_event is not None
        assert updated_event.place == place
        assert updated_event.name == event_dump['name']
        assert updated_event.description == event_dump['description']
        assert updated_event.startTime == datetime.strptime(event_dump['startTime'],
                                                            '%Y-%m-%dT%H:%M:%S').replace(tzinfo=None)
        assert updated_event.endTime == datetime.strptime(event_dump['endTime'],
                                                          '%Y-%m-%dT%H:%M:%S').replace(tzinfo=None)

        assert updated_event.artists[0].id == artist2_dump['id']
        assert updated_event.artists[0].firstName == artist2_dump['firstName']
        assert updated_event.artists[0].lastName == artist2_dump['lastName']

        _remove_files(json.loads(updated_event.photo))

    def test_update_event_end_date_earlier(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)
        _ = _create_event({"id": place.id})

        event_dump = {
            "place": {"id": place.id},
            "name": "new event",
            'startTime': "2020-01-01T20:00:00",
            'endTime': "2019-01-01T20:00:00"
        }

        r = client.post(_url, data=_params(event_dump), headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "The end date can't be earlier then event starts"

    def test_update_event_without_end_time(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)
        _ = _create_event({"id": place.id})

        event_dump = {
            "id": 1,
            'startTime': "2018-01-01T20:00:00"
        }

        event = Event.get_by_id(1)

        r = client.put(_url, data=_params(event_dump), headers=_auth_header(token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert event.startTime == datetime.strptime(event_dump['startTime'], '%Y-%m-%dT%H:%M:%S')

    def test_update_event_wrong_format_time(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)
        _ = _create_event({"id": place.id})

        event_dump = {
            "id": 1,
            'startTime': "2018",
            'endTime': '2019'
        }

        r = client.put(_url, data=_params(event_dump), headers=_auth_header(token))

        assert r.status_code == 422
        assert r.json['message']['startTime'] == ['Not a valid datetime.']
        assert r.json['message']['endTime'] == ['Not a valid datetime.']

    def test_update_event_not_exists_event(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)
        _ = _create_event({"id": place.id})

        event_dump = {
            'id': 2,
            'name': "new name"
        }

        r = client.put(_url, data=_params(event_dump), headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "Event does not exist"

    def test_update_event_without_access(self, client):
        _, token, pseudo_host_dump = _create_user(role=4)
        pseudo_place = _create_place(pseudo_host_dump)
        event = _create_event({"id": pseudo_place.id})

        event_dump = {
            'id': event.id,
            'name': "new name"
        }

        r = client.put(_url, data=_params(event_dump), headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == "Not enough privileges"

        _, _, host_dump = _create_user(role=2, email="bar@foo.com")
        place = _create_place(host_dump)
        event2 = _create_event({"id": place.id})

        place_event_dump = {
            'id': event2.id,
            'name': "new name"
        }

        r = client.put(_url, data=_params(place_event_dump), headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == 'Not enough privileges'

    def test_update_event_photos_updated(self, client):
        _, host_token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        client.post(_url, data=_params(_event_json({"id": place.id}), 2), headers=_auth_header(host_token))

        r = client.put(_url, data=_params({"id": 1}, 2), headers=_auth_header(host_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'

        file_path = os.path.join(flask.current_app.root_path, flask.current_app.config['UPLOAD_FOLDER'])

        photo = json.loads(Event.get_by_id(1).photo)

        assert os.path.isfile(os.path.join(file_path, photo[0]))
        assert os.path.isfile(os.path.join(file_path, photo[1]))
        assert os.path.isfile(os.path.join(file_path, photo[2]))
        assert os.path.isfile(os.path.join(file_path, photo[3]))

        _remove_files(photo)

    def test_update_place_photos_maximum_reached(self, client):
        _, host_token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        client.post(_url, data=_params(_event_json({"id": place.id}), 2), headers=_auth_header(host_token))

        client.put(_url, data=_params({"id": 1}, 2), headers=_auth_header(host_token))
        client.put(_url, data=_params({"id": 1}, 2), headers=_auth_header(host_token))
        client.put(_url, data=_params({"id": 1}, 2), headers=_auth_header(host_token))
        client.put(_url, data=_params({"id": 1}, 2), headers=_auth_header(host_token))
        r = client.put(_url, data=_params({"id": 1}, 2), headers=_auth_header(host_token))

        assert r.status_code == 400
        assert r.json['message'][:33] == 'Total number of files can be only'

        photo = json.loads(Event.get_by_id(1).photo)

        _remove_files(photo)

    #
    # Delete
    #
    def test_delete_event(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)
        event = _create_event({"id": place.id})

        r = client.delete(_url, data={'id': event.id}, headers=_auth_header(token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'

    def test_delete_event_by_admin(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)
        event = _create_event({"id": place.id})

        _, admin_token, _ = _create_user(role=1, email='bar@foo.com')

        r = client.delete(_url, data={'id': event.id}, headers=_auth_header(admin_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'

    def test_delete_event_no_input(self, client):
        _, token, host_dump = _create_user(role=2)
        _ = _create_place(host_dump)

        r = client.delete(_url, data={}, headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_delete_event_no_header(self, client):
        r = client.delete(_url, data={})

        assert r.status_code == 401
        assert r.json['msg'] == "Missing Authorization Header"

    def test_delete_event_not_exists_event(self, client):
        _, token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)
        _ = _create_event({"id": place.id})

        r = client.delete(_url, data={'id': 2}, headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "Event does not exist"

    def test_delete_event_without_access(self, client):
        _, token, host_dump = _create_user(role=2)
        _, _, host2_dump = _create_user(email="bar@foo.com", role=2)
        place1 = _create_place(host_dump)
        place2 = _create_place(host2_dump)
        _ = _create_event({"id": place1.id})
        event2 = _create_event({"id": place2.id})

        r = client.delete(_url, data={'id': event2.id}, headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == "Not enough privileges"

    def test_delete_event_specific_photo(self, client):
        _, host_token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        client.post(_url, data=_params(_event_json({"id": place.id}), 2), headers=_auth_header(host_token))

        photo = json.loads(Event.get_by_id(1).photo)

        r1 = client.delete(_url, data={'id': 1, 'photo': photo[0]}, headers=_auth_header(host_token))
        r2 = client.delete(_url, data={'id': 1, 'photo': photo[1]}, headers=_auth_header(host_token))

        assert r1.status_code == 200
        assert r1.json['status'] == 'success'
        assert r2.status_code == 200
        assert r2.json['status'] == 'success'

        file_path = os.path.join(flask.current_app.root_path, flask.current_app.config['UPLOAD_FOLDER'])

        assert not os.path.isfile(os.path.join(file_path, photo[0]))
        assert not os.path.isfile(os.path.join(file_path, photo[1]))

    def test_delete_event_all_photos(self, client):
        _, host_token, host_dump = _create_user(role=2)
        place = _create_place(host_dump)

        client.post(_url, data=_params(_event_json({"id": place.id}), 2), headers=_auth_header(host_token))

        photo = json.loads(Event.get_by_id(1).photo)

        r = client.delete(_url, data={'id': 1}, headers=_auth_header(host_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'

        file_path = os.path.join(flask.current_app.root_path, flask.current_app.config['UPLOAD_FOLDER'])

        assert not os.path.isfile(os.path.join(file_path, photo[0]))
        assert not os.path.isfile(os.path.join(file_path, photo[1]))
