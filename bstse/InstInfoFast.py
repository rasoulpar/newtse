import urllib3
import csv

class InstInfoFast():

    def __init__(self, i = None, c = 27):
        self.__url__ = 'http://www.tsetmc.com/tsev2/data/instinfofast.aspx?i={}&c={}+'
        self.i = i
        self.c = c
        self.path = './data/'

    def _get_inst_info_fast_url(self):
        url = self.__url__
        url = url.format(self.i, self.c)
        return url
        # self.priceHitoryUrl =
    
    def get_inst_info_fast(self, i = None):
        if i == None:
            if self.i == None:
                raise Exception('i should be provided. This parameter is mandatory for scrapping bstse.')
        else:
            self.i = i

        url = self._get_inst_info_fast_url()

        http = urllib3.PoolManager()

        req = http.request('GET', url)

        data = str(req.data.decode('ascii')).split(';')
        print(data[1])
        
    def parse_market_data(m_data = None):
        if m_data == None:
            raise Exception('Please provide me some data')
        market_data = {
            'tpx':  None
        }
    
    def save_to_file(self, data = None, path = './data/'):
        self.path = self.path if self.path != None else path
        path_to_file = self.path + 'ph_{}.csv'.format(self.i)
        with open(path_to_file, 'w') as csv_file:
            csv_file.write(data)
