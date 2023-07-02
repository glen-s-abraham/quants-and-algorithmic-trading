import yfinance as yf
import pandas as pd
import numpy as np

tickers = ["AMZN","GOOG","MSFT"]

ohlcv_dataset = {}

for ticker in tickers:
    ohlcv_data = yf.download(ticker,period="1mo",interval="5m")
    ohlcv_data.dropna(how="any",inplace=True)
    ohlcv_dataset[ticker] = ohlcv_data


def calculate_rsi(DF, n=14):
    df=DF.copy()
    df["change"]= df["Adj Close"] - df["Adj Close"].shift(1)
    df["gain"] = np.where(df["change"]>=0,df["change"],0)
    df["loss"] = np.where(df["change"]<0,-1*df["change"],0)
    df["avgGain"] = df["gain"].ewm(alpha=1/n,min_periods=n).mean()
    df["avgLoss"] = df["loss"].ewm(alpha=1/n,min_periods=n).mean()
    df["rs"] = df["avgGain"]/df["avgLoss"]
    df["rsi"] = 100-(100/(1+df["rs"]))
    return df["rsi"]
    
for ticker in tickers:
    ohlcv_dataset[ticker]["RSI"]=calculate_rsi(ohlcv_dataset[ticker])