import pandas

EXTRACT_PATH = "data/_nasdaq_list.csv"


def extract(path=EXTRACT_PATH):

    stock_df = pandas.read_csv(path, sep="|", usecols=["Symbol"])
    stock_hold = stock_df["Symbol"].values.tolist()[:-1]
    return stock_hold
