import requests
from bs4 import BeautifulSoup
import pandas as pd

tickers = ["AAPL","CSCO","INFY.NS"]

income_statement_dict = {}
balance_sheet_dict = {}
cashflow_dict = {}

financial_urls_map={}

financial_urls_map["income_statement"] = "https://finance.yahoo.com/quote/{}/financials?p={}"
financial_urls_map["balance_sheet"] = "https://finance.yahoo.com/quote/{}/balance-sheet?p={}"
financial_urls_map["cash_flow"] = "https://finance.yahoo.com/quote/{}/cash-flow?p={}"


headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

def scrape_financials(ticker,statement_type):
    url = financial_urls_map[statement_type].format(ticker,ticker)
    page = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.findAll("div", {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    income_statement = {}
    table_title = {}
    for t in table:
        headings = t.find_all("div",{"class":"D(tbr) C($primaryColor)"})
        for top_row in headings:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
        rows = t.findAll("div", {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            income_statement[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]
    return table_title,income_statement

def cleanup_columns_to_numeric(table):
    for col in table.columns:
        table[col] = table[col].str.replace('\W', '', regex=True)
        table[col] = pd.to_numeric(table[col])
    return table

#Income statement
for ticker in tickers:
    table_title,income_statement = scrape_financials(ticker,"income_statement")
    temp = pd.DataFrame(income_statement).T
    temp.columns = table_title["Breakdown"]
    income_statement_dict[ticker] = cleanup_columns_to_numeric(temp)

#Balance Sheet
for ticker in tickers:
    table_title,income_statement = scrape_financials(ticker,"balance_sheet")
    temp = pd.DataFrame(income_statement).T
    temp.columns = table_title["Breakdown"]
    balance_sheet_dict[ticker] = cleanup_columns_to_numeric(temp)

#Cash flow
for ticker in tickers:
    table_title,income_statement = scrape_financials(ticker,"cash_flow")
    temp = pd.DataFrame(income_statement).T
    temp.columns = table_title["Breakdown"]
    cashflow_dict[ticker] = cleanup_columns_to_numeric(temp)

print(income_statement_dict)
print(balance_sheet_dict)
print(cashflow_dict)







