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

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

# register the blueprints
app.register_blueprint(home_blueprint)

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.json_encoder = JSONEncoder

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from src.oasis import db
db.init_app(app)
