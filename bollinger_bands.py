import yfinance as yf
import pandas as pd

tickers = ["AMZN","GOOG","MSFT"]

ohlcv_dataset = {}

for ticker in tickers:
    ohlcv_data = yf.download(ticker,period="1mo",interval="15m")
    ohlcv_data.dropna(how="any",inplace=True)
    ohlcv_dataset[ticker] = ohlcv_data


def calculate_bollinger_bands(dataset,period=14,std_deviaton=2):
    _dataset = dataset.copy()
    _dataset['MB'] = _dataset["Adj Close"].rolling(period).mean()
    _dataset['UB'] =_dataset['MB'] + 2*_dataset["Adj Close"].rolling(period).std(ddof=0)
    _dataset['LB'] = _dataset['MB'] - 2*_dataset["Adj Close"].rolling(period).std(ddof=0)
    _dataset["BB_WIDTH"] = _dataset["UB"]-_dataset["LB"]
    return _dataset[["MB","UB","LB","BB_WIDTH"]]

for ticker in ohlcv_dataset:
    ohlcv_dataset[ticker][["MB","UB","LB","BB_WIDTH"]] = calculate_bollinger_bands( ohlcv_dataset[ticker])