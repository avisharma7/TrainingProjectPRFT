from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'database': 'SMA'
}

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(query, data=None):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(query, data=None):
    connection = create_connection()
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, data)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"The error '{e}' occurred")
    return result

# Ensure companies table exists
create_companies_table_query = """
CREATE TABLE IF NOT EXISTS companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    symbol VARCHAR(10) NOT NULL
)"""
execute_query(create_companies_table_query)

@app.route('/create_data', methods=['POST'])
def create_data():
    data = request.get_json()
    company_name = data['companyName']
    company_symbol = data['companySymbol']
    
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {company_symbol} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE NOT NULL,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume INT
    )"""
    execute_query(create_table_query)
    
    insert_company_query = """
    INSERT INTO companies (name, symbol) VALUES (%s, %s)
    """
    execute_query(insert_company_query, (company_name, company_symbol))
    
    insert_data_query = f"""
    INSERT INTO {company_symbol} (date, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    for entry in data['data']:
        execute_query(insert_data_query, (entry['Date'], entry['open'], entry['high'], entry['low'], entry['close'], entry['volume']))
    
    return jsonify({"message": "Data inserted successfully"}), 201

@app.route('/update_data/<company_symbol>', methods=['PUT'])
def update_data(company_symbol):
    data = request.get_json()
    date = data['Date']
    update_fields = ", ".join([f"{key} = %s" for key in data if key != 'Date'])
    update_query = f"""
    UPDATE {company_symbol}
    SET {update_fields}
    WHERE date = %s
    """
    update_values = tuple(data[key] for key in data if key != 'Date') + (date,)
    execute_query(update_query, update_values)
    
    return jsonify({"message": "Data updated successfully"}), 200

@app.route('/delete_data/<company_symbol>', methods=['DELETE'])
def delete_data(company_symbol):
    data = request.get_json()
    if 'Date' in data:
        delete_query = f"DELETE FROM {company_symbol} WHERE date = %s"
        execute_query(delete_query, (data['Date'],))
        return jsonify({"message": f"Data for date {data['Date']} deleted successfully"}), 200
    else:
        drop_table_query = f"DROP TABLE {company_symbol}"
        execute_query(drop_table_query)
        
        delete_company_query = "DELETE FROM companies WHERE symbol = %s"
        execute_query(delete_company_query, (company_symbol,))
        
        return jsonify({"message": f"Table {company_symbol} and corresponding company data deleted successfully"}), 200

@app.route('/get_data/<company_symbol>', methods=['GET'])
def get_data(company_symbol):
    select_query = f"SELECT * FROM {company_symbol}"
    results = execute_read_query(select_query)
    
    data = []
    for row in results:
        data.append({
            "id": row[0],
            "date": row[1],
            "open": row[2],
            "high": row[3],
            "low": row[4],
            "close": row[5],
            "volume": row[6]
        })
    
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)
