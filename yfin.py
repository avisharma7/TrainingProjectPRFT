import yfinance as yf

# aapl= yf.Ticker("prft")
# aapl_historical = aapl.history(start="2024-06-05", end="2024-07-05", interval="1d", actions = False)
# print(aapl_historical)

data = yf.download("AMZN GOOG", start="2024-06-05", end="2024-07-05", group_by='tickers', actions = False)
print(data)