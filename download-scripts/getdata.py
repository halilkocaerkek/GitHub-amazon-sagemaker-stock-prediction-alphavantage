from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

from pprint import pprint
import matplotlib.pyplot as plt

key='7YVKV6R8YWNYE83E'

ts = TimeSeries(key,output_format='pandas')

def get_data(stock):
    data, meta_data = ts.get_intraday(symbol=stock,interval='1min', outputsize='full')

    data['4. close'].plot()
    plt.title('Intraday Times Series for the {} stock (1 min)'.format(stock))
    plt.show()

    data['Mnemonic']=stock
    data['ISIN']=''
    data['SecurityDesc']=''
    data['SecurityType']='Common stock'
    data['Currency']=''
    data['SecurityID']=''
   # data['Time']=data['date'].time()
    data['NumberOfTrades'] = 1
    data=data.rename(columns={"1. open": "StartPrice", "2. high": "MaxPrice", "3. low":"MinPrice","4. close":"EndPrice", "5. volume":"TradedVolume"})
    
    #print(data.head())
    for i in data.index:
        data.at[i, 'Time'] =  i.time()
        data.at[i, 'Date'] =  i.date()

    print('{} : {}'.format(stock, data.shape))
    #print(data.head())
    data.to_csv('data/download/{}.csv'.format(stock))  

def get_bands(stock):
    ti = TechIndicators(key=key, output_format='pandas')
    data, meta_data = ti.get_bbands(symbol=stock, interval='1min', time_period=60)
    data.plot()
    plt.title('BBbands indicator for  {} stock (60 min)'.format(stock))
    plt.show()
    print('{} : {}'.format(stock, data.shape))
    print(data.head())
    print(data.tail())

get_bands('IBM')
#get_data('MSFT')
#get_data('IBM')
#get_data('AMZN')
#get_data('AAPL')