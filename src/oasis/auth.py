import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from .schemas import validate_user
from .users import find_user
from src import flask_bcrypt

auth_blueprint = Blueprint('auth', __name__)

#@jwt.unauthorized_loader
#def unauthorized_response(callback):
#    return jsonify({
#        'ok': False,
#        'message': 'Missing Authorization Header'
#    }), 401

from src import flask_bcrypt

@auth_blueprint.route('/api/auth', methods=['POST'])
def user_auth():
    data = validate_user(request.get_json(force=True))
    if data['ok']:
            data = data['data']
            user = find_user(data['email'])
            
            if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
                del user['password']
                access_token = create_access_token(identity=data)
                refresh_token = create_refresh_token(identity=data)
                user['token'] = access_token
                user['refresh'] = refresh_token
                return jsonify({'ok': True, 'data': user}), 200
            else:
                return jsonify({'ok': False, 'message': 'invalid username or password'}), 401
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@auth_blueprint.route('/api/register', methods=['POST'])
def user_register():
    data = validate_user(request.get_json(force=True))
    if data['ok']:
        data = data['data']
        data['password'] = flask_bcrypt.generate_password_hash(data['password'])
        print(data['password'])
        # Insert
        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400
