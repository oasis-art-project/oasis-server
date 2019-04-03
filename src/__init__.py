import os
import json
import datetime
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
app = Flask(__name__,
 static_folder = './public',
 template_folder="./static")
from src.oasis.views import home_blueprint

# register the blueprints
app.register_blueprint(home_blueprint)

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from src.oasis import db
db.init_app(app)
