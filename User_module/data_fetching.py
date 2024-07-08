# data_fetching.py
import os
import yfinance as yf

def delete_existing_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def fetch_and_save_data(symbol):
    ticker = yf.Ticker(symbol.upper())
    historical_data = ticker.history(start="2024-06-05", end="2024-07-05", interval="1d")
    csv_filename = f"{symbol}_historical.csv"
    
    # Delete the existing file if it exists
    delete_existing_file(csv_filename)
    
    # Save the new data to CSV
    historical_data.to_csv(csv_filename)
    
    return csv_filename
