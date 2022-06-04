# coding=UTF-8
from tkinter import *
from tkinter.constants import BOTH, CENTER, LEFT
from matplotlib.pyplot import close
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

def btn_clicked():
    print("Button Clicked")

# 第1步，例項化object，建立視窗window
window = tk.Tk()

# 第2步，給視窗的視覺化起名字
window.title('股市視覺化')

# 第3步，設定視窗的大小(長 * 寬)
#window.geometry('800x800')  # 這裡的乘是小x
window.geometry("1572x947")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 947,
    width = 1572,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

canvas.create_rectangle(
    231, 3, 231+1341, 3+947,
    fill = "#222831",
    outline = "")


canvas.create_rectangle(
    0, -1, 0+231, -1+947,
    fill = "#eeeeee",
    outline = "")


canvas.create_rectangle(
    1092, 669, 1092+460, 669+230,
    fill = "#c4c4c4",
    outline = "")


canvas.create_rectangle(
    1092, 297, 1092+460, 297+338,
    fill = "#c4c4c4",
    outline = "")


canvas.create_rectangle(
    388, 669, 388+681, 669+230,
    fill = "#c4c4c4",
    outline = "")


bband = tk.BooleanVar() 
bband.set(True)

macd = tk.BooleanVar() 
macd.set(False)

rsi = tk.BooleanVar() 
rsi.set(False)

kd = tk.BooleanVar() 
kd.set(False)


# 第4步，在圖形介面上建立一個標籤用以顯示內容並放置
##tk.Label(window, text='on the window', bg='red', font=('Arial', 16)).grid()   # 和前面部件分開建立和放置不同，其實可以建立和放置一步完成

# 第5步，建立一個主frame，長在主window視窗上
frame_strategy = tk.Frame(window,bg="black")
frame_strategy.grid(row=0, column=0)

frame_substrategy = tk.Frame(window)
frame_substrategy.grid(row=0, column=1)

frame_entry = tk.Frame(window)
frame_entry.grid(row=1, column=0)

frame_plot = tk.Frame(window)
frame_plot.grid(row=2, column=0)

def go():
    ##stock_num = str(input("輸入股票代碼:"))
    ##stock_num = '2330'
    skillpoint = [0,0,0,0] ##壓力 布林 均線 MACD
    today = datetime.datetime.today() - datetime.timedelta(days=3) ##2022-06-04
    s =  today.strftime('%Y-%m-%d')
    # print(type(s))
 
    global canvas
    #canvas = None 
    stock_num = entry0.get()

    start = datetime.datetime(2021,9,24)
    stock_df = pdr.DataReader(stock_num+'.TW', 'yahoo', start=start)
    if(stock_df is not None):
        stock_df["close"] = stock_df["Close"]
        close = [float(x) for x in stock_df["close"]]
        
        ###指數平均線
        gold_cross = np.array([])
        death_cross = np.array([])
        stock_df["EMA5"] = int(0)
        stock_df["EMA10"] = int(0)
        stock_df["EMA5"] = talib.EMA(np.array(close),timeperiod=5)
        stock_df["EMA10"] = talib.EMA(np.array(close),timeperiod=10)
        cross = np.where(stock_df['EMA5']>stock_df['EMA10'],1,-1)
        for i in range(cross.size-1):
            if cross[i]==-1 and cross[i+1]==1:
                gold_cross = np.append(gold_cross,[stock_df.index[i]])
            if cross[i]==1 and cross[i+1]==-1:
                death_cross = np.append(death_cross,[stock_df.index[i]])
        print("gold\n",gold_cross)
        print("death\n",death_cross)
        
        stock_df["EMA20"] = int(0)
        stock_df["EMA20"] = talib.EMA(np.array(close),timeperiod=20)
        
        print(stock_df.at[s,"Open"])
        ###MACDd
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
        # if canvas: canvas.get_tk_widget().grid_forget()
        # canvas = tk.Canvas(frame_plot, width=400, height=400)
        # canvas = FigureCanvasTkAgg(daily_fig)
        # canvas.get_tk_widget().grid(row=2, column=0)
        daily_fig.savefig(stock_num + ".png")

        trend_img = PhotoImage(file = stock_num + ".png")
        trend_img = trend_img.zoom(4)
        trend_img = trend_img.subsample(5)
        canvas.create_image(
        720.0, 400.0,
        image = trend_img)
    
        # # creating the Matplotlib toolbar
        # toolbar = NavigationToolbar2Tk(canvas,window)
        # toolbar.update()
        # # placing the toolbar on the Tkinter window

        stock_df["predict"] = int(0)
        for i in range(len(stock_df.index)-3):
            if((stock_df.loc[stock_df.index[i+3],['Close']]>stock_df.loc[stock_df.index[i],['Close']]).bool()):
                stock_df.loc[stock_df.index[i],['predict']] = 1
            else:
                stock_df.loc[stock_df.index[i],['predict']] = 0

        #for i in range(13,len(stock_df.index)-3):
            #if((stock_df.loc[stock_df.index[i+1],['EMA12']]>stock_df.loc[stock_df.index[i+1],['EMA26']]).bool()):
                #if((stock_df.loc[stock_df.index[i],['EMA12']]<stock_df.loc[stock_df.index[i],['EMA26']]).bool()):
                    #print(stock_df.loc[stock_df.index[i],['Date']])
                    #print('1')
            
        #stock_df.to_csv('./SVM/'+stock_num+'.csv')

        #顯示資訊
        canvas.create_text(
        726.5, 135.0,
        text = "2330",
        fill = "#fd7014",
        font = ("None", int(35.0)))

        canvas.create_text(
        1358.5, 226.0,
        text = "score",
        fill = "#eeeeee",
        font = ("None", int(35.0)))

        canvas.create_text(
        510.0, 789.5,
        text = "start	\n547.00\nhigh	\n547.00\nlow	\n535.00",
        fill = "#000000",
        font = ("None", int(26.0)))

        canvas.create_text(
        721.0, 789.5,
        text = "value\n13.95\nP/E ratio	\n21.15\nyield\n2.04%",
        fill = "#000000",
        font = ("None", int(26.0)))

        canvas.create_text(
        934.0, 789.5,
        text = "CDP	\nB\n52 wk high\n688.00\n52 wk low	\n518.00",
        fill = "#000000",
        font = ("None", int(26.0)))

        canvas.create_text(
        1265.0, 355.0,
        text = "ma",
        fill = "#000000",
        font = ("None", int(35.0)))

        canvas.create_text(
        1429.0, 454.0,
        text = "8",
        fill = "#000000",
        font = ("None", int(100.0)))

        canvas.create_text(
        1497.0, 503.0,
        text = "/10",
        fill = "#000000",
        font = ("None", int(30.0)))

        canvas.create_text(
        1263.5, 491.5,
        text = "ma Long \nma short\n3 day gold\n3 dat dead",
        fill = "#000000",
        font = ("None", int(25.0)))

    else:
        print("wrong number")


