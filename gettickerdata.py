import pandas as pd
import numpy as np
from datetime import datetime as dt
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
    del df['Date'], df['ts']
    
    is_bet = is_between_cond([1398, 7, 25], [1398, 8, 3], df)
    print(df[is_bet])
    # save_to_csv('./' + tickers_list[0] + '.csv', df.to_dict())

    df = df.sort_values(by='Date', ascending=True)
    
    df['returns'] = (df.Close / df.Close.shift(1)) - 1

    df = df.dropna()
    
    # hist_me(df)

    await browser.close()

# accepts tow list of jalali dates, year, month and day
def is_between_cond(j_start, j_end, df):
    start = jalali_to_datetime64(j_start[0], j_start[1], j_start[2])
    end = jalali_to_datetime64(j_end[0], j_end[1], j_end[2])
    type(True)
    type(False)
    between_booleans = []
    for day in df.index:
        if day >= start and day < end:
            between_booleans.append(True)
        else:
            between_booleans.append(False)
    
    is_between = pd.Series(between_booleans)

    return is_between
    
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

# year, month, day
def jalali_to_datetime64(j_year=1368, j_month=7, j_day=25):
    return np.datetime64(JalaliDate(j_year, j_month, j_day).to_gregorian())
    


asyncio.get_event_loop().run_until_complete(main())