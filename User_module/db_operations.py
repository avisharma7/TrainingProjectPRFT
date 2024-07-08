# db_operations.py
import mysql.connector

# Database connection details
db_config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'database': 'SMA'
}

def fetch_companies_from_db():
    conn = mysql.connector.connect(**db_config)
    c = conn.cursor()
    c.execute('SELECT symbol, name FROM companies')
    companies = {symbol: name for symbol, name in c.fetchall()}
    c.close()
    conn.close()
    return companies
