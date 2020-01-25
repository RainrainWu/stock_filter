from etl import etl_stock
from stock.stock_holder import stock_holder


stocks = etl_stock.extract()[:50]
holder = stock_holder(stocks)
holder.apply_ONeil()
print(holder.get_hold())
