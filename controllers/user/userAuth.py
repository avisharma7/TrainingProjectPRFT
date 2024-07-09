from flask import request, jsonify
from data.conn import mydb, mycursor
import re
import os
import jwt

def user_register():
    data = request.get_json()
    
    username = data.get('username')
        
    query = "SELECT COUNT(*) FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
    result = mycursor.fetchone()
    if result[0] > 0:
        return jsonify({'status': 'fail','message': 'Username already exists'})

    password = data.get('password')
    
    pattern = re.compile(r'^(?=.*[A-Z])(?=.*\W).{10,}$')
    if not pattern.match(password):
        return jsonify({'status': 'fail','message': 'Password must be at least 10 characters long, contain at least one special character, and one uppercase letter.'})
        
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    mycursor.execute(query, (username, password))
    mydb.commit()

    return jsonify({'status': 'success','message': 'Registration successful'})

def user_login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    mycursor.execute(query, (username, password))
    user = mycursor.fetchone()

    if user:
        payload = {'username': user[1]}
        secret_key = os.getenv('SECRET_KEY')
        
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        
        token_file = open('token.txt', 'w')
        
        token_file.write(token)
        
        return jsonify({'status': 'success','message': 'Login successful','token': token})
           
    return jsonify({'status': 'fail', 'message': 'Invalid username or password' })
