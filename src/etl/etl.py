import etl_stock
import etl_eps

stocks = etl_stock.get_nasdaq_list()[:50]
metrix = etl_eps.extract(stocks)
etl_eps.load(metrix)
