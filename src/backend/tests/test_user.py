# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

import json
import os
from copy import deepcopy

import flask

from src.backend.controllers.userController import user_schema as _user_schema
from src.backend.models.userModel import User
from src.backend.tests.helpers import \
    params as _params, \
    remove_files as _remove_files, \
    create_user as _create_user, \
    user_json as _user_json, \
    auth_header as _auth_header


_url = '/api/user/'

# TODO: add more ASSERT NOT fields
# TODO: read r.json for more ASSERTS
class TestUser:
    """
    Test CRUD operations edge cases of the User model
    """

    #
    # Get
    #
    def test_get_user(self, client):
        user, _, user_dump = _create_user()

        r = client.get("{}{}".format(_url, user.id))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert r.json['user']['id']
        assert r.json['user']['firstName'] == user_dump['firstName']
        assert r.json['user']['lastName'] == user_dump['lastName']
        assert r.json['user']['twitter'] == user_dump['twitter']
        assert r.json['user']['flickr'] == user_dump['flickr']
        assert r.json['user']['instagram'] == user_dump['instagram']
        assert r.json['user']['role'] == user_dump['role']
        assert 'email' not in r.json['user']
        assert 'token' not in r.json['user']
        assert 'password' not in r.json['user']

    def test_get_user_not_exists_user(self, client):
        r = client.get("{}{}".format(_url, 1))

        assert r.status_code == 400
        assert r.json['message'] == 'User does not exist'

    def test_get_user_by_admin(self, client):
        _, admin_token, _ = _create_user(email='bar@foo.com', role=1)
        user, _, user_dump = _create_user()

        r = client.get("{}{}".format(_url, user.id), headers=_auth_header(admin_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert r.json['user']['id']
        assert r.json['user']['email'] == user_dump['email']
        assert r.json['user']['firstName'] == user_dump['firstName']
        assert r.json['user']['lastName'] == user_dump['lastName']
        assert r.json['user']['twitter'] == user_dump['twitter']
        assert r.json['user']['flickr'] == user_dump['flickr']
        assert r.json['user']['instagram'] == user_dump['instagram']
        assert r.json['user']['role'] == user_dump['role']
        assert 'token' not in r.json['user']
        assert 'password' not in r.json['user']

    def test_get_user_with_email_by_admin(self, client):
        _, admin_token, _ = _create_user(email='bar@foo.com', role=1)
        user, _, user_dump = _create_user()

        r = client.get("{}{}".format(_url, user.id), headers=_auth_header(admin_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert r.json['user']['id']
        assert r.json['user']['email'] == user_dump['email']
        assert r.json['user']['firstName'] == user_dump['firstName']
        assert r.json['user']['lastName'] == user_dump['lastName']
        assert r.json['user']['twitter'] == user_dump['twitter']
        assert r.json['user']['flickr'] == user_dump['flickr']
        assert r.json['user']['instagram'] == user_dump['instagram']
        assert r.json['user']['role'] == user_dump['role']
        assert 'token' not in r.json['user']
        assert 'password' not in r.json['user']

    def test_get_not_exists_user_with_email(self, client):
        _, admin_token, _ = _create_user(role=1)

        r = client.get("{}{}".format(_url, 'bar@foo.com'), headers=_auth_header(admin_token))

        assert r.status_code == 400
        assert r.json['message'] == 'User does not exist'

    def test_get_user_with_email_not_by_admin(self, client):
        _, user_token, _ = _create_user(email='bar@foo.com')
        user, _, _ = _create_user()

        r = client.get("{}{}".format(_url, user.email), headers=_auth_header(user_token))

        assert r.status_code == 401
        assert r.json['message'] == 'Not enough privileges'

    def test_get_users(self, client):
        user, user_token, dump = _create_user()

        another_user = {
            'firstName': 'bar',
            'lastName': 'foo',
            'twitter': 'anotherTwitter',
            'flickr': 'anotherFlickr',
            'instagram': 'anotherInstagram',
            'role': 3,
            'email': 'bar@foo.com'
        }

        _, _, another_user_dump = _create_user(**another_user)

        r = client.get(_url)

        assert r.status_code == 200

        assert r.json['users'][0]['firstName'] == dump['firstName']
        assert r.json['users'][0]['lastName'] == dump['lastName']
        assert r.json['users'][0]['twitter'] == dump['twitter']
        assert r.json['users'][0]['flickr'] == dump['flickr']
        assert r.json['users'][0]['instagram'] == dump['instagram']
        assert r.json['users'][0]['role'] == dump['role']
        assert r.json['users'][0]['id'] == 1
        assert 'email' not in r.json['users'][0]
        assert 'password' not in r.json['users'][0]
        assert 'token' not in r.json['users'][0]

        assert r.json['users'][1]['firstName'] == another_user_dump['firstName']
        assert r.json['users'][1]['lastName'] == another_user_dump['lastName']
        assert r.json['users'][1]['twitter'] == another_user_dump['twitter']
        assert r.json['users'][1]['flickr'] == another_user_dump['flickr']
        assert r.json['users'][1]['instagram'] == another_user_dump['instagram']
        assert r.json['users'][1]['role'] == another_user_dump['role']
        assert r.json['users'][1]['id'] == 2
        assert 'email' not in r.json['users'][1]
        assert 'password' not in r.json['users'][1]
        assert 'token' not in r.json['users'][1]

    def test_get_users_by_admin(self, client):
        _, admin_token, admin_dump = _create_user(role=1)

        another_user = {
            'email': 'bar@foo.com',
            'firstName': 'bar',
            'lastName': 'foo',
            'twitter': 'anotherTwitter',
            'flickr': 'anotherFlickr',
            'instagram': 'anotherInstagram',
            'role': 3
        }

        _, _, another_user_dump = _create_user(**another_user)

        r = client.get(_url, headers=_auth_header(admin_token))

        assert r.json['users'][0]['email'] == admin_dump['email']
        assert r.json['users'][0]['firstName'] == admin_dump['firstName']
        assert r.json['users'][0]['lastName'] == admin_dump['lastName']
        assert r.json['users'][0]['twitter'] == admin_dump['twitter']
        assert r.json['users'][0]['flickr'] == admin_dump['flickr']
        assert r.json['users'][0]['instagram'] == admin_dump['instagram']
        assert r.json['users'][0]['role'] == admin_dump['role']
        assert r.json['users'][0]['id'] == 1
        assert 'password' not in r.json['users'][0]
        assert 'token' not in r.json['users'][0]

        assert r.json['users'][1]['email'] == another_user_dump['email']
        assert r.json['users'][1]['firstName'] == another_user_dump['firstName']
        assert r.json['users'][1]['lastName'] == another_user_dump['lastName']
        assert r.json['users'][1]['twitter'] == another_user_dump['twitter']
        assert r.json['users'][1]['flickr'] == another_user_dump['flickr']
        assert r.json['users'][1]['instagram'] == another_user_dump['instagram']
        assert r.json['users'][1]['role'] == another_user_dump['role']
        assert r.json['users'][1]['id'] == 2
        assert 'password' not in r.json['users'][1]
        assert 'token' not in r.json['users'][1]

    #
    # Create
    #
    def test_create_user(self, client):
        r = client.post(_url, data=_params(_user_json()))

        assert r.status_code == 201
        assert r.json['status'] == 'success'
        assert r.json['token'] != ''
        assert User.get_by_id(1).firstName == _user_json()['firstName']

    def test_create_no_input(self, client):
        r = client.post(_url, data={})

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_create_miss_input(self, client):
        r = client.post(_url, data=_params({"foo": "bar"}))

        assert r.status_code == 422
        assert r.json['message']['email'] == ["Missing data for required field."]
        assert r.json['message']['password'] == ["Missing data for required field."]
        assert r.json['message']['firstName'] == ["Missing data for required field."]
        assert r.json['message']['lastName'] == ["Missing data for required field."]
        assert r.json['message']['role'] == ["Missing data for required field."]

    def test_create_incorrect_input(self, client):
        user = {'email': "foobarcom",
                'password': "foo",
                'firstName': "",
                'lastName': " ",
                'role': 6
                }

        r = client.post(_url, data=_params(user))

        assert r.status_code == 422
        assert r.json['message']['email'] == ["Not a valid email address."]
        assert r.json['message']['password'] == ["Shorter than minimum length 6."]
        assert r.json['message']['firstName'] == ["String does not match expected pattern."]
        assert r.json['message']['lastName'] == ["String does not match expected pattern."]
        assert r.json['message']['role'] == ["Must be between 1 and 4."]

    def test_create_user_exists(self, client):
        client.post(_url, data=_params(_user_json()))

        r = client.post(_url, data=_params(_user_json()))

        assert r.status_code == 400
        assert r.json['message'] == 'User already exists'

    def test_create_admin(self, client):
        admin = _user_json()
        admin["role"] = 1

        r = client.post(_url, data=_params(admin))

        assert r.status_code == 401
        assert r.json['message'] == "Not enough privileges"

    def test_create_admin_by_admin(self, client):
        admin, token, _ = _create_user(role=1)

        new_admin = _user_json()
        new_admin['email'] = "bar@foo.com"
        new_admin['role'] = 1

        r = client.post(_url, data=_params(new_admin), headers=_auth_header(token))

        assert r.status_code == 201
        assert r.json['status'] == 'success'
        assert r.json['token'] != ''

    #
    # Update
    #
    def test_update_user(self, client):
        user, token, _ = _create_user()

        updates = {
            'email': "bar@foo.com",
            'password': "barfoo",
            'firstName': "bar",
            'lastName': "foo",
            'twitter': 'anotherTwitter',
            'flickr': 'anotherFlickr',
            'instagram': 'anotherInstagram'
        }

        r = client.put(_url, data=_params(updates), headers=_auth_header(token))

        updated_user = User.get_by_id(user.id)

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert r.json['token'] != ''
        assert updated_user is not None
        assert updated_user.email == updates['email']
        assert updated_user.firstName == updates['firstName']
        assert updated_user.lastName == updates['lastName']
        assert updated_user.twitter == updates['twitter']
        assert updated_user.flickr == updates['flickr']
        assert updated_user.instagram == updates['instagram']

    def test_update_user_by_admin(self, client):
        user, _, _ = _create_user()

        _, admin_token, _ = _create_user(role=1, email='foo@foo.com')

        updates = {
            'id': user.id,
            'email': "bar@foo.com",
            'password': "barfoo",
            'firstName': "bar",
            'lastName': "foo",
            'twitter': 'anotherTwitter',
            'flickr': 'anotherFlickr',
            'instagram': 'anotherInstagram'
        }

        r = client.put(_url, data=_params(updates), headers=_auth_header(admin_token))

        updated_user = User.get_by_id(user.id)

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert r.json['token'] != ''
        assert updated_user is not None
        assert updated_user.email == updates['email']
        assert updated_user.firstName == updates['firstName']
        assert updated_user.lastName == updates['lastName']
        assert updated_user.twitter == updates['twitter']
        assert updated_user.flickr == updates['flickr']
        assert updated_user.instagram == updates['instagram']

    def test_update_login_updated_password(self, client):
        user, token, _ = _create_user()

        updates = {'password': "barfoo"}

        r = client.put(_url, data=_params(updates), headers=_auth_header(token))

        updated_user = User.get_by_id(user.id)

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert r.json['token'] != ''
        assert updated_user.check_password(updates['password'])

    def test_update_user_no_input(self, client):
        _, token, _ = _create_user()

        r = client.put(_url, data={}, headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_update_user_no_header(self, client):
        r = client.put(_url, data={})

        assert r.status_code == 401
        assert r.json['msg'] == "Missing Authorization Header"

    def test_update_user_partly_input(self, client):
        user, token, dump = _create_user()

        for input_data in dump:
            if input_data == 'id':
                continue

            partly_user_iteration = deepcopy(dump)

            # 0 for editing
            # 1 for removing
            for i in range(2):
                if i == 0:
                    if type(partly_user_iteration[input_data]) == str():
                        partly_user_iteration[input_data] = '{}0'.format(partly_user_iteration[input_data])
                    else:
                        continue
                if i == 1:
                    del partly_user_iteration[input_data]

                client.put(_url, data=_params(partly_user_iteration), headers=_auth_header(token))

                updated_user = _user_schema.dump(User.get_by_id(user.id)).data

                if i == 0:
                    assert dump[input_data] != updated_user[input_data]
                if i == 1:
                    assert dump[input_data] == updated_user[input_data]

    def test_update_user_incorrect_input(self, client):
        _, token, _ = _create_user()

        updates = {'email': "foobarcom",
                   'password': "foo",
                   'firstName': "",
                   'lastName': " ",
                   'role': 6
                   }

        r = client.put(_url, data=_params(updates), headers=_auth_header(token))

        assert r.status_code == 422
        assert r.json['message']['email'] == ["Not a valid email address."]
        assert r.json['message']['password'] == ["Shorter than minimum length 6."]
        assert r.json['message']['firstName'] == ["String does not match expected pattern."]
        assert r.json['message']['lastName'] == ["String does not match expected pattern."]
        assert r.json['message']['role'] == ["Must be between 1 and 4."]

    def test_update_user_not_exists_user(self, client):
        _, token, dump = _create_user()

        dump['id'] = 2

        r = client.put(_url, data=_params(dump), headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "User does not exist"

    def test_update_user_to_make_admin_by_admin(self, client):
        admin, token, _ = _create_user(email='bar@foo.com', role=1)

        _, _, dump = _create_user()
        dump['email'] = 'bar@bar.com'
        dump['firstName'] = 'bar'
        dump['lastName'] = 'foo'
        dump['twitter'] = 'anotherTwitter'
        dump['flickr'] = 'anotherFlickr'
        dump['instagram'] = 'anotherInstagram'
        dump['role'] = 1

        r = client.put(_url, data=_params(dump), headers=_auth_header(token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'
        assert r.json['token'] != ''

    def test_update_user_without_access(self, client):
        _, token, pseudo_admin_json = _create_user(email='bar@foo.com', role=2)

        # An attempt to make himself as an admin
        pseudo_admin_json['role'] = 1

        r = client.put(_url, data=_params(pseudo_admin_json), headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == 'Not enough privileges'

        # An attempt to edit someone's account
        user, _, dump = _create_user()

        dump['firstName'] = 'bar'

        r = client.put(_url, data=_params(dump), headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == 'Not enough privileges'

    #
    # Delete
    #
    def test_delete_user(self, client):
        _, admin_token, _ = _create_user(email='bar@foo.com', role=1)

        user, _, _ = _create_user()

        r = client.delete(_url, data={'id': user.id}, headers=_auth_header(admin_token))

        assert r.status_code == 200
        assert r.json['status'] == 'success'

    def test_delete_user_no_input(self, client):
        _, token, _ = _create_user(role=2)

        r = client.delete(_url, data={}, headers=_auth_header(token))

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_delete_user_no_header(self, client):
        r = client.delete(_url, data={})

        assert r.status_code == 401
        assert r.json['msg'] == "Missing Authorization Header"

    def test_delete_user_not_exists_user(self, client):
        _, admin_token, _ = _create_user(email='bar@foo.com', role=1)

        r = client.delete(_url, data={'id': 2}, headers=_auth_header(admin_token))

        assert r.status_code == 400
        assert r.json['message'] == "User does not exist"

    def test_delete_user_without_access(self, client):
        _, token, _ = _create_user()
        user, _, _ = _create_user(email='bar@foo.com')

        r = client.delete(_url, data={"id": user.id}, headers=_auth_header(token))

        assert r.status_code == 401
        assert r.json['message'] == "Not enough privileges"
