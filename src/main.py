from crawler.stock_holder import stock_holder
from crawler.stock_filter import stock_filter


holder = stock_holder()
filter = stock_filter(holder.get_hold()[:10])
filter.filter_growth("trailingPE", 1.1, 1)
# filter.filter_interval("forwardPE", 1, 15)
print(filter.get_stock())
