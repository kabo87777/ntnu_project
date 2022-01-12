# coding=UTF-8
from tkinter.constants import BOTH, CENTER, LEFT
import mplfinance as mpf
import pandas_datareader as pdr
import datetime as datetime
from talib import abstract
import talib
import numpy as np
import pandas as pd
import tkinter as tk
import tkinter.tix as tix
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

def RSI(df, period):
    return abstract.RSI(df, timeperiod=period)

# 第1步，例項化object，建立視窗window
window = tk.Tk()

# 第2步，給視窗的視覺化起名字
window.title('股市視覺化')

# 第3步，設定視窗的大小(長 * 寬)
window.geometry('800x800')  # 這裡的乘是小x

bband = tk.BooleanVar() 
bband.set(True)

macd = tk.BooleanVar() 
macd.set(False)

rsi = tk.BooleanVar() 
rsi.set(False)

kd = tk.BooleanVar() 
kd.set(False)


# 第4步，在圖形介面上建立一個標籤用以顯示內容並放置
##tk.Label(window, text='on the window', bg='red', font=('Arial', 16)).pack()   # 和前面部件分開建立和放置不同，其實可以建立和放置一步完成

# 第5步，建立一個主frame，長在主window視窗上
frame = tk.Frame(window)
frame.pack()



def go():
    ##stock_num = str(input("輸入股票代碼:"))
    ##stock_num = '2330'
    stock_num = hi_there.get()
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

        index  = []
        panel = 2
        if(bband.get()):
            index.extend([mpf.make_addplot(stock_df['lowerband'],color = 'cyan',width=1),
                mpf.make_addplot(stock_df['middleband'],color='y',width=1),
                mpf.make_addplot(stock_df['upperband'],color = 'orange',width=1)])
        if(macd.get()):
            index.extend([mpf.make_addplot(stock_df["MACD"], panel = panel,type='bar', ylabel = 'MACD', color = 'red')])
            panel+=1
        if(rsi.get()):
            index.extend([mpf.make_addplot(RSI(stock_df, 14), panel = panel, ylabel = 'RSI', color = 'lime',width=1)])
            panel+=1
        if(kd.get()):
            index.extend([mpf.make_addplot(stock_df["k"], panel = panel, ylabel = 'KD', color = 'cyan',width=1),
                mpf.make_addplot(stock_df["d"], panel = panel,  color = 'orange',width=1)])
            panel+=1
        ##畫圖
        daily_fig, axlist = mpf.plot(stock_df,type='candle',  title = stock_num ,style = s, mav=(5,10,20), addplot = index,volume=True, returnfig=True)  ## mav = MA
        canvas = FigureCanvasTkAgg(daily_fig)
        canvas.get_tk_widget().pack()
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                    window)
        toolbar.update()
    
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
    else:
        print("wrong number")

#輸入框
hi_there = tk.Entry(window)
hi_there.pack()

#按鈕
mybutton = tk.Button(frame, text="輸入股票代碼" , command=go)
mybutton.pack()

BBAND_check = tk.Checkbutton(frame, text='BBAND', var=bband) 
BBAND_check.pack()

MACD_check = tk.Checkbutton(frame, text='MACD', var=macd) 
MACD_check.pack()

RSI_check = tk.Checkbutton(frame, text='RSI', var=rsi) 
RSI_check.pack()

KD_check = tk.Checkbutton(frame, text='KD', var=kd) 
KD_check.pack()
 
window.mainloop()