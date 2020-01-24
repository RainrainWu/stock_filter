import csv


class stock_load():

    def __init__(self, stocks):

        self.stock_hold = stocks

    def load_csv(self, direct="data/stock_hold.csv"):

        with open(direct, 'w', newline='') as wf:
            wr = csv.writer(wf, quoting=csv.QUOTE_ALL)
            wr.writerow(self.stock_hold)
