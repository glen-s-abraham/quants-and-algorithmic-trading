import yfinance as yf
import pandas as pd

tickers = ["AMZN","GOOG","MSFT"]

ohlcv_dataset = {}

for ticker in tickers:
    ohlcv_data = yf.download(ticker,period="1mo",interval="5m")
    ohlcv_data.dropna(how="any",inplace=True)
    ohlcv_dataset[ticker] = ohlcv_data

#true_range = max[(high-low),abs(high-previous_close),abs(low-previous_close)]
#atr = exp(true_range)
def calculate_atr(DF, n=14):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = abs(df["High"] - df["Adj Close"].shift(1))
    df["L-PC"] = abs(df["Low"] - df["Adj Close"].shift(1))
    df["TR"] = df[["H-L","H-PC","L-PC"]].max(axis=1, skipna=False)
    df["ATR"] = df["TR"].ewm(com=n, min_periods=n).mean()
    return df["ATR"]
    
for ticker in tickers:
    ohlcv_dataset[ticker]["ATR"]=calculate_atr(ohlcv_dataset[ticker])