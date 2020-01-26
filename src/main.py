from etl import etl_stock
from stock.stock_holder import stock_holder


stocks = etl_stock.get_nasdaq_list()

# Peter Lynch
peter_lynch = stock_holder(stocks[:50])
peter_lynch.filter_eps_trend(0.8, 1.2, 2).filter_pb_ratio(0, 1.5)
print(peter_lynch.get_hold())
