# analysis.py
import pandas as pd
import matplotlib.pyplot as plt
from controllers.user.data_fetching import fetch_and_save_data

def analyze_company(symbol, company_name):
    csv_filename = fetch_and_save_data(symbol)

    df = pd.read_csv(csv_filename)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.loc[df['Date'] > '2023-10-10']
    df.set_index('Date', inplace=True)

    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Open'], label='Open')
    plt.plot(df.index, df['Close'], label='Close')
    plt.plot(df.index, df['High'], label='High')
    plt.plot(df.index, df['Low'], label='Low')

    plt.title(f"{company_name} Stock")
    plt.ylabel('Stock Price')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def compare_companies(symbol1, symbol2, companies):
    file1 = fetch_and_save_data(symbol1)
    file2 = fetch_and_save_data(symbol2)

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    df1['Date'] = pd.to_datetime(df1['Date'])
    df2['Date'] = pd.to_datetime(df2['Date'])

    df1.set_index('Date', inplace=True)
    df2.set_index('Date', inplace=True)

    merged_df = df1.merge(df2, on='Date', suffixes=('_company1', '_company2'))

    merged_df['Open_diff'] = merged_df['Open_company1'] - merged_df['Open_company2']
    merged_df['Close_diff'] = merged_df['Close_company1'] - merged_df['Close_company2']
    merged_df['High_diff'] = merged_df['High_company1'] - merged_df['High_company2']
    merged_df['Low_diff'] = merged_df['Low_company1'] - merged_df['Low_company2']

    plt.figure(figsize=(14, 7))

    plt.subplot(2, 2, 1)
    plt.plot(merged_df.index, merged_df['Open_diff'], label='Open Difference')
    plt.title('Open Price Difference')
    plt.xlabel('Date')
    plt.ylabel('Difference')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(merged_df.index, merged_df['Close_diff'], label='Close Difference')
    plt.title('Close Price Difference')
    plt.xlabel('Date')
    plt.ylabel('Difference')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(merged_df.index, merged_df['High_diff'], label='High Difference')
    plt.title('High Price Difference')
    plt.xlabel('Date')
    plt.ylabel('Difference')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(merged_df.index, merged_df['Low_diff'], label='Low Difference')
    plt.title('Low Price Difference')
    plt.xlabel('Date')
    plt.ylabel('Difference')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
