import matplotlib.pyplot as plt
import seaborn as sea
import numpy as np
import pandas as pd

df = pd.read_csv("ibm_stock_data.csv")
# print(df.head())

df['timestamp'] =pd.to_datetime(df['timestamp'],errors='ignore') 
df.loc[df['timestamp'] > '10/10/2023' ]
df.set_index('timestamp', inplace = True)

plt.figure(figsize=(14,7))
plt.plot(df['timestamp'], df['high'], label = 'high')

plt.title("IBM Stock")
plt.ylabel('high')
plt.xlabel('Date')
plt.legend()

plt.show()
