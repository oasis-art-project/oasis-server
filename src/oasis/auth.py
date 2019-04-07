import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from .schemas import validate_auth_user, validate_user
from .users import create_user, find_user
from src import flask_bcrypt, jwt

auth_blueprint = Blueprint('auth', __name__)

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401

@auth_blueprint.route('/api/auth', methods=['POST'])
def user_auth():
    data = validate_auth_user(request.get_json(force=True))
    if not data['ok']:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

    data = data['data']
    user = find_user(data['email'])

    if not user and not flask_bcrypt.check_password_hash(user['user_password'], data['password']):
         return jsonify({'ok': False, 'message': 'invalid username or password'}), 401

    del user['user_password']
    access_token = create_access_token(identity=data)
    refresh_token = create_refresh_token(identity=data)
    user['token'] = access_token
    user['refresh'] = refresh_token
    
    return jsonify({'ok': True, 'data': user}), 200

@auth_blueprint.route('/api/register', methods=['POST'])
def user_register():
    data = validate_user(request.get_json(force=True))
    
    if not data['ok']:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

    data = data['data']
        
    if find_user(data['email']) is not None:
        return jsonify({'ok' : False, 'message': 'User already exists'}), 401

    data['password'] = flask_bcrypt.generate_password_hash(data['password'])
    user = create_user(data)
    
    return jsonify({'ok': True, 'message': 'User created successfully!'}), 200

@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'token': create_access_token(identity=current_user)
    }
    return jsonify({'ok': True, 'data': ret}), 200
