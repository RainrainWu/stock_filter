import sys
import requests
from loguru import logger

ENDPOINT = "https://www.nasdaq.com/api/v1/historical/{stock}/stocks"
PERIOD = "/2017-01-01/2019-12-31"


def extract(stocks):

    # Estract history with specified stock code list,
    # notify if return data too less and mark as no data,
    # then finally save into data pool
    for s in stocks:

        url = ENDPOINT.format(stock=s.upper())
        try:
            req = requests.get(url + PERIOD, timeout=3)
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

        with open("data/stocks/history/" + s + "_3Y.csv", "w") as wf:
            wf.write(data)
            logger.debug("[Extract] " + s + " success")
            wf.close()
