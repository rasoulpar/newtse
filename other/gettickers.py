import pandas as pd
import asyncio
from pyppeteer import launch
import persian
import csv
#tblToGrid > tbody > tr:nth-child(2) > td:nth-child(7) > a
async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://www.tsetmc.com/Loader.aspx?ParTree=111C1417')
    numberOfRows = await page.evaluate('''() => {
        return document.getElementById("tblToGrid").rows.length;
    }''')

    tickersDict = {}

    for i in range(2, numberOfRows):
        selector = '#tblToGrid > tbody > tr:nth-child(' + str(i) +') > td:nth-child(7) > a'
        
        href = await page.querySelectorEval(selector, 'el => el.href')
        ticker = persian.convert_ar_characters(await page.querySelectorEval(selector, 'el => el.innerText'))
        if len(href.split('=')) == 3:
            inscode = href.split('=')[2]
            tickersDict.update({ticker: inscode})
    await browser.close()
    save_to_csv('./tickers.csv', tickersDict)

def save_to_csv(path_to_file, data_dict):
    with open(path_to_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data_dict.items():
            writer.writerow([key, value])

def read_to_dict(path_to_file):
    with open(path_to_file, newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        mydict = dict(reader)

asyncio.get_event_loop().run_until_complete(main())
