import requests
import json
import datetime
import pandas
from loguru import logger

EPS_FILE_PATH = "data/stocks/eps/eps.csv"
ENDPOINT = "https://query1.finance.yahoo.com/v7/finance/options/{stock_id}"


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


def backtrace_timestamp(day=0):

    curr = datetime.date.today()
    date = datetime.datetime(curr.year, curr.month, curr.day, 0, 0)
    bias = datetime.timedelta(days=day)
    date -= bias
    timestamp = str(int(date.timestamp()))
    return timestamp


def filter_eps_trend(stocks, magnification, years=1):

    # with pre-load eps historical data to pick up high-growth
    # stock
    eps_df = pandas.read_csv(EPS_FILE_PATH)
    new_hold = []

    for stock in stocks:
        eps = eps_df.loc[eps_df['STOCK'] == stock.upper()]
        if len(eps) == 0:
            tpl = "[FILTER] {s} eps data not found"
            logger.warning(tpl.format(s=stock))
            continue

        eps_sum = [str(eps.values.tolist()[0][i]) for i in range(1, 4)]
        if years > len(eps_sum) - 1 or years < 1:
            logger.error("[FILTER] Years specified invalid!")
        if eps_sum[0] == "":
            tpl = "[FILTER] {s} eps sum is none"
            logger.warning(tpl.format(s=stock))

        ratios = []
        for i in range(years):
            mul = float(eps_sum[i]) / float(eps_sum[i+1])
            ratios += [mul >= magnification]

        if all(ratios):
            tpl = "[FILTER] [EPS] {s} {r}, selected"
            logger.debug(tpl.format(s=stock, r=" ".join(eps_sum)))
            new_hold += [stock]
        else:
            tpl = "[FILTER] [EPS] {s} {r}, deprecated"
            logger.debug(tpl.format(s=stock, r=" ".join(eps_sum)))

    return new_hold


def filter_index_interval(self, index, lowerbound, upperbound):

    # Scrape metrix from yahoo finance api, then extract index
    # with customize rule.
    new_hold = []
    for stock in self.stock_hold:

        url = ENDPOINT.format(stock_id=stock.upper())
        url += "?date=" + backtrace_timestamp()
        req = requests.get(url)
        data = json.loads(req.text)
        metrix = data["optionChain"]["result"][0]["quote"]

        try:
            value = metrix[index]
        except KeyError:
            template = "[Metrix] {s} {i} key not found"
            logger.warning(template.format(s=stock, i=index))
            continue

        if (compare("ge", value, lowerbound) and
                compare("lt", value, upperbound)):
            template = "[Select] {s} {i} = {v}, selected"
            logger.debug(template.format(s=stock, i=index, v=value))
            new_hold += [stock]
        else:
            template = "[Select] {s} {i} = {v}, deprecated"
            logger.debug(template.format(s=stock, i=index, v=value))

    self.stock_hold = new_hold
    return self
