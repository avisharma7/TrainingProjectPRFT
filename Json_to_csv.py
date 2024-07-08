# import requests

# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey= 8WHQFD24UNWXFO0?datatype=csv'
# r = requests.get(url)
# data = r.json()

# print(data)

import requests
import csv

# API URL with parameters
url = 'https://www.alphavantage.co/query'
params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'IBM',
    'apikey': '8WHQFD24UNWXFO0',
    'datatype': 'csv'  # Specify datatype as CSV
}

# Send GET request to Alpha Vantage API
r = requests.get(url, params=params)

# Check if the request was successful
if r.status_code == 200:
    # Save response content to a file named 'ibm_stock_data.csv'
    with open('ibm_stock_data.csv', 'wb') as f:
        f.write(r.content)
    print("CSV file 'ibm_stock_data.csv' has been created successfully.")
else:
    print("Failed to fetch data:", r.status_code)