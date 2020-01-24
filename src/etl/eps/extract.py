from selenium import webdriver
from selenium.common import exceptions
from loguru import logger

EPS_URL = "https://www.nasdaq.com/market-activity/stocks/{s}/revenue-eps"
EPS_XPATH = (
    "/html/body/div[4]/div/main/div/div[4]/div[2]/div/div[1]/"
    "div/div[1]/table/tbody/tr[{r}]/td[{c}]"
)
COL_LIST = [1, 2, 3]
ROW_LIST = [7, 11, 15, 3, 19]
MONTH_LIST = ["MAR", "JUN", "SEP", "DEC", "SUM"]
YEAR_LIST = ["2019", "2018", "2017"]


class eps_extract():

    def __init__(self):
        pass

    @staticmethod
    def extract(stocks):

        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(chrome_options=options)
        header = [x + "_" + y for x in YEAR_LIST for y in MONTH_LIST]
        eps_metrix = [["STOCK"] + header]

        for stock in stocks:
            logger.debug(EPS_URL.format(s=stock.lower()))
            driver.get(EPS_URL.format(s=stock))
            eps_stock = [stock]

            for col in COL_LIST:
                for row in ROW_LIST:
                    xpath = EPS_XPATH.format(r=row, c=col)

                    try:
                        text = driver.find_element_by_xpath(xpath).text
                        eps_stock += [text]
                    except exceptions.NoSuchElementException:
                        tpl = "[XPATH] {s} eps notfound"
                        logger.warning(tpl.format(s=stock))
                        eps_stock += [""]

            eps_metrix += [eps_stock]

        driver.close()
        return eps_metrix
