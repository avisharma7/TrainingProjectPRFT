# data_fetching.py
import os
import yfinance as yf

def delete_existing_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def fetch_and_save_data(symbol):
    st = input("Enter the start date in (YYYY-MM-DD) format: ")
    ed = input("Enter the end date in (YYYY-MM-DD) format: ")
    int = input("Enter the interval (Day=1d) , (Week=1w), (Month=1mo): ")
    ticker = yf.Ticker(symbol.upper())
    historical_data = ticker.history(start=st, end=ed, interval=int)
    csv_filename = f"{symbol}_historical.csv"
    
    # Delete the existing file if it exists
    delete_existing_file(csv_filename)
    
    # Save the new data to CSV
    historical_data.to_csv(csv_filename)
    
    return csv_filename
