import pandas


class stock_holder():

    def __init__(self):

        self.stock_hold = []
        self.load_all()

    def get_hold(self):

        return self.stock_hold

    def load_all(self, data="data/_nasdaq_list.csv"):

        stock_df = pandas.read_csv(data, sep="|", usecols=["Symbol"])
        self.stock_hold = stock_df["Symbol"].values.tolist()[:-1]

    def apply_ONeil(self):
        pass
