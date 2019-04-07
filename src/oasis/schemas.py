from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

auth_user_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 5
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}

user_schema = {
    "type": "object",
    "properties": {
        "firstName" : {
            "type": "string",
            "minLength": 1
        },
        "lastName" : {
            "type": "string",
            "minLength": 1,
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 5
        },
        "role": {
            "type": "number",
            "minimum": 1,
            "maximum": 4
        }
    },
    "required": ["firstName", "lastName", "email", "password", "role"],
    "additionalProperties": False
}

def validate_auth_user(data):
    try:
        validate(data, auth_user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}

def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
