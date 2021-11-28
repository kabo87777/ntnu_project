import mplfinance as mpf
import pandas_datareader as pdr
import datetime as datetime
start = datetime.datetime(2021,9,28)
df_2330 = pdr.DataReader('2330.TW', 'yahoo', start=start)
df_2330.index.name = 'Date'
mpf.plot(df_2330,type='candle', mav=(5,10,20),volume=True)