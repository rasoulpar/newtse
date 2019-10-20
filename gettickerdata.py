import pandas as pd
import matplotlib.pyplot as plt
import asyncio
from pyppeteer import launch
import persian
import csv
from tabulate import tabulate
import math

ticker = ''
async def main():
    browser = await launch()
    page = await browser.newPage()
    tickers = read_to_dict('./tickers.csv')

    tickers_list = ['فولاد']
    days = 5 * 365

    for i in range(0, len(tickers_list)):
        ticker = tickers_list[i]
        if ticker in tickers:
            url = 'http://members.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i=' + tickers[ticker] + '&Top=' + str(days) + '&A=1'
        else:
            continue

    await page.goto(url)
    priceHistory = await page.querySelectorEval('body', 'el => el.innerText.split(";").map(el => { let eel = el.split("@"); return eel; })')

    df = pd.DataFrame(priceHistory, columns=['Date', 'High', 'Low', 'Close', 'Last', 'First', 'Open', 'TradesValue', 'Volume', 'TradesCount'])
    df = df.sort_values(by='Date', ascending=True)

    df['Close'] = df.Close.astype(float)
    df.index = df.Date
    df['returns'] = (df.Close / df.Close.shift(1)) - 1

    df = df.dropna()
    
    hist_me(df)

    df.sort_values('returns', inplace=True, ascending=True)

    VaR_90 = df['returns'].quantile(0.1) * 100
    VaR_95 = df['returns'].quantile(0.05) * 100
    VaR_99 = df['returns'].quantile(0.01) * 100

    print(tabulate([['90%', VaR_90], ['95%', VaR_95], ['99%', VaR_99]], ('Confidence Level', 'Value at Risk %')))

    await browser.close()


def tickers_list():
    tickers_list = read_to_dict('./tickers_list.csv')

def read_to_dict(path_to_file):
    with open(path_to_file, newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        return dict(reader)

def hist_me(df):
    plt.hist(df.returns, bins=40)
    plt.xlabel('Retruns')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()



asyncio.get_event_loop().run_until_complete(main())