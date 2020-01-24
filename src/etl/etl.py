from stocks.extract import stock_extract
from eps.extract import eps_extract
from eps.load import eps_load

stocks = stock_extract.extract_all()
metrix = eps_extract.extract(stocks)
eps_load.load_csv(metrix)
