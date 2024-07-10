import os
import jwt
from functools import wraps
from flask import request, jsonify

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # Read the token from token.txt file
            with open('token.txt', 'r') as token_file:
                token = token_file.read().strip()
                
            if not token:
                return jsonify({'status': 'fail', 'message': 'Token is missing!'}), 401

            secret_key = os.getenv('SECRET_KEY')
            jwt.decode(token, secret_key, algorithms=['HS256'])
        except Exception as e:
            return jsonify({'status': 'fail', 'message': 'Token is invalid or expired!'}), 401

        return f(*args, **kwargs)
    return decorated
