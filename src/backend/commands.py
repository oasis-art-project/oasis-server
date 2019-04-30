"""
Boston University. Spring 2019
@author: Maxim Tsybanov (oasis@tsybanov.com)
"""

import click
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
    try:
        UserSchema().load({
            'email': 'admin@oasis.com',
            'password': 'adminOasis',
            'firstName': 'Admin',
            'lastName': 'Oasis',
            'role': 1
        }).data.save()
        print('Admin created. Please use credentials:\nLogin: admin@oasis.com\nPassword: adminOasis')
    except IntegrityError:
        print('Admin is already created. Please use credentials:\nLogin: admin@oasis.com\nPassword: adminOasis')

