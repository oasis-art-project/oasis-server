from flask import render_template, Blueprint, request
from .auth import auth

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
def index():
 return render_template("index.html")

@home_blueprint.route('/api/auth', methods=['POST'])
def auth_user():
 return auth(request.get_json(force=True))
