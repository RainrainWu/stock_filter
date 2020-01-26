import requests
import pandas
from loguru import logger

EXTRACT_PATH = "data/stocks/list/{e}.csv"

EXTRACT_ENDPOINT = (
    "https://old.nasdaq.com/screening/companies-by-name.aspx"
    "?letter=0&exchange={e}&render=download"
)


def __extract_exchange(exchange):

    try:
        req = requests.get(EXTRACT_ENDPOINT.format(e=exchange))
        req.raise_for_status()
    except requests.exceptions.Timeout:
        tpl = "[Extract] {e} stock list timeout"
        logger.error(tpl.format(e=exchange))
        return
    except requests.exceptions.TooManyRedirects:
        tpl = "[Extract] {e} stock list too Many redirect"
        logger.error(tpl.format(e=exchange))
        return
    except requests.exceptions.RequestException:
        tpl = "[Extract] {e} stock list error"
        logger.error(tpl.format(e=exchange))
        return

    data = req.content.decode("utf-8")
    if len(data) < 1000:
        tpl = "[Extract] {e} stock list no data"
        logger.error(tpl.format(e=exchange))
        return

    with open(EXTRACT_PATH.format(e=exchange), "w") as wf:
        wf.write(data)
        tpl = "[EXTRACT] {e} stock list success"
        logger.debug(tpl.format(e=exchange))
        wf.close()

    return


def extract():
    __extract_exchange("nasdaq")
    __extract_exchange("amex")
    __extract_exchange("nyse")


def __get_list(exchange):
    path = EXTRACT_PATH.format(e=exchange)
    stock_df = pandas.read_csv(path, sep=",", usecols=["Symbol"])
    stock_hold = stock_df["Symbol"].values.tolist()
    return stock_hold


def get_nasdaq_list():
    return __get_list("nasdaq")


def get_amex_list():
    return __get_list("amex")


def get_nyse_list():
    return __get_list("nyse")
