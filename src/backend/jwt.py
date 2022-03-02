# -*- coding: utf-8 -*-

"""
Part of the OASIS ART PROJECT - https://github.com/orgs/oasis-art-project
Copyright (c) 2019-22 TEAM OASIS
License Artistic-2.0
"""

from src.backend.extensions import jwt
from src.backend.models.userModel import User


# JWT Callbacks
def jwt_identity(payload):
    return User.query.filter_by(id=payload).first()


def identity_loader(user):
    return user


# Blacklist of tokens
blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist
