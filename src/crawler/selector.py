import pandas
import requests
import json
from loguru import logger


class select_stock():

    endpoint = "https://query1.finance.yahoo.com/v7/finance/options/{stock}"

    def __init__(self, data="data/_nasdaq_list.csv"):

        stock_df = pandas.read_csv(data, sep="|", usecols=["Symbol"])
        self.stock_list = stock_df["Symbol"]
        self.stock_hold = self.stock_list[:]

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

    def filter(self, index, mode, threshold):

        # Scrape metrix from yahoo finance api, then extract index
        # with customize rule.
        new_hold = []
        for s in self.stock_hold[0:20]:

            req = requests.get(select_stock.endpoint.format(stock=s.upper()))
            data = json.loads(req.text)
            metrix = data["optionChain"]["result"][0]["quote"]

            try:
                value = metrix[index]
            except KeyError:
                logger.warning("[Metrix] " + s + index + " key not found")
                continue

            if (select_stock.compare(mode, value, threshold)):
                logger.debug("[Select] " + s + " selected")
                new_hold += [s]
            else:
                logger.debug("[Select] " + s + " deprecated")

        self.stock_hold = new_hold
        return self


selector = select_stock()
selector.filter("forwardPE", "le", 15)
print(selector.stock_hold)
