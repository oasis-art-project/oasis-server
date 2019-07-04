# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

import os

from flask import Flask, render_template
from flask_migrate import MigrateCommand

from src.backend.commands import test, seed
from src.backend.extensions import db, migrate, jwt, ma, manager, api_bp, api
from src.backend.jwt import jwt_identity, identity_loader
from src.backend.router import init_router
from src.config import ProductionConfig


def create_app(conf=ProductionConfig):
    app = Flask(__name__,
                static_folder='./public',
                template_folder="../../webapp")

    # Load config
    app.config.from_object(conf)

    # Initializers
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    jwt.user_loader_callback_loader(jwt_identity)
    jwt.user_identity_loader(identity_loader)
    migrate.init_app(app, db)
    manager.add_command('db', MigrateCommand)

    # Load router
    app.register_blueprint(api_bp, url_prefix='/api')
    init_router(api)

    # Load commands
    app.cli.add_command(test)
    app.cli.add_command(seed)

    # Load index.html from template folder
    @app.route('/')
    def index():
        return render_template("index.html")

    # Ensure the instance and upload folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(os.path.join('src', app.config['UPLOAD_FOLDER']))
    except OSError:
        pass

    return app
