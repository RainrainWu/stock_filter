import requests
import json
import pandas
from loguru import logger

EPS_FILE_PATH = "data/stocks/eps/eps.csv"
QUOTE_ENDPOINT = (
    "https://query1.finance.yahoo.com/v6/finance/quote"
    "?symbols={stock_id}"
)
STATISTIC_ENDPOINT = (
    "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{stock_id}"
    "?modules=defaultKeyStatistics"
)


def filter_quote(stocks, key, lowerbound, upperbound):

    hold = []
    for stock in stocks:

        url = QUOTE_ENDPOINT.format(stock_id=stock.upper())
        req = requests.get(url)
        data = json.loads(req.text)
        metrix = data["quoteResponse"]["result"][0]

        try:
            value = metrix[key]
        except TypeError:
            tpl = "[FILTER] {s} no quote data"
            logger.warning(tpl.format(s=stock))
            continue
        except KeyError:
            tpl = "[FILTER] {s} no {k} data"
            logger.warning(tpl.format(s=stock, k=key))
            continue

        if value >= lowerbound and value < upperbound:
            template = "[FILTER] {s} {k} {v}, selected"
            logger.debug(template.format(s=stock, k=key, v=value))
            hold += [stock]
        else:
            template = "[FILTER] {s} {k} {v}, deprecated"
            logger.debug(template.format(s=stock, k=key, v=value))

    return hold


def filter_statistic(stocks, key, lowerbound, upperbound):

    hold = []
    for stock in stocks:

        url = STATISTIC_ENDPOINT.format(stock_id=stock.upper())
        req = requests.get(url)
        data = json.loads(req.text)
        result = data["quoteSummary"]["result"]

        try:
            statistic = result[0]["defaultKeyStatistics"]
            value = statistic[key]["fmt"][:-1]
            if value[-1] == "%":
                value = value[:-1]
            value = float(value)
        except TypeError:
            tpl = "[FILTER] {s} no statistic data"
            logger.warning(tpl.format(s=stock))
            continue
        except KeyError:
            tpl = "[FILTER] {s} no {k} data"
            logger.warning(tpl.format(s=stock, k=key))
            continue

        if value >= lowerbound and value < upperbound:
            template = "[FILTER] {s} {k} {v}, selected"
            logger.debug(template.format(s=stock, k=key, v=value))
            hold += [stock]
        else:
            template = "[FILTER] {s} {k} {v}, deprecated"
            logger.debug(template.format(s=stock, k=key, v=value))

    return hold


def filter_eps_trend(stocks, lowerbound, upperbound, years=1):

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
            ratios += [(mul >= lowerbound and mul < upperbound)]

        if all(ratios):
            tpl = "[FILTER] [EPS] {s} {r}, selected"
            logger.debug(tpl.format(s=stock, r=" ".join(eps_sum)))
            new_hold += [stock]
        else:
            tpl = "[FILTER] [EPS] {s} {r}, deprecated"
            logger.debug(tpl.format(s=stock, r=" ".join(eps_sum)))

    return new_hold
