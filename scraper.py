import requests
from bs4 import BeautifulSoup

income_statement={}

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
url="https://finance.yahoo.com/quote/AAPL/financials?p=AAPL"

page = requests.get(url=url,headers=headers)
soup = BeautifulSoup(page.content,"html.parser")

table = soup.findAll("div",{"class":"M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})


for t in table:
    rows = t.findAll("div", {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
    for row in rows:
        income_statement[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1]

print(income_statement)


