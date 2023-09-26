import requests
from bs4 import BeautifulSoup
import pandas as pd

#extract simple tables
url = "https://www.xe.com/currencycharts/"
tables = pd.read_html(url)


def scrape_valuations(ticker):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    url = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(ticker, ticker)
    page = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.findAll("table", {"class": "W(100%) Bdcl(c)"})
    temp_stats={}
    for _t in table:
        rows = _t.findAll("tr")
        for _row in rows:
            temp_stats[_row.getText(separator="|").split("|")[0]]=_row.getText(separator="|").split("|")[-1]
    return temp_stats;


vals=scrape_valuations("AAPL")
print(vals)



