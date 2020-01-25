import csv
import re
from selenium import webdriver
from selenium.common import exceptions
from loguru import logger

EPS_URL = "https://www.nasdaq.com/market-activity/stocks/{s}/revenue-eps"
EPS_XPATH = (
    "/html/body/div[4]/div/main/div/div[4]/div[2]/div/div[1]/"
    "div/div[1]/table/tbody/tr[19]/td[{c}]"
)
COL_LIST = [1, 2, 3]
HEADER = ["STOCK", "2019", "2018", "2017"]
LOAD_PATH = "data/stocks/eps/eps.csv"


def extract(stocks):

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chrome_options=options)
    pattern = re.compile("[0-9]+[\.]*[0-9]*")
    eps_metrix = [HEADER]

    for stock in stocks:
        logger.debug(EPS_URL.format(s=stock.lower()))
        driver.get(EPS_URL.format(s=stock))
        eps_stock = [stock]

        for col in COL_LIST:
            xpath = EPS_XPATH.format(c=col)

            try:
                text = driver.find_element_by_xpath(xpath).text
                match = pattern.search(text)
                eps_stock += ["" if match is None else match.group(0)]
            except exceptions.NoSuchElementException:
                tpl = "[XPATH] {s} eps notfound"
                logger.warning(tpl.format(s=stock))
                eps_stock += [""]

        eps_metrix += [eps_stock]

    driver.close()
    return eps_metrix


def load(metrix, path=LOAD_PATH):

    with open(path, 'w', newline='') as wf:
        wr = csv.writer(wf, delimiter=',', quoting=csv.QUOTE_ALL)
        wr.writerows(metrix)
