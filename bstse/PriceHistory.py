import urllib3
import csv

class PriceHistory():

    def __init__(self, i = None, top = 999999, a = 0):
        self.__url__ = 'http://members.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i={}&Top={}&A={}'
        self.i = i
        self.top = top
        self.a = a
        self.path = './data/'

    def _get_price_history_url(self):
        url = self.__url__
        url = url.format(self.i, self.top, self.a)
        return url
        # self.priceHitoryUrl =
    
    def get_price_history(self, i = None):
        if i == None:
            if self.i == None:
                raise Exception('i should be provided. This parameter is mandatory for scrapping bstse.')
        else:
            self.i = i

        url = self._get_price_history_url()

        http = urllib3.PoolManager()

        req = http.request('GET', url)

        self.save_to_file(data=req.data.decode('ascii').replace('@', ',').replace(';', '\n'))
    
    # def normalize(self, old = list('@', ';'), new = list(',', '\n')):
    #     pass
    
    def save_to_file(self, data = None, path = './data/'):
        self.path = self.path if self.path != None else path
        path_to_file = self.path + 'ph_{}.csv'.format(self.i)
        with open(path_to_file, 'w') as csv_file:
            csv_file.write(data)
