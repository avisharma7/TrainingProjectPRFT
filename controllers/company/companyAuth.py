from flask import request, jsonify
from data.conn import mydb, mycursor
import re

def company_register():
    data = request.get_json()
    
    username = data.get('username')
        
    query = "SELECT COUNT(*) FROM company WHERE username = %s"
    mycursor.execute(query, (username,))
    result = mycursor.fetchone()
    if result[0] > 0:
        return jsonify({'status': 'fail','message': 'Username already exists'})

    password = data.get('password')
    
    pattern = re.compile(r'^(?=.*[A-Z])(?=.*\W).{10,}$')
    if not pattern.match(password):
        return jsonify({'status': 'fail','message': 'Password must be at least 10 characters long, contain at least one special character, and one uppercase letter.'})
        
    company_name = data.get('company_name')
    
    query = "INSERT INTO company (username, password, company_name) VALUES (%s, %s, %s)"
    mycursor.execute(query, (username, password, company_name))
    mydb.commit()

    return jsonify({'status': 'success','message': 'Registration successful'})


def company_login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')

    query = "SELECT * FROM company WHERE username = %s AND password = %s"
    mycursor.execute(query, (username, password))
    user = mycursor.fetchone()

    if not user:
        return jsonify({'status': 'fail', 'message': 'Invalid username or password' })

    return jsonify({'status': 'success','message': 'Login successful','user': user})
