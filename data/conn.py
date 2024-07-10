import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = os.getenv('DB_PASS'),
    database = os.getenv('DB_NAME'),
    port = 3306
)

db_config = {
    'user': 'root',
    'password': os.getenv('DB_PASS'),
    'host': 'localhost',
    'database': os.getenv('DB_NAME')
}

mycursor = mydb.cursor(buffered=True)