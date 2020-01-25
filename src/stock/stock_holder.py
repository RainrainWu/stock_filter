from stock import stock_filter


class stock_holder():

    def __init__(self, stocks):

        self.stock_hold = stocks

    def get_hold(self):

        return self.stock_hold

    def apply_ONeil(self):

        stocks = stock_filter.filter_eps_trend(self.stock_hold, 1.0, 2)
        self.stock_hold = stocks
