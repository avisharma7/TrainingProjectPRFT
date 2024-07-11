from flask import request, jsonify
from data.conn import mydb, mycursor
import re
import os
import jwt

def register(table_name):
    def user_register():
        data = request.get_json()
        
        username = data.get('username')
            
        query = f"SELECT COUNT(*) FROM {table_name} WHERE username = %s"
        mycursor.execute(query, (username,))
        result = mycursor.fetchone()
        if result[0] > 0:
            return jsonify({'status': 'fail','message': 'Username already exists'})

        password = data.get('password')
        
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*\W).{10,}$')
        if not pattern.match(password):
            return jsonify({'status': 'fail','message': 'Password must be at least 10 characters long, contain at least one special character, and one uppercase letter.'})
        
        payload = {'username': username}
        secret_key = os.getenv('SECRET_KEY')
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        
        query = f"INSERT INTO {table_name} (username, password, token) VALUES (%s, SHA2(CONCAT(%s, 'salt'), 256), %s)"
        mycursor.execute(query, (username, password, token))
        mydb.commit()

        return jsonify({'status': 'success','message': 'Registration successful'})

    return user_register()

def login(table_name):
    def user_login():
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')

        query = f"SELECT * FROM {table_name} WHERE username = %s AND password = SHA2(CONCAT(%s, 'salt'), 256)"
        mycursor.execute(query, (username, password))
        user = mycursor.fetchone()

        if user:
            payload = {'username': user[1]}
            secret_key = os.getenv('SECRET_KEY')
            
            # Generate new JWT token
            token = jwt.encode(payload, secret_key, algorithm='HS256')
            
            # Update token in the database
            update_query = f"UPDATE {table_name} SET token = %s WHERE username = %s"
            mycursor.execute(update_query, (token, username))
            mydb.commit()

            # Update token in token.txt file
            with open('token.txt', 'w') as token_file:
                token_file.write(token)

            return jsonify({'status': 'success', 'message': 'Login successful', 'token': token})
               
        return jsonify({'status': 'fail', 'message': 'Invalid username or password'})

    return user_login()
