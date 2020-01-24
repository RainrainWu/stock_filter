import csv

LOAD_DIR = "data/stocks/eps/eps_6Y.csv"


class eps_load():

    def __init__(self):
        pass

    @staticmethod
    def load_csv(metrix, direct=LOAD_DIR):

        with open(direct, 'w', newline='') as wf:
            wr = csv.writer(wf, delimiter=',', quoting=csv.QUOTE_ALL)
            wr.writerows(metrix)
