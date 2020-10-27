import pandas as pd
import matplotlib.pyplot as plt

from enum import Enum  

Adjusted = Enum('Adjusted', 'true false')
Interval = Enum('Interval', '_1min _5min _15min _30min _60min')
OutputSize = Enum('outputsize', 'compact full')
DataType = Enum('datatype', 'json csv')

def Slice(year, month):
    return 'year{}month{}'.format(year, month) 

def GetInterval(interval):
    return interval.name[1:] 
 
key = '7YVKV6R8YWNYE83E'
apiUrl = 'https://www.alphavantage.co/query'

def Time_Series_Intraday_Extended(symbol,interval,slice,adjusted,key):
    url = '{}?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={}&interval={}&slice={}&adjusted={}&apikey={}'
    fileName = 'data/download/{}-{}-{}.csv'.format(symbol,GetInterval(interval), slice)

    data = pd.read_csv(url.format(apiUrl, symbol, GetInterval(interval), slice, adjusted, key))
    data.to_csv(fileName)  
    print(fileName)

for symbol in ['IBM','AAPL']:
    for year in range(1,3):
        for month in range(1,13):
            Time_Series_Intraday_Extended(symbol, Interval._60min, Slice(year,month), Adjusted.false, key)