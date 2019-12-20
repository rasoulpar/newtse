import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import yfinance as yf
from tabulate import tabulate
import sys
import math

def phi(x):
    return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)

#-----------------------------------------------------------------------

# Return the value of the Gaussian probability function with mean mu
# and standard deviation sigma at the given x value.

def pdf(x, mu=0.0, sigma=1.0):
    return phi((x - mu) / sigma) / sigma

#-----------------------------------------------------------------------

# Return the value of the cumulative Gaussian distribution function
# with mean 0.0 and standard deviation 1.0 at the given z value.

def Phi(z):
    if z < -8.0: return 0.0
    if z >  8.0: return 1.0
    total = 0.0
    term = z
    i = 3
    while total != total + term:
        total += term
        term *= z * z / float(i)
        i += 2
    return 0.5 + total * phi(z)

#-----------------------------------------------------------------------

# Return standard Gaussian cdf with mean mu and stddev sigma.
# Use Taylor approximation.

def cdf(z, mu=0.0, sigma=1.0):
    return Phi((z - mu) / sigma)

#-----------------------------------------------------------------------

# Black-Scholes formula.

def callPrice(s, x, r, sigma, t):
    a = (math.log(s/x) + (r + sigma * sigma/2.0) * t) / \
        (sigma * math.sqrt(t))
    b = a - sigma * math.sqrt(t)
    return s * cdf(a) - x * math.exp(-r * t) * cdf(b)

df = pd.DataFrame()

# df = yf.download('FB', '2018-01-01', '2018-01-15')
df = yf.download('FB',period='5y')

df['returns'] = (df.Close.shift(-5) / df.Close) - 1
print(np.std(df.returns))
df = df.dropna()

# plt.hist(df.returns, bins=40)
# plt.xlabel('Retruns')
# plt.ylabel('Frequency')
# plt.grid(True)

# plt.show()

df.sort_values('returns', inplace=False, ascending=True)

print(callPrice(186.16, 210.00, 0.05, 0.038, 0.25))

VaR_90 = df['returns'].quantile(0.1)
x = 186.15 * (1 + VaR_90)
c_90 = callPrice(x, 200, 0.05, 0.038, 0.25)

VaR_95 = df['returns'].quantile(0.05)
x = 186.15 * (1 + VaR_95)
c_95 = callPrice(x, 200, 0.05, 0.038, 0.25)

VaR_99 = df['returns'].quantile(0.01)
x = 186.15 * (1 + VaR_99)
c_99 = callPrice(x, 200, 0.05, 0.038, 0.25)

print(tabulate([['90%', VaR_90, c_90 * 100], ['95%', VaR_95, c_95 * 100], ['99%', VaR_99, c_99 * 100]], ('Confidence Level', 'Value at Risk (%)', 'VaR')))


