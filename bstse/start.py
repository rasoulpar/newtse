import PriceHistory as ph
import TickersList as tl
import InstInfoFast as iif

i = 46348559193224090

tickersL = iif.InstInfoFast(i=i)

tickersL.get_inst_info_fast()
