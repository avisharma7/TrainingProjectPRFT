import os
import jwt
from functools import wraps
from flask import request, jsonify

def read_token_from_file():
    try:
        with open('token.txt', 'r') as token_file:
            token = token_file.read().strip()
            return token
    except FileNotFoundError:
        return None

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = read_token_from_file()
        if not token:
            return jsonify({'status': 'fail', 'message': 'Unauthorized Action!'}), 403

        try:
            secret_key = os.getenv('SECRET_KEY')
            jwt.decode(token, secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'status': 'fail', 'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'status': 'fail', 'message': 'Invalid token!'}), 403

        return f(*args, **kwargs)
    return decorated_function
