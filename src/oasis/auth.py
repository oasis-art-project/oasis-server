import os
from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
#from src import flask_bcrypt, jwt
from .schemas import validate_user
from .users import find_user

#@jwt.unauthorized_loader
#def unauthorized_response(callback):
#    return jsonify({
#        'ok': False,
#        'message': 'Missing Authorization Header'
#    }), 401


def auth(req):
    data = validate_user(req)
    if data['ok']:
            data = data['data']
            user = find_user(data['email'])
            print(user)
            return data['email']
            #return jsonify({'ok': True, 'data': user}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400
