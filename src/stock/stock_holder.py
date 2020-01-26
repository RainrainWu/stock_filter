import math
from stock import stock_filter


class stock_holder():

    def __init__(self, stocks):
        self.stock_hold = stocks

    def get_hold(self):
        return self.stock_hold

    def filter_pb_ratio(self, lowerbound, upperbound):
        self.stock_hold = stock_filter.filter_quote(
            self.stock_hold, "priceToBook", lowerbound, upperbound
        )
        return self

    def filter_trailing_pe(self, lowerbound, upperbound):
        self.stock_hold = stock_filter.filter_quote(
            self.stock_hold, "trailingPE", lowerbound, upperbound
        )
        return self

    def filter_peg_ratio(self, lowerbound, upperbound):
        self.stock_hold = stock_filter.filter_statistic(
            self.stock_hold, "pegRatio", lowerbound, upperbound
        )
        return self

    def filter_trailing_eps(self, lowerbound):
        self.stock_hold = stock_filter.filter_statistic(
            self.stock_hold, "trailingEps", lowerbound, math.inf
        )
        return self

    def filter_profit_margin(self, lowerbound):
        self.stock_hold = stock_filter.filter_statistic(
            self.stock_hold, "profitMargins", lowerbound, math.inf
        )
        return self

    def filter_institution_held(self, lowerbound, upperbound):
        self.stock_hold = stock_filter.filter_statistic(
            self.stock_hold, "heldPercentInstitutions", lowerbound, upperbound
        )
        return self

    def filter_eps_trend(self, lowerbound, upperbound, years):
        self.stock_hold = stock_filter.filter_eps_trend(
            self.stock_hold, lowerbound, upperbound, years
        )
        return self
