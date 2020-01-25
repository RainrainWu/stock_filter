import etl_stock
import etl_eps
import etl_history

stocks = etl_stock.extract()[:50]
# etl_history.extract(stocks)
metrix = etl_eps.extract(stocks)
etl_eps.load(metrix)
