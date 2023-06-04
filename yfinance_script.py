import datetime

import pandas as pd
import yfinance as yf

stocks=["AMZN","MSFT","INTC","GOOG","INFY.NS"]

#subtract offset from todays date
start=datetime.datetime.today()-datetime.timedelta(30)
end = datetime.date.today()
cl_price = pd.DataFrame()
ohlcv_data={}


for ticker in stocks:
    cl_price[ticker] = yf.download(ticker,start,end)["Adj Close"]
for ticker in stocks:
    ohlcv_data[ticker] = yf.download(ticker, start, end)


print(ohlcv_data)

