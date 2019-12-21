import PriceHistory as ph
import InstInfoFast as iif
import TickersList as tl

i = 46348559193224090

tickersL = iif.InstInfoFast(i=i)

tickersL.get_inst_info_fast()
