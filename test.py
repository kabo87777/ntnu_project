# coding=UTF-8
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

    ###指數平均線
    # stock_df["EMA12"] = talib.EMA(np.array(close),timeperiod=6)
    # stock_df["EMA26"] = talib.EMA(np.array(close),timeperiod=12)

    ###MACD
    stock_df["MACD"],stock_df["MACDsignal"],stock_df["MACDhist"] = talib.MACD(np.array(close),fastperiod = 6,slowperiod = 12,signalperiod = 9)
    
    ###KD值
    stock_df['k'], stock_df['d'] = talib.STOCH(stock_df['High'], stock_df['Low'], stock_df['close'],fastk_period = 9)

    ### 布林
    stock_df['upperband'],stock_df['middleband'],stock_df['lowerband']= talib.BBANDS(stock_df['close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

    
    ##print(stock_df)

    mc = mpf.make_marketcolors(up='r',down='g', edge='', wick='inherit',volume='inherit')

    s = mpf.make_mpf_style(gridaxis='both',gridstyle='-.',y_on_right=True,marketcolors=mc,edgecolor='white',figcolor='white',facecolor='black', gridcolor='gray')
    ##reference :https://blog.csdn.net/weixin_48964486/article/details/116229333



    index  = [
            mpf.make_addplot(stock_df[['upperband','lowerband']],color = 'cyan',width=1),
            mpf.make_addplot(stock_df['middleband'],color='y',width=1),
        
        
            mpf.make_addplot(stock_df["MACD"], panel = 2,type='bar', ylabel = 'MACD', color = 'red'),
            mpf.make_addplot(RSI(stock_df, 14), panel = 3, ylabel = 'RSI', color = 'lime',width=1),
            mpf.make_addplot(stock_df["k"], panel = 4, ylabel = 'KD', color = 'cyan',width=1),
            mpf.make_addplot(stock_df["d"], panel = 4,  color = 'orange',width=1)
            ]

    ##畫圖
    mpf.plot(stock_df,type='candle',  title = stock_num ,style = s, mav=(5,10,20), addplot = index,volume=True)  ## mav = MA
else:
    print("wrong number")