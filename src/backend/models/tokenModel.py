# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from datetime import datetime
from flask_jwt_extended import create_access_token, decode_token
from src.backend.extensions import db
from src.backend.models.model import SurrogatePK


class Token(SurrogatePK, db.Model):
    __tablename__ = 'tokens'
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.Integer, nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    def __init__(self, **kwargs):
        super(Token, self).__init__(**kwargs)

    @staticmethod
    def _epoch_utc_to_datetime(epoch_utc):
        return datetime.fromtimestamp(epoch_utc)

    @staticmethod
    def create_token(user):
        user_full_name = (user.firstName + " " + user.lastName).strip()

        token = create_access_token(identity=user.id, user_claims={'fullName': user_full_name, 'email': user.email, 'role': user.role})
        decoded_token = decode_token(token)

        jti = decoded_token['jti']
        token_type = decoded_token['type']
        user_identity = user.id
        expires = Token._epoch_utc_to_datetime(decoded_token['exp'])
        revoked = False

        Token(jti=jti, token_type=token_type, user_identity=user_identity, expires=expires, revoked=revoked).save()

        return token

    @staticmethod
    def is_token_revoked(token):
        decoded_token = decode_token(token)
        jti = decoded_token['jti']
        decoded_token = Token.query.filter_by(jti=jti).one()
        return decoded_token.revoked if decoded_token else True

    @staticmethod
    def revoke_token(token):
        decoded_token = decode_token(token)
        decoded_token = Token.query.filter_by(jti=decoded_token['jti']).one()

        if not token:
            return "No token in database"

        decoded_token.revoked = True
        decoded_token.save()

    @staticmethod
    def revoke_token_by_user_identity(identity):
        token = Token.query.filter_by(user_identity=identity).first()

        if not token:
            return "No token in database"

        token.revoked = True
        token.save()
