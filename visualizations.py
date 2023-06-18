import  datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

stocks = ["AMZN","MSFT","FB","GOOG"]
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()

cl_price = pd.DataFrame()


for ticker in stocks:
    cl_price[ticker] = yf.download(ticker,start,end)["Adj Close"]
    
cl_price.dropna(axis=1,how='any',inplace=True)

daily_returns = cl_price.pct_change()

fig,ax = plt.subplots()

ax.set(title='Mean returns',xlabel="stocks",ylabel='Mean returns')
plt.bar(x=daily_returns.columns,height=daily_returns.mean())
plt.bar(x=daily_returns.columns,height=daily_returns.std())