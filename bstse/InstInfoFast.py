import urllib3
import csv

class InstInfoFast():

    def __init__(self, i = None, c = 27):
        self.__url__ = 'http://www.tsetmc.com/tsev2/data/instinfofast.aspx?i={}&c={}+'
        self.i = i
        self.c = c
        self.path = './data/'
        self.data = None

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

        self.data = str(req.data.decode('ascii')).split(';')
        
        return self._parse_data()
    
    # parse request data
    # all information is inputed and parsed
    # an object argument should be implemented for data stracture parameters
    def _parse_data(self):
        if self.data is None:
            raise Exception('There is no InstInfoFast data available')
        # ticker's current prices status
        current_price_info = str(self.data[0]).split('@')[0].split(',')
        # qoutes for both buy and sell sides of ticker
        current_three_first_qoutes = str(self.data[2]).split('@')
        # legual and individual buyy/sell counts and percentage
        current_legal_personal_info = str(self.data[4]).split(',')

        current_price_info = self._parse_current_price(current_price_info)

        current_three_first_qoutes = self._parse_current_three_first_qoutes(current_three_first_qoutes)

        current_legal_personal_info = self._parse_current_price(current_legal_personal_info)

        return {
            'current_price_info': current_price_info,
            'current_three_firs_qoutes': current_three_first_qoutes,
            'current_legal_personal_info': current_legal_personal_info
        }

    def _parse_current_three_first_qoutes(self, current_three_first_qoutes = None):
        if current_three_first_qoutes is None:
            raise Exception('You have to provide some current three first qoutes.')
        if self.__is_iterable(current_three_first_qoutes) is False:
            raise Exception('current three first qoutes is not iterable')
        dict_current_three_first_qoutes = {
            # dict of price info
            # to be implemented
        }
        return dict_current_three_first_qoutes
    
    def _parse_current_legal_personal_info(self, current_legal_personal_info = None):
        if current_legal_personal_info is None:
            raise Exception('You have to provide some current legal personal info.')
        if self.__is_iterable(current_legal_personal_info) is False:
            raise Exception('current legal personal info is not iterable')
        dict_current_legal_personal_info = {
            # dict of price info
            # to be implemented
        }
        return dict_current_legal_personal_info
    
    def _parse_current_price(self, current_price_info = None):
        if current_price_info is None:
            raise Exception('You have to provide some current price info.')
        if self.__is_iterable(current_price_info) is False:
            raise Exception('current price info is not iterable')
        dict_current_price = {
            'Last_trade_time': current_price_info[0],
            'A': current_price_info[1]
        }
        return dict_current_price
        
    
    def __is_iterable(self, obj):
        try:
            iter(obj)
            return True
        except TypeError:
            return False
        
    def parse_market_data(self, m_data = None):
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
