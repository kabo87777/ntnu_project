import mplfinance as mpf
import pandas_datareader as pdr
import datetime as datetime
from talib import abstract
import talib
import numpy as np
import pandas as pd

def RSI(df, period):
    return abstract.RSI(df, timeperiod=period)

stock_num = str(input("輸入股票代碼:"))

start = datetime.datetime(2021,9,28)
stock_df = pdr.DataReader(stock_num+'.TW', 'yahoo', start=start)
if(stock_df is not None):
    stock_df["close"] = stock_df["Close"]
    close = [float(x) for x in stock_df["close"]]
    stock_df["EMA12"] = talib.EMA(np.array(close),timeperiod=6)
    stock_df["EMA26"] = talib.EMA(np.array(close),timeperiod=12)
    stock_df["MACD"],stock_df["MACDsignal"],stock_df["MACDhist"] = talib.MACD(np.array(close),fastperiod = 6,slowperiod = 12,signalperiod = 9)
    stock_df['k'], stock_df['d'] = talib.STOCH(stock_df['High'], stock_df['Low'], stock_df['close'],fastk_period = 9)
    #print(stock_df)
    mc = mpf.make_marketcolors(up='r',down='g',volume='in')
    s  = mpf.make_mpf_style(marketcolors=mc)
    index  = [mpf.make_addplot(stock_df["MACD"], panel = 2,type='bar', ylabel = 'MACD', color = 'red'),
              mpf.make_addplot(RSI(stock_df, 14), panel = 3, ylabel = 'RSI', color = 'lime'),
              mpf.make_addplot(stock_df["k"], panel = 4, ylabel = 'KD', color = 'yellow'),
              mpf.make_addplot(stock_df["d"], panel = 4,  color = 'blue')
            ]
    mpf.plot(stock_df,type='candle', style = s, mav=(5,10,20), addplot = index,volume=True)
else:
    print("wrong number")