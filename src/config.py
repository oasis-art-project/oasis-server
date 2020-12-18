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
    S3_BUCKET = os.environ.get("S3_BUCKET")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

    # Upload data conf
    MAX_IMAGE_SIZE = 2048 * 2048
    IMAGE_UPLOAD_FOLDER = os.environ.get("IMAGE_UPLOAD_FOLDER")
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # JWT
    JWT_SECRET_KEY = 'jwt-secret-string'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # SMTP mail
    MAIL_SERVER = 'mail.hover.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # Twilio SMS
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

class ProductionConfig(Config):
    DEBUG = False


class TestConfig(Config):
    DEBUG = True
    TESTING = True

    # Store DB in memory using SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'

    # Discard environmental variable
    IMAGE_UPLOAD_FOLDER = ''

