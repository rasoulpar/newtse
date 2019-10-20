import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import yfinance as yf
from tabulate import tabulate

df = pd.DataFrame()

df = yf.download('FB', '2012-01-01', '2018-01-15')

df['returns'] = (df.Close.shift(-5) / df.Close) - 1

df = df.dropna()

plt.hist(df.returns, bins=40)
plt.xlabel('Retruns')
plt.ylabel('Frequency')
plt.grid(True)

plt.show()

df.sort_values('returns', inplace=True, ascending=True)

VaR_90 = df['returns'].quantile(0.1)
VaR_95 = df['returns'].quantile(0.05)
VaR_99 = df['returns'].quantile(0.01)

print(tabulate([['90%', VaR_90], ['95%', VaR_95], ['99%', VaR_99]], ('Confidence Level', 'Value at Risk')))


