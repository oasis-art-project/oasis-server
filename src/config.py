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
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    # AWS configuration
    AWS_DISABLED = os.environ.get("AWS_DISABLED")
    S3_BUCKET = os.environ.get("S3_BUCKET")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

    # Upload data conf
    MAX_IMAGE_SIZE = 2024 * 2048
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

