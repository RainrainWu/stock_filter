import requests
import json
import datetime
from loguru import logger


class stock_filter():

    endpoint = "https://query1.finance.yahoo.com/v7/finance/options/{stock_id}"

    def __init__(self, stocks):

        self.stock_hold = stocks

    def get_stock(self):

        return self.stock_hold

    @staticmethod
    def compare(mode, value, threshold):

        if (mode == "gt"):
            return value > threshold
        elif (mode == "ge"):
            return value >= threshold
        elif (mode == "lt"):
            return value < threshold
        elif (mode == "le"):
            return value <= threshold
        else:
            logger.error("[Compare] " + mode + " mode undefined.")
            return False

    @staticmethod
    def backtrace_timestamp(day=0):

        curr = datetime.date.today()
        date = datetime.datetime(curr.year, curr.month, curr.day, 0, 0)
        bias = datetime.timedelta(days=day)
        date -= bias
        timestamp = str(int(date.timestamp()))
        return timestamp

    def filter_growth(self, index, magnification, years=1):

        # Scrape metrix from yahoo finance api, then compare index
        # with last year
        for stock in self.stock_hold:

            index_list = []
            url_base = stock_filter.endpoint.format(stock_id=stock.upper())
            for year in range(years + 1):

                timestamp = stock_filter.backtrace_timestamp(year * 365)
                url = url_base + "?date=" + timestamp
                logger.info(url)
                req = requests.get(url)
                data = json.loads(req.text)
                metrix = data["optionChain"]["result"][0]["quote"]

                try:
                    value = metrix[index]
                    index_list += [value]
                except KeyError:
                    template = "[Metrix] {s} {i} key not found"
                    logger.warning(template.format(s=stock, i=index))
                    continue

            logger.info(index_list)
            if (len(index_list) == 0):
                continue

            compare_list = []
            for i in range(years):

                compare = (index_list[i] / index_list[i+1]) > magnification
                compare_list += [compare]

            logger.info(compare_list)

    def filter_interval(self, index, lowerbound, upperbound):

        # Scrape metrix from yahoo finance api, then extract index
        # with customize rule.
        new_hold = []
        for stock in self.stock_hold:

            url = stock_filter.endpoint.format(stock_id=stock.upper())
            url += "?date=" + stock_filter.backtrace_timestamp()
            req = requests.get(url)
            data = json.loads(req.text)
            metrix = data["optionChain"]["result"][0]["quote"]

            try:
                value = metrix[index]
            except KeyError:
                template = "[Metrix] {s} {i} key not found"
                logger.warning(template.format(s=stock, i=index))
                continue

            if (stock_filter.compare("ge", value, lowerbound) and
                    stock_filter.compare("lt", value, upperbound)):
                template = "[Select] {s} {i} = {v}, selected"
                logger.debug(template.format(s=stock, i=index, v=value))
                new_hold += [stock]
            else:
                template = "[Select] {s} {i} = {v}, deprecated"
                logger.debug(template.format(s=stock, i=index, v=value))

        self.stock_hold = new_hold
        return self
