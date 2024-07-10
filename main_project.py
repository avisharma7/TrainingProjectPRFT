from flask import Flask, request, jsonify, session,send_from_directory
from matplotlib.dates import DateFormatter
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import base64
import io
import yfinance as yf
from sqlalchemy import create_engine, text
import os

# Define role constants
USER_ROLE = 'user'
COMPANY_ROLE = 'companyauth'

app = Flask(__name__)
app.secret_key = 'vaano'  # Set a secret key for sessions

db_config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'database': 'SMA'
}
# Create SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

# List of symbols for Yahoo Finance
yfinance_symbols = ['ibm', 'prft', 'nsci', 'ba', 'meta', 'nvda', 'tsla', 'aapl', 'amzn', 'intc']

def fetch_companies_from_db():
    conn = engine.connect()
    result = conn.execute(text('SELECT symbol, name FROM companies'))
    companies = {row[0].lower(): row[1] for row in result}
    conn.close()
    return companies

def delete_existing_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def fetch_and_save_data_yfinance(symbol, start_date, end_date):
    ticker = yf.Ticker(symbol.upper())
    historical_data = ticker.history(start=start_date, end=end_date, interval="1d")
    csv_filename = f"{symbol}_historical.csv"
    delete_existing_file(csv_filename)
    historical_data.to_csv(csv_filename)
    return csv_filename

def fetch_and_save_data_db(symbol):
    query = text(f"SELECT * FROM {symbol}")
    df = pd.read_sql(query, engine)
    if df.empty:
        raise ValueError(f"No data found for symbol {symbol} in the database.")
    csv_filename = f"{symbol}_historical.csv"
    delete_existing_file(csv_filename)
    df.to_csv(csv_filename, index=False)
    return csv_filename

def calculate_rsi(data, window=14):
    delta = data.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def save_plot_to_file(df, title, subtitle):
    plt.figure(figsize=(14, 10))
    plt.subplot(2, 1, 1)
    plt.plot(df.index, df['Open'], label='Open')
    plt.plot(df.index, df['Close'], label='Close')
    plt.plot(df.index, df['High'], label='High')
    plt.plot(df.index, df['Low'], label='Low')
    plt.title(title)
    plt.ylabel('Stock Price')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(df.index, df['RSI'], label='RSI', color='purple')
    plt.title(subtitle)
    plt.ylabel('RSI')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    
    # Save to file
    img_filename = f"{title.replace(' ', '_')}.png"
    plt.savefig(img_filename)
    plt.close()
    
    return img_filename

# Decorator to check role
def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if 'role' in session and session['role'] == role:
                return fn(*args, **kwargs)
            return jsonify({'message': f'Unauthorized access for role "{role}".'}), 403
        return decorated_view
    return wrapper

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if user and check_password_hash(user[2], password):  # user[2] is the password_hash column
        session['username'] = user[0]
        session['role'] = user[4]  # Assuming role is in the 5th column (index 4)
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/register', methods=['POST'])

def register():
    data = request.get_json()
    user_id = data.get('user_id')
    username = data.get('username')
    password = data.get('password')
    hashed_password = generate_password_hash(password)
    role = data.get('role')
    email = data.get('email')
    
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Users (user_id, username, password_hash, email, role) VALUES (%s, %s, %s, %s, %s)",
                       (user_id, username, hashed_password, email, role))
        connection.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Error as e:
        return jsonify({'message': f'Error: {e}'}), 500
    finally:
        cursor.close()
        connection.close()

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
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()

def execute_read_query(query, data=None):
    connection = create_connection()
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, data)
        result = cursor.fetchall()
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()
    return result

