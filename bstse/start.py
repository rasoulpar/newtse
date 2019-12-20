import PriceHistory as ph
import InstInfoFast as iif
import TickersList as tl

i = 46348559193224090

tickersL = ph.PriceHistory(i=i)
print(tickersL.get_price_history())
