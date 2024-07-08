import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("aapl_historical.csv")

df['Date'] = pd.to_datetime(df['Date'])

df = df.loc[df['Date'] > '2023-10-10']

df.set_index('Date', inplace=True)

# plt.gca().set_facecolor('#f5f5f5')

plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Open'], label='Open')
plt.plot(df.index, df['Close'], label='Close')
plt.plot(df.index, df['High'], label='High')
plt.plot(df.index, df['Low'], label='Low')

plt.title("Apple Stock")
plt.ylabel('Stock Price')
plt.xlabel('Date')

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()