@app.route('/analyze_company', methods=['POST'])
@role_required(USER_ROLE)
def analyze_company():
    data = request.json
    symbol = data['symbol']
    company_name = data['company_name']
    start_date = data['start_date']
    end_date = data['end_date']
    
    if symbol in yfinance_symbols:
        csv_filename = fetch_and_save_data_yfinance(symbol, start_date, end_date)
    else:
        csv_filename = fetch_and_save_data_db(symbol)
    
    df = pd.read_csv(csv_filename)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.loc[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    
    if df.empty:
        return jsonify({"error": "No data available for the given date range."}), 404
    
    df.set_index('Date', inplace=True)
    df['RSI'] = calculate_rsi(df['Close'])
    
    img_filename = save_plot_to_file(df, f"{company_name} Stock", f"{company_name} RSI")
    
    return jsonify({"image_url": f"/images/{img_filename}"})

@app.route('/compare_companies', methods=['POST'])
@role_required(USER_ROLE)
def compare_companies():
    data = request.json
    symbol1 = data['symbol1']
    symbol2 = data['symbol2']
    start_date = data['start_date']
    end_date = data['end_date']
    
    if symbol1 in yfinance_symbols:
        file1 = fetch_and_save_data_yfinance(symbol1, start_date, end_date)
    else:
        file1 = fetch_and_save_data_db(symbol1)
    
    if symbol2 in yfinance_symbols:
        file2 = fetch_and_save_data_yfinance(symbol2, start_date, end_date)
    else:
        file2 = fetch_and_save_data_db(symbol2)
    
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df1['Date'] = pd.to_datetime(df1['Date'])
    df2['Date'] = pd.to_datetime(df2['Date'])
    df1.set_index('Date', inplace=True)
    df2.set_index('Date', inplace=True)
    
    df1 = df1.loc[(df1.index >= start_date) & (df1.index <= end_date)]
    df2 = df2.loc[(df2.index >= start_date) & (df2.index <= end_date)]
    
    if df1.empty or df2.empty:
        return jsonify({"error": "No data available for one or both symbols in the given date range."}), 404
    
    df1['RSI'] = calculate_rsi(df1['Close'])
    df2['RSI'] = calculate_rsi(df2['Close'])
    
    plt.figure(figsize=(14, 7))
    plt.plot(df1.index, df1['RSI'], label=f"{symbol1} RSI", color='blue')
    plt.plot(df2.index, df2['RSI'], label=f"{symbol2} RSI", color='orange')
    plt.title('RSI Comparison')
    plt.ylabel('RSI')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    img_filename = f"RSI_Comparison_{symbol1}_{symbol2}.png"
    plt.savefig(img_filename)
    plt.close()
    
    return jsonify({"image_url": f"/images/{img_filename}"})

# Compare Close Price

@app.route('/compare_close_prices', methods=['POST'])
@role_required(USER_ROLE)
def compare_close_prices():
    data = request.get_json()
    f1 = data.get('file1').split('_')[0]
    f2 = data.get('file2').split('_')[0]
    file1 = data['file1']
    file2 = data['file2']
    
    # Read CSV files into pandas DataFrames
    df1 = pd.read_csv(file1, parse_dates=['Date'], index_col='Date')
    df2 = pd.read_csv(file2, parse_dates=['Date'], index_col='Date')
    
    # Sort dataframes by Date (if not already sorted)
    df1 = df1.sort_index()
    df2 = df2.sort_index()
    
    # Plot daily Close prices
    plt.figure(figsize=(14, 7))
    plt.plot(df1.index, df1['Close'], label=f1, marker='o')
    plt.plot(df2.index, df2['Close'], label=f2, marker='o')
    
    plt.title('Daily Close Prices Comparison')
    plt.xlabel('Date')
    plt.ylabel('Close Price ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Format x-axis dates
    date_form = DateFormatter("%Y-%m-%d")
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.gcf().autofmt_xdate()
    
    # Save daily plot to a file
    daily_plot_filename = f'daily_close_prices_comparison_between_{f1}_{f2}.png'
    plt.savefig(f'images/{daily_plot_filename}')
    plt.close()
    
    # Resample to weekly data
    df1_weekly = df1.resample('W').mean()
    df2_weekly = df2.resample('W').mean()
    
    # Plot weekly Close prices
    plt.figure(figsize=(14, 7))
    plt.plot(df1_weekly.index, df1_weekly['Close'], label=f1, marker='o')
    plt.plot(df2_weekly.index, df2_weekly['Close'], label=f2, marker='o')
    
    plt.title('Weekly Close Prices Comparison')
    plt.xlabel('Date')
    plt.ylabel('Close Price ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.gcf().autofmt_xdate()
    
    # Save weekly plot to a file
    weekly_plot_filename = f"weekly_close_prices_comparison_between_{f1}_{f2}.png"
    plt.savefig(f'images/{weekly_plot_filename}')
    plt.close()
    
    return jsonify({
        'daily_plot_url': f'/images/{daily_plot_filename}',
        'weekly_plot_url': f'/images/{weekly_plot_filename}'
    })

# Compare Open Price

@app.route('/compare_open_prices', methods=['POST'])
@role_required(USER_ROLE)
def compare_open_prices():
    data = request.get_json()
    f1 = data.get('file1').split('_')[0]
    f2 = data.get('file2').split('_')[0]
    file1 = data['file1']
    file2 = data['file2']
    
    # Read CSV files into pandas DataFrames
    df1 = pd.read_csv(file1, parse_dates=['Date'], index_col='Date')
    df2 = pd.read_csv(file2, parse_dates=['Date'], index_col='Date')
    
    # Sort dataframes by Date (if not already sorted)
    df1 = df1.sort_index()
    df2 = df2.sort_index()
    
    # Plot daily Open prices
    plt.figure(figsize=(14, 7))
    plt.plot(df1.index, df1['Open'], label=f1, marker='o')
    plt.plot(df2.index, df2['Open'], label=f2, marker='o')
    
    plt.title('Daily Open Prices Comparison')
    plt.xlabel('Date')
    plt.ylabel('Open Price ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Format x-axis dates
    date_form = DateFormatter("%Y-%m-%d")
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.gcf().autofmt_xdate()
    
    # Save daily plot to a file
    daily_plot_filename = f'daily_close_prices_comparison_between_{f1}_{f2}.png'
    plt.savefig(f'images/{daily_plot_filename}')
    plt.close()
    
    # Resample to weekly data
    df1_weekly = df1.resample('W').mean()
    df2_weekly = df2.resample('W').mean()
    
    # Plot weekly Open prices
    plt.figure(figsize=(14, 7))
    plt.plot(df1_weekly.index, df1_weekly['Open'], label=f1, marker='o')
    plt.plot(df2_weekly.index, df2_weekly['Open'], label=f2, marker='o')
    
    plt.title('Weekly Open Prices Comparison')
    plt.xlabel('Date')
    plt.ylabel('Open Price ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.gcf().autofmt_xdate()
    
    # Save weekly plot to a file
    weekly_plot_filename = f"weekly_close_prices_comparison_between_{f1}_{f2}.png"
    plt.savefig(f'images/{weekly_plot_filename}')
    plt.close()
    
    return jsonify({
        'daily_plot_url': f'/images/{daily_plot_filename}',
        'weekly_plot_url': f'/images/{weekly_plot_filename}'
    })

# Compare High Price

@app.route('/compare_high_prices', methods=['POST'])
@role_required(USER_ROLE)
def compare_high_prices():
    data = request.get_json()
    f1 = data.get('file1').split('_')[0]
    f2 = data.get('file2').split('_')[0]
    file1 = data['file1']
    file2 = data['file2']
    
    # Read CSV files into pandas DataFrames
    df1 = pd.read_csv(file1, parse_dates=['Date'], index_col='Date')
    df2 = pd.read_csv(file2, parse_dates=['Date'], index_col='Date')
    
    # Sort dataframes by Date (if not already sorted)
    df1 = df1.sort_index()
    df2 = df2.sort_index()
    
    # Plot daily High prices
    plt.figure(figsize=(14, 7))
    plt.plot(df1.index, df1['High'], label=f1, marker='o')
    plt.plot(df2.index, df2['High'], label=f2, marker='o')
    
    plt.title('Daily High Prices Comparison')
    plt.xlabel('Date')
    plt.ylabel('High Price ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Format x-axis dates
    date_form = DateFormatter("%Y-%m-%d")
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.gcf().autofmt_xdate()
    
    # Save daily plot to a file
    daily_plot_filename = f'daily_close_prices_comparison_between_{f1}_{f2}.png'
    plt.savefig(f'images/{daily_plot_filename}')
    plt.close()
    
    # Resample to weekly data
    df1_weekly = df1.resample('W').mean()
    df2_weekly = df2.resample('W').mean()
    
    # Plot weekly High prices
    plt.figure(figsize=(14, 7))
    plt.plot(df1_weekly.index, df1_weekly['High'], label=f1, marker='o')
    plt.plot(df2_weekly.index, df2_weekly['High'], label=f2, marker='o')
    
    plt.title('Weekly High Prices Comparison')
    plt.xlabel('Date')
    plt.ylabel('High Price ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.gcf().autofmt_xdate()
    
    # Save weekly plot to a file
    weekly_plot_filename = f"weekly_close_prices_comparison_between_{f1}_{f2}.png"
    plt.savefig(f'images/{weekly_plot_filename}')
    plt.close()
    
    return jsonify({
        'daily_plot_url': f'/images/{daily_plot_filename}',
        'weekly_plot_url': f'/images/{weekly_plot_filename}'
    })

#Compare Low Pricess

@app.route('/compare_low_prices', methods=['POST'])
@role_required(USER_ROLE)
def compare_low_prices():
    data = request.get_json()
    f1 = data.get('file1').split('_')[0]
    f2 = data.get('file2').split('_')[0]
    file1 = data['file1']
    file2 = data['file2']
    
    # Read CSV files into pandas DataFrames
    df1 = pd.read_csv(file1, parse_dates=['Date'], index_col='Date')
    df2 = pd.read_csv(file2, parse_dates=['Date'], index_col='Date')
    
    # Sort dataframes by Date (if not already sorted)
    df1 = df1.sort_index()
    df2 = df2.sort_index()
    
    # Plot daily Low prices
    plt.figure(figsize=(14, 7))
    plt.plot(df1.index, df1['Low'], label=f1, marker='o')
    plt.plot(df2.index, df2['Low'], label=f2, marker='o')
    
    plt.title('Daily Low Prices Comparison')
    plt.xlabel('Date')
    plt.ylabel('Low Price ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Format x-axis dates
    date_form = DateFormatter("%Y-%m-%d")
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.gcf().autofmt_xdate()
    
    # Save daily plot to a file
    daily_plot_filename = f'daily_close_prices_comparison_between_{f1}_{f2}.png'
    plt.savefig(f'images/{daily_plot_filename}')
    plt.close()
    
    # Resample to weekly data
    df1_weekly = df1.resample('W').mean()
    df2_weekly = df2.resample('W').mean()
    
    # Plot weekly Low prices
    plt.figure(figsize=(14, 7))
    plt.plot(df1_weekly.index, df1_weekly['Low'], label=f1, marker='o')
    plt.plot(df2_weekly.index, df2_weekly['Low'], label=f2, marker='o')
    
    plt.title('Weekly Low Prices Comparison')
    plt.xlabel('Date')
    plt.ylabel('Low Price ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.gcf().autofmt_xdate()
    
    # Save weekly plot to a file
    weekly_plot_filename = f"weekly_close_prices_comparison_between_{f1}_{f2}.png"
    plt.savefig(f'images/{weekly_plot_filename}')
    plt.close()
    
    return jsonify({
        'daily_plot_url': f'/images/{daily_plot_filename}',
        'weekly_plot_url': f'/images/{weekly_plot_filename}'
    })


@app.route('/fetch_companies', methods=['GET'])
def fetch_companies():
    companies = fetch_companies_from_db()
    return jsonify(companies)

# Serve image files from the 'images' directory
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)


# COMPANY USER MODULE CODES:

# Ensure companies table exists

create_companies_table_query = """
CREATE TABLE IF NOT EXISTS companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    symbol VARCHAR(10) NOT NULL UNIQUE
)"""
execute_query(create_companies_table_query)


#Creates data  for a company

@app.route('/create_data', methods=['POST'])
@role_required(COMPANY_ROLE)
def create_data():
    data = request.get_json()
    company_name = data.get('companyName')
    company_symbol = data.get('companySymbol')
    
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
    execute_query(create_table_query)
    
    insert_company_query = """
    INSERT INTO companies (name, symbol) VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE name = VALUES(name)
    """
    execute_query(insert_company_query, (company_name, company_symbol))
    
    insert_data_query = f"""
    INSERT INTO {company_symbol} (date, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    for entry in data.get('data', []):
        execute_query(insert_data_query, (entry['Date'], entry['open'], entry['high'], entry['low'], entry['close'], entry['volume']))
    
    return jsonify({"message": "Data inserted successfully"}), 201


#updates company data based on symbol

@app.route('/update_data/<company_symbol>', methods=['PUT'])
@role_required(COMPANY_ROLE)
def update_data(company_symbol):
    data = request.get_json()
    date = data.get('Date')
    update_fields = ", ".join([f"{key} = %s" for key in data if key != 'Date'])
    update_query = f"""
    UPDATE {company_symbol}
    SET {update_fields}
    WHERE date = %s
    """
    update_values = tuple(data[key] for key in data if key != 'Date') + (date,)
    execute_query(update_query, update_values)
    
    return jsonify({"message": "Data updated successfully"}), 200


# Delete company specific data when date is passed and if not passed deletes whole company record

@app.route('/delete_data/<company_symbol>', methods=['DELETE'])
@role_required(COMPANY_ROLE)
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

#Gets company data based on symbol list  
@app.route('/get_data/<company_symbol>', methods=['GET'])
@role_required(COMPANY_ROLE)
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
     # Ensure the 'images' directory exists
    if not os.path.exists('images'):
        os.makedirs('images')

    app.run(debug=True)
