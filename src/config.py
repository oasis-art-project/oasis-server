# -*- coding: utf-8 -*-

"""
Part of the OASIS ART PROJECT - https://github.com/orgs/oasis-art-project
Copyright (c) 2019-22 TEAM OASIS
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

    # Webapp url
    WEBAPP_URL = os.environ.get('WEBAPP_URL')

    # SQLAlchemy conf
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # AWS configuration
    S3_BUCKET = os.environ.get("S3_BUCKET")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

    # Upload data conf
    MAX_IMAGE_PREV_RES = 512
    MAX_IMAGE_FULL_RES = 4096    
    IMAGE_UPLOAD_FOLDER = os.environ.get("IMAGE_UPLOAD_FOLDER")
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # JWT
    JWT_SECRET_KEY = 'jwt-secret-string'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # SMTP mail
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = True

class ProductionConfig(Config):
    DEBUG = False


class TestConfig(Config):
    DEBUG = True
    TESTING = True

    # Store DB in memory using SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'

    # Discard environmental variable
    IMAGE_UPLOAD_FOLDER = ''

