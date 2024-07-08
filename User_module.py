import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# List of companies with symbols in lowercase
companies = {
    "ibm": "IBM",
    "prft": "Perficient, Inc.",
    "nsci": "NCS Multistage Holdings, Inc.",
    "ba": "The Boeing Company",
    "meta": "Meta Platforms, Inc.",
    "nvda": "NVIDIA Corporation",
    "tsla": "Tesla, Inc.",
    "aapl": "Apple Inc.",
    "amzn": "Amazon.com, Inc.",
    "intc": "Intel Corporation"
}

# Display the companies to the user
print("Please choose a company from the list below:")
for symbol, name in companies.items():
    print(f"{symbol}: {name}")

# Take the user's input
company_symbol = input("Enter the symbol of the company you want to choose: ").lower()

# Check if the input is valid
if company_symbol in companies:
    # Fetch the historical data for the chosen company
    ticker = yf.Ticker(company_symbol.upper())
    historical_data = ticker.history(start="2024-06-05", end="2024-07-05", interval="1d")

    # Save the data to a CSV file
    csv_filename = f"{company_symbol}_historical.csv"
    historical_data.to_csv(csv_filename)

    # Read the data back from the CSV file
    df = pd.read_csv(csv_filename)

    # Process the data for visualization
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.loc[df['Date'] > '2023-10-10']
    df.set_index('Date', inplace=True)

    # Plot the data
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Open'], label='Open')
    plt.plot(df.index, df['Close'], label='Close')
    plt.plot(df.index, df['High'], label='High')
    plt.plot(df.index, df['Low'], label='Low')

    plt.title(f"{companies[company_symbol]} Stock")
    plt.ylabel('Stock Price')
    plt.xlabel('Date')

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("Invalid company symbol. Please run the script again and choose a valid symbol.")
