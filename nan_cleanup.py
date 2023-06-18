import  datetime as dt
import yfinance as yf
import pandas as pd

stocks = ["AMZN","MSFT","FB","GOOG"]
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()

cl_price = pd.DataFrame()


for ticker in stocks:
    cl_price[ticker] = yf.download(ticker,start,end)["Adj Close"]

# cl_price.fillna({"FB":0,"GOOG":1})
# cl_price.fillna(0)
cl_price=cl_price.dropna(axis=1,how='any')

# print(cl_price.mean())
# print(cl_price.std())
# print(cl_price.median())
# print(cl_price.describe())
# print(cl_price.head(5))
# print(cl_price.tail(5))

#returns
daily_returns = cl_price.pct_change() #calc daily returns
#daily_returns = cl_price/cl_price.shift(1)-1 #daily returns = cur day/prev day

print("################## daily returns ################")
print(daily_returns)

#perform operations on daily returns always

print(daily_returns.mean())
print(daily_returns.std()) #check how volatile is the daily returns with respect to the mean.

#rolling mean aka moving average

print('################# rolling ######################')
##rolling() groups data to apply a rolling operation
print(daily_returns.rolling(window=10).mean()) #simple moving average

print('################# exponential ######################')
#Exponential whighted functions
print(daily_returns.ewm(com=10).mean())

cl_price.plot(subplots=True,layout=(2,2))
daily_returns.plot(subplots=True,layout=(2,2))

(1+daily_returns).cumprod().plot()
