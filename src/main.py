from etl import etl_stock
from stock.stock_holder import stock_holder


stocks = etl_stock.extract()[:100]
holder = stock_holder(stocks)
holder.filter_trailing_pe(3, 15).filter_peg_ratio(0, 1)
print(holder.get_hold())
