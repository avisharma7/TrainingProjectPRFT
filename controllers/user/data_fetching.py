from flask import request, jsonify
import os
import yfinance as yf
import pandas as pd
from data.conn import db_config
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Create the SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

def delete_existing_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def fetch_and_save_data_yfinance(symbol):
    try:
        data = request.get_json()
        
        st = data.get('start_date')
        ed = data.get('end_date')
        ticker = yf.Ticker(symbol.upper())
        historical_data = ticker.history(start=st, end=ed, interval="1d")
        csv_filename = f"{symbol}_historical.csv"
        
        # Delete the existing file if it exists
        delete_existing_file(csv_filename)
        
        # Save the new data to CSV
        historical_data.to_csv(csv_filename)
        
        return csv_filename
    except Exception as e:
        return jsonify({'error': f"Failed to fetch data from Yahoo Finance: {e}"}), 500

def fetch_and_save_data_db(symbol):
    try:
        query = text(f"SELECT * FROM {symbol}")
        df = pd.read_sql(query, engine)
        
        if df.empty:
            raise ValueError(f"No data found for symbol {symbol} in the database.")
        
        csv_filename = f"{symbol}_historical.csv"
        
        # Delete the existing file if it exists
        delete_existing_file(csv_filename)
        
        # Save the new data to CSV
        df.to_csv(csv_filename, index=False)
        
        return csv_filename
    except SQLAlchemyError as e:
        return jsonify({'error': f"Database error: {e}"}), 500
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        return jsonify({'error': f"Failed to fetch data from the database: {e}"}), 500

def calculate_rsi(data, window=14):
    try:
        delta = data.diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    except Exception as e:
        return jsonify({'error': f"Failed to calculate RSI: {e}"}), 500

