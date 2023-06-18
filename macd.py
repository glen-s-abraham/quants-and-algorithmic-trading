import yfinance as yf
import pandas as pd

tickers = ["AMZN","GOOG","MSFT"]

ohlcv_dataset = {}

for ticker in tickers:
    ohlcv_data = yf.download(ticker,period="1mo",interval="15m")
    ohlcv_data.dropna(how="any",inplace=True)
    ohlcv_dataset[ticker] = ohlcv_data

#MACD formula
#MACD line:(12-day Exp Moving Avg - 26-day Exp Moving Avg)
#Signal line: 9-day EXp Moving Avg of MACD line
#MACD histogram: MACD line - Signal Line

def calculate_macd(ohlcv_data,fast_moving_avg_period=12,slow_moving_avg_period=26,signal_moving_avg_period=9):
    _ohlcv_data = ohlcv_data.copy()
    _ohlcv_data["fast_moving_avg"] = _ohlcv_data["Adj Close"].ewm(span=fast_moving_avg_period,min_periods=fast_moving_avg_period).mean()
    _ohlcv_data["slow_moving_avg"] = _ohlcv_data["Adj Close"].ewm(span=slow_moving_avg_period,min_periods=slow_moving_avg_period).mean()
    _ohlcv_data["MACD"] = _ohlcv_data["fast_moving_avg"] - _ohlcv_data["slow_moving_avg"]
    _ohlcv_data["signal"] = _ohlcv_data["MACD"].ewm(span=signal_moving_avg_period,min_periods=signal_moving_avg_period).mean()
    return _ohlcv_data.loc[:,["MACD","signal"]]

for ticker in ohlcv_dataset:
    ohlcv_dataset[ticker][["MACD","SIGNAL"]] = calculate_macd( ohlcv_dataset[ticker])