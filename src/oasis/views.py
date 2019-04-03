from flask import render_template, Blueprint, request
from src import app
from .auth import auth
home_blueprint = Blueprint('home',__name__)

app.register_blueprint(home_blueprint)

@home_blueprint.route('/')
def index():
 return render_template("index.html")

@home_blueprint.route('/api/auth', methods=['POST'])
def auth_user():
 return auth(request.get_json(force=True))
