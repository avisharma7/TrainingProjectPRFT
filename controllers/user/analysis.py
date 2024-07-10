# analysis.py
import pandas as pd
from flask import request, jsonify
import matplotlib.pyplot as plt
from controllers.user.data_fetching import fetch_and_save_data_db, fetch_and_save_data_yfinance, calculate_rsi

yfinance_symbols = ['ibm', 'prft', 'nsci', 'ba', 'meta', 'nvda', 'tsla', 'aapl', 'amzn', 'intc']

def analyze_company(symbol, company_name, is_yfinance):
    if is_yfinance:
        csv_filename = fetch_and_save_data_yfinance(symbol)
    else:
        csv_filename = fetch_and_save_data_db(symbol)

    df = pd.read_csv(csv_filename)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter data if required
    data = request.get_json()
    
    st = data.get('start_date')
    ed = data.get('end_date')
    df = df.loc[(df['Date'] >= st) & (df['Date'] <= ed)]
    
    if df.empty:
        print(f"No data available for the date range {st} to {ed}.")
        return
    
    df.set_index('Date', inplace=True)

    # Calculate RSI
    df['RSI'] = calculate_rsi(df['Close'])

    plt.figure(figsize=(14, 10))

    plt.subplot(2, 1, 1)
    plt.plot(df.index, df['Open'], label='Open')
    plt.plot(df.index, df['Close'], label='Close')
    plt.plot(df.index, df['High'], label='High')
    plt.plot(df.index, df['Low'], label='Low')
    plt.title(f"{company_name} Stock")
    plt.ylabel('Stock Price')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(df.index, df['RSI'], label='RSI', color='purple')
    plt.title(f"{company_name} RSI")
    plt.ylabel('RSI')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def compare_companies(symbol1, symbol2, companies):
    # Fetch data from Yahoo Finance or Database
    if symbol1 in yfinance_symbols:
        file1 = fetch_and_save_data_yfinance(symbol1)
    else:
        file1 = fetch_and_save_data_db(symbol1)
    
    if symbol2 in yfinance_symbols:
        file2 = fetch_and_save_data_yfinance(symbol2)
    else:
        file2 = fetch_and_save_data_db(symbol2)

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Convert 'Date' to datetime
    df1['Date'] = pd.to_datetime(df1['Date'])
    df2['Date'] = pd.to_datetime(df2['Date'])

    # Set 'Date' as the index
    df1.set_index('Date', inplace=True)
    df2.set_index('Date', inplace=True)

    data = request.get_json()
    
    st = data.get('start_date')
    ed = data.get('end_date')

    # Filter data based on user input date range
    df1 = df1.loc[(df1.index >= st) & (df1.index <= ed)]
    df2 = df2.loc[(df2.index >= st) & (df2.index <= ed)]

    if df1.empty:
        print(f"No data available for {symbol1} in the date range {st} to {ed}.")
        return

    if df2.empty:
        print(f"No data available for {symbol2} in the date range {st} to {ed}.")
        return

    # Calculate RSI
    df1['RSI'] = calculate_rsi(df1['Close'])
    df2['RSI'] = calculate_rsi(df2['Close'])

    plt.figure(figsize=(14, 7))

    plt.subplot(2, 1, 1)
    plt.plot(df1.index, df1['RSI'], label=f"{companies.get(symbol1, symbol1.upper())} RSI", color='blue')
    plt.plot(df2.index, df2['RSI'], label=f"{companies.get(symbol2, symbol2.upper())} RSI", color='orange')
    plt.title('RSI Comparison')
    plt.ylabel('RSI')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()