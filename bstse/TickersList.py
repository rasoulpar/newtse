import urllib3
import csv
import datetime

class TickersList():
    def __init__(self):
        self.__url = 'http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx?h=0&r=0'
        self.path = './data/tickers_list/'
    
    def get_tickers_list(self):
        http = urllib3.PoolManager()

        req = http.request('GET', self.__url)

        tickers_data = req.data.decode('utf-8').split('@')[2]
        
        tickers_data = tickers_data.replace('\n', '')
        
        tickets_list = tickers_data.split(';')

        ins_code = list()

        for t in tickets_list:
            ticker = t.split(',')
            dict_ticker = {
                'ins': ticker[0],
                'identity': ticker[1],
                'ticker': ticker[2],
                'ticker_full': ticker[3] 
            }
            ins_code.append(dict_ticker)
        
        return ins_code

    def save_to_file(self, path = './data/tickers_list/'):
        self.path = self.path if self.path != None else path
        path_to_file = self.path + 'tl_{}.csv'.format(str(datetime.datetime.now()).replace('-', '_').replace(' ', '__').replace(':', ''))
        csv_columns = ['ins', 'identity', 'ticker', 'ticker_full']
        with open(path_to_file, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writeheader()
            tickers_list = self.get_tickers_list()

            writer.writerows(tickers_list)

            # for ticker in tickers_list:
            #     writer.writerow(ticker)