# 主技術分析策略: 5/10/20/60MA 布林通道 RSI

# 副技術分析策略: VOL RSI MACD KD

but_col = 0
BBAND_check = tk.Checkbutton(frame_strategy, text='BBAND', var=bband) 
BBAND_check.grid(row=1, column=but_col)
but_col += 1

MACD_check = tk.Checkbutton(frame_strategy, text='MACD', var=macd) 
MACD_check.grid(row=1, column=but_col)
but_col += 1


RSI_check = tk.Checkbutton(frame_strategy, text='RSI', var=rsi) 
RSI_check.grid(row=1, column=but_col)
but_col += 1

KD_check = tk.Checkbutton(frame_strategy, text='KD', var=kd) 
KD_check.grid(row=1, column=but_col)
but_col += 1

#輸入框
#hi_there = tk.Entry(frame_entry)
#hi_there.grid(row=2, column=1)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    887.0, 42.0,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#eeeeee",
    highlightthickness = 0)

entry0.place(
    x = 750.0, y = 19,
    width = 274.0,
    height = 44)

#按鈕
# mybutton = tk.Button(frame_entry, text="搜尋" , command=go)
# mybutton.grid(row=2, column=2)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 60, y = 231,
    width = 115,
    height = 43)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b1.place(
    x = 60, y = 155,
    width = 115,
    height = 40)

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b2.place(
    x = 60, y = 65,
    width = 115,
    height = 46)

img3 = PhotoImage(file = f"img3.png") #搜尋按鈕
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = go,
    relief = "flat")

b3.place(
    x = 1057, y = 18,
    width = 64,
    height = 47)

#文字顯示

canvas.create_text(
    726.5, 135.0,
    text = "stock",
    fill = "#fd7014",
    font = ("None", int(35.0)))

canvas.create_text(
    1358.5, 226.0,
    text = "score",
    fill = "#eeeeee",
    font = ("None", int(35.0)))

canvas.create_text(
    510.0, 789.5,
    text = "start	\n547.00\nhigh	\n547.00\nlow	\n535.00",
    fill = "#000000",
    font = ("None", int(26.0)))

canvas.create_text(
    721.0, 789.5,
    text = "value\n13.95\nP/E ratio	\n21.15\nyield\n2.04%",
    fill = "#000000",
    font = ("None", int(26.0)))

canvas.create_text(
    934.0, 789.5,
    text = "CDP	\nB\n52 wk high\n688.00\n52 wk low	\n518.00",
    fill = "#000000",
    font = ("None", int(26.0)))

canvas.create_text(
    1265.0, 355.0,
    text = "ma",
    fill = "#000000",
    font = ("None", int(35.0)))

canvas.create_text(
    1429.0, 454.0,
    text = "8",
    fill = "#000000",
    font = ("None", int(100.0)))

canvas.create_text(
    1497.0, 503.0,
    text = "/10",
    fill = "#000000",
    font = ("None", int(30.0)))

canvas.create_text(
    1263.5, 491.5,
    text = "ma Long \nma short\n3 day gold\n3 dat dead",
    fill = "#000000",
    font = ("None", int(25.0)))

#顯示走勢圖
# trend_img = PhotoImage(file = f"output.png")
# trend_img = trend_img.zoom(4)
# trend_img = trend_img.subsample(5)
# canvas.create_image(
# 720.0, 400.0,
# image = trend_img)


# searchlabel = tk.Label(frame_entry, text='輸入股票代碼')
# searchlabel.grid(row=2, column=0)
background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    620.5, 166.0,
    image=background_img)

window.resizable(False, False)
window.mainloop()

