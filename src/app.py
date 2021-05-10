# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

import os

from flask import Flask, render_template, current_app
from flask_migrate import MigrateCommand
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room

from src.backend.commands import test, seed
from src.backend.extensions import db, migrate, jwt, ma, manager, api_bp, api, storage, mail, sms
from src.backend.jwt import jwt_identity, identity_loader
from src.backend.router import init_router
from src.config import ProductionConfig, TestConfig
from src.backend.sockets import CustomNamespace

def create_app(conf=ProductionConfig):
    app = Flask(__name__,
                static_folder='./public',
                template_folder="./templates")

    # Load config
    app.config.from_object(conf)

    # Enabled CORS: https://enable-cors.org/server_flask.html
    cors = CORS(app, resources={r"/*":{"origins":"*"}})

    # Chat init
    # socketio = SocketIO(app, cors_allowed_origins="*")
    # socketio.on_namespace(CustomNamespace(app))

    # Ensure the instance and upload folder exists
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    if not app.config['IMAGE_UPLOAD_FOLDER']:
        # Default local image upload folder
        if conf == ProductionConfig:
            app.config['IMAGE_UPLOAD_FOLDER'] = os.path.join(app.root_path, "public/imgs")
        elif conf == TestConfig:
            app.config['IMAGE_UPLOAD_FOLDER'] = os.path.join(app.root_path, "backend/tests/uploads")

    upload_folder = os.path.expanduser(app.config['IMAGE_UPLOAD_FOLDER'])
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Initializers
    db.init_app(app)
    ma.init_app(app)
    storage.init_app(app)
    mail.init_app(app)
    sms.init_app(app)
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

    @app.route("/account")
    def account():
        # Show the account-edit HTML page:
        return render_template('account.html')

    @app.route('/files')
    def files():
        summaries = storage.bucket.objects.all()
        return render_template('files.html', my_bucket=storage.bucket, files=summaries)

    return app