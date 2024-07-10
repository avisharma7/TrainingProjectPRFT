from flask import request, jsonify
from data.conn import mycursor, mydb
from mysql.connector import Error

def createTable_IfNotExist(company_symbol):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {company_symbol} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Date DATE NOT NULL,
        Open FLOAT,
        High FLOAT,
        Low FLOAT,
        Close FLOAT,
        Volume INT
    )"""
    
    mycursor.execute(create_table_query)

def create_data():
    data = request.get_json()
    
    company_name = data.get('companyName')
    company_symbol = data.get('companySymbol')
   
    createTable_IfNotExist(company_symbol)
   
    insert_company_query = "INSERT INTO companies (name, symbol) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name)"
    mycursor.execute(insert_company_query, (company_name, company_symbol))
    mydb.commit()
   
    insert_data_query = f"""
    INSERT INTO {company_symbol} (date, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
   
    for entry in data.get('data', []):
        mycursor.execute(insert_data_query, (entry['Date'], entry['open'], entry['high'], entry['low'], entry['close'], entry['volume']))
        mydb.commit()
   
    return jsonify({"message": "Data inserted successfully"}), 201

def update_data(company_symbol):
    try:
        data = request.get_json()
        date = data.get('Date')
        update_fields = ", ".join([f"{key} = %s" for key in data if key != 'Date'])
        update_query = f"""
        UPDATE {company_symbol}
        SET {update_fields}
        WHERE date = %s
        """
        update_values = tuple(data[key] for key in data if key != 'Date') + (date,)
        
        mycursor.execute(update_query, update_values)
        mydb.commit()

        return jsonify({"message": "Data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update data"}), 500
    
def delete_data(company_symbol):
    data = request.get_json()
    if 'Date' in data:
        delete_query = f"DELETE FROM {company_symbol} WHERE date = %s"
        mycursor.execute(delete_query, (data['Date'],))
        mydb.commit()
        return jsonify({"message": f"Data for date {data['Date']} deleted successfully"}), 200
    
    return jsonify({'error': 'Please provide date'})
             
def get_data(company_symbol):
    mycursor.execute(f'SELECT * FROM {company_symbol}')
    rows = mycursor.fetchall()
    
    data = []
    for row in rows:
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