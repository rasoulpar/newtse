import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import asyncio
from pyppeteer import launch
import persian
import csv
import scipy as scipy
from persiantools.jdatetime import JalaliDate

ticker = ''
async def main():
    browser = await launch()
    page = await browser.newPage()
    tickers = read_to_dict('./tickers.csv')

    tickers_list = ['پاسا']
    days = 20

    for i in range(0, len(tickers_list)):
        ticker = tickers_list[i]
        if ticker in tickers:
            url = 'http://members.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i=' + tickers[ticker] + '&Top=' + str(days) + '&A=1'
        else:
            continue

    await page.goto(url)
    priceHistory = await page.querySelectorEval('body', 'el => el.innerText.split(";").map(el => { let eel = el.split("@"); return eel; })')
    df = pd.DataFrame(priceHistory, columns=['Date', 'High', 'Low', 'Close', 'Last', 'First', 'Open', 'TradesValue', 'Volume', 'TradesCount'])

    df['Close'] = df.Close.astype(float)
    df.drop(df.tail(1).index,inplace=True)
    # print(df)
    df['Date'] = df['Date'].str[:4] + '-' + df['Date'].str[4:6] + '-' + df['Date'].str[6:8]
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['ts'] = df.Date.values.astype(np.int64) // 10 ** 9
    df['JDate'] = df.Date.map(lambda x: JalaliDate.to_jalali(x.year, x.month, x.day))
    df.index = df['Date']
    del df['Date']
    
    save_to_csv('./' + tickers_list[0] + '.csv', df.to_dict())
    

    # print(df.assign(temp_c=lambda x: ((x['Date'][0]))).head())

    df = df.sort_values(by='Date', ascending=True)
    
    df['returns'] = (df.Close / df.Close.shift(1)) - 1

    df = df.dropna()
    
    # hist_me(df)

    await browser.close()


def tickers_list():
    tickers_list = read_to_dict('./tickers_list.csv')

def read_to_dict(path_to_file):
    with open(path_to_file, newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        return dict(reader)

def save_to_csv(path_to_file, data_dict):
    with open(path_to_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data_dict.items():
            writer.writerow([key, value])

def hist_me(df):
    plt.hist(df.returns, bins=40)
    plt.xlabel('Retruns')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()



asyncio.get_event_loop().run_until_complete(main())