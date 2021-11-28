import mplfinance as mpf
import pandas_datareader as pdr
import datetime as datetime
from talib import abstract

def RSI(df, period):
    return abstract.RSI(df, timeperiod=period)

stock_num = str(input("輸入股票代碼:"))

start = datetime.datetime(2021,9,28)
stock_df = pdr.DataReader(stock_num+'.TW', 'yahoo', start=start)
if(stock_df is not None):
    stock_df["close"] = stock_df["Close"]
    mc = mpf.make_marketcolors(up='r',down='g',volume='in')
    s  = mpf.make_mpf_style(marketcolors=mc)
    index  = mpf.make_addplot(RSI(stock_df, 14), panel = 2, ylabel = 'RSI', color = 'lime')
    mpf.plot(stock_df,type='candle', style = s, mav=(5,10,20), addplot = [index],volume=True)
else:
    print("wrong number")