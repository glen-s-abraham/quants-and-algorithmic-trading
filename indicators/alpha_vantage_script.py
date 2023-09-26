#https://github.com/RomelTorres/alpha_vantage

key_path="/home/glen/projects/alphavantage_fin_api_1.txt"

from alpha_vantage.timeseries import TimeSeries
import pandas as pd

def pull_data(symbol):
    ts = TimeSeries(key=open(key_path, 'r').read(), output_format='pandas')
    data = ts.get_daily(symbol=symbol, outputsize='full')[0]
    data.columns = ["open", "high", "low", "close", "volume"]
    return  data

data = pull_data("MSFT")
print(data)



