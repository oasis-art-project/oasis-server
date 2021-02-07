# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

import click
import os
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError

from src.backend.models.userModel import UserSchema

"""
Commands for flask CLI
"""

# flask test - start pytest
@click.command()
def test():
    import pytest
    rv = pytest.main(['src/backend/tests', '--tb=short'])
    exit(rv)


# flask seed - add an admin user
@click.command()
@with_appcontext
def seed():
    email = os.environ.get("ADMIN_EMAIL")
    if not email:
        raise Exception("Admin email is undefined. Set in ADMIN_EMAIL environmental variable")


    password = os.environ.get("ADMIN_PASSWORD")
    if not password:
        raise Exception("Admin password is undefined. Set in ADMIN_PASSWORD environmental variable")

    try:
        UserSchema().load({
            'email': email,
            'password': password,
            'firstName': 'Admin',
            'lastName': 'Oasis',
            'role': 1
        }).data.save()
        print('Admin created. Please use credentials:\nLogin', email, '\nPassword:', password)
    except IntegrityError:
        print('Admin is already created. Please use credentials:\nLogin: ', email, '\nPassword:', password)

