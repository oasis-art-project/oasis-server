# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from src.backend.models.userModel import UserSchema
from src.backend.tests.helpers import \
    params as _params, \
    auth_header as _auth_header, \
    user_json as _user_json

_url = '/api/login/'
_user_schema = UserSchema()


class TestLogin:
    def test_login(self, client):
        user = _user_schema.load(_user_json()).data
        user.save()

        r = client.post(_url, data=_params({'email': _user_json()['email'], 'password': _user_json()['password']}))

        assert r.status_code == 200
        assert r.json['token'] != ""

    def test_login_wrong_password(self, client):
        user = _user_schema.load(_user_json()).data
        user.save()

        r = client.post(_url, data=_params({'email': _user_json()['email'], 'password': 'barfoo'}))

        assert r.status_code == 401
        assert r.json['message'] == "Wrong password"

    def test_login_missing_no_input(self, client):
        user = _user_schema.load(_user_json()).data
        user.save()

        r = client.post(_url, data={})

        assert r.status_code == 400
        assert r.json['message'] == 'No input data provided'

    def test_login_missing_incorrect_input(self, client):
        user = _user_schema.load(_user_json()).data
        user.save()

        r = client.post(_url, data=_params({'foo': 'bar'}))

        assert r.status_code == 400
        assert r.json['message'] == "No input data provided"

    def test_logout(self, client):
        user = _user_schema.load(_user_json()).data
        user.save()

        token = client.post(_url, data=_params({'email': _user_json()['email'],
                                                'password': _user_json()['password']})).json['token']

        logout = client.delete(_url, headers=_auth_header(token))
        r = client.delete(_url, headers=_auth_header(token))

        assert logout.status_code == 200
        assert logout.json['status'] == "success"
        assert r.status_code == 401
        assert r.json['msg'] == 'Token has been revoked'
