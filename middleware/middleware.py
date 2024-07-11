import os
import jwt
from functools import wraps
from flask import request, jsonify
from data.conn import mydb

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # Read the token from token.txt file
            with open('token.txt', 'r') as token_file:
                token = token_file.read().strip()
                
            if not token:
                return jsonify({'status': 'fail', 'message': 'Token is missing!'}), 401

            # secret_key = os.getenv('SECRET_KEY')
            # payload = jwt.decode(token, secret_key, algorithms=['HS256'])

            # Check if the token exists in the user_tokens table
            user_token_query = "SELECT * FROM users WHERE token = %s"
            user_token_cursor = mydb.cursor(dictionary=True)
            user_token_cursor.execute(user_token_query, (token,))
            user_token_result = user_token_cursor.fetchone()

            # Check if the token exists in the company_tokens table
            company_token_query = "SELECT * FROM company WHERE token = %s"
            company_token_cursor = mydb.cursor(dictionary=True)
            company_token_cursor.execute(company_token_query, (token,))
            company_token_result = company_token_cursor.fetchone()
            
            route_name = request.endpoint

            if user_token_result and route_name.startswith('user_routes'):
                # Token exists in user_tokens table, allow access to user endpoints
                return f(*args, **kwargs)
            elif company_token_result and route_name.startswith('company_routes'):
                # Token exists in company_tokens table, allow access to company endpoints
                return f(*args, **kwargs)
            else:
                return jsonify({'status': 'fail', 'message': 'Token is invalid or expired!'}), 401

        except Exception as e:
            return jsonify({'status': 'fail', 'message': 'Token is invalid or expired!'}), 401
        finally:
            # Close database cursors and connection
            if 'user_token_cursor' in locals():
                user_token_cursor.close()
            if 'company_token_cursor' in locals():
                company_token_cursor.close()

    return decorated
