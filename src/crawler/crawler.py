import sys
import pandas
import requests
from loguru import logger


class extract_history():

    endpoint = "https://www.nasdaq.com/api/v1/historical/{stock}/stocks"
    period = "/2017-01-01/2019-12-31"

    def __init__(self, data="data/_nasdaq_list.csv"):

        stock_df = pandas.read_csv(data, sep="|", usecols=["Symbol"])
        self.stock_list = stock_df["Symbol"]

    def save_history(self):

        # Estract history with specified stock code list,
        # notify if return data too less and mark as no data,
        # then finally save into data pool
        for s in self.stock_list[0:10]:

            url = extract_history.endpoint.format(stock=s.upper())
            try:
                req = requests.get(url + extract_history.period, timeout=3)
                req.raise_for_status()
            except requests.exceptions.Timeout:
                logger.error("[Extract] " + s + " timeout")
                continue
            except requests.exceptions.TooManyRedirects:
                logger.error("[Extract] " + s + " too Many redirect")
                continue
            except requests.exceptions.RequestException as err:
                logger.error("[Extract] " + s + err)
                sys.exit(1)

            data = req.content.decode("utf-8")
            data = data.replace("$", "").replace("N/A", "0")

            if len(data) < 1000:
                logger.warning("[Extract] " + s + " no data")
                continue

            with open("data/stocks/" + s + "_3Y.csv", "w") as wf:
                wf.write(data)
                logger.debug("[Extract] " + s + " success")
                wf.close()


extract = extract_history()
extract.save_history()
