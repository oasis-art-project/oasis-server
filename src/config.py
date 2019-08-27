# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

import os
from datetime import timedelta


class Config(object):
    """
    Base configuration
    """
    # App path
    PARENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    INSTANCE_PATH = os.path.join(PARENT_PATH, 'instance')

    # SQLAlchemy conf
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/oasis.sqlite'.format(INSTANCE_PATH)
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/oasis'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    # Upload data conf
    MAX_CONTENT_LENGTH = 5000 * 1024
    UPLOAD_FOLDER = 'public/uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # JWT
    JWT_SECRET_KEY = 'jwt-secret-string'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)


class ProductionConfig(Config):
    DEBUG = False


class TestConfig(Config):
    DEBUG = True
    TESTING = True

    # In memory
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'

