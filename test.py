# coding=UTF-8
from asyncio.windows_events import NULL
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
import openpyxl
import tkinter.font as tkFont

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

#右下
canvas.create_rectangle(
    1092, 419, 1092+460, 419+480,
    fill = "#c4c4c4",
    outline = "")

#右上
canvas.create_rectangle(
    1092, 297, 1092+360, 297+100,
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

f1 = tkFont.Font(family='Tw Cen MT',size = 25 , weight='normal') #bold=粗體，normal=一般
#print(tkFont.families())

def go():
    ##stock_num = str(input("輸入股票代碼:"))
    ##stock_num = '2330'
    
    global canvas
    #canvas = None 
    canvas.delete("info")
    stock_num = entry0.get()
    # end = datetime.datetime(2022,6,2)
    # end = datetime.datetime(2022,6,15)
    end = datetime.datetime(2022,6,17)
    start = end -  datetime.timedelta(days = 50)
    # end = datetime.datetime(2022,6,17)
    stock_df = pdr.DataReader(stock_num+'.TW', 'yahoo', start=start,end=end)
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
        #print("gold\n",gold_cross)
        #print("death\n",death_cross)


        stock_df["EMA20"] = int(0)
        stock_df["EMA20"] = talib.EMA(np.array(close),timeperiod=20)
        
        today = datetime.datetime.today() - datetime.timedelta(days=0) ##2022-06-04
        # last_day =  today.strftime('%Y-%m-%d')
        last_day = stock_df.index.tolist()[-1]
        

        #print(type(stock_df.at[last_day,"Open"]))
        ###MACDd
        stock_df["MACD"],stock_df["MACDsignal"],stock_df["MACDhist"] = talib.MACD(np.array(close),fastperiod = 12,slowperiod = 26,signalperiod = 9)
        
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
            index.extend([mpf.make_addplot(stock_df["MACDhist"], panel = panel,type='bar', ylabel = 'MACD', color = 'red')])
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

        #f_score
        f_score_data = pd.read_excel("fscore.xlsx")
        f_score_data.set_index('代號')
        s = np.array([])
        score = 0
        for i in range(f_score_data.shape[0]):
            if str(f_score_data.loc[i]['代號'])!=str(stock_num):
                continue
            score = 0
            score+=f_score_data.loc[i]['(年)資產報酬率(%)']>0
            score+=f_score_data.loc[i]['(年)來自營運之現金流量(百萬)']>0
            score+=f_score_data.loc[i]['(年)來自營運之現金流量(百萬)']>f_score_data.loc[i]['(年)稅後淨利(百萬)']
            score+=f_score_data.loc[i]['(年)負債比率(%)']<f_score_data.loc[i]['(年-1)負債比率(%)']
            score+=f_score_data.loc[i]['(年)流動比率(%)']>f_score_data.loc[i]['(年-1)流動比率(%)']
            score+=f_score_data.loc[i]['(年)資產報酬率(%)']>f_score_data.loc[i]['(年-1)資產報酬率(%)']
            score+=f_score_data.loc[i]['(年)營業毛利率(%)']>f_score_data.loc[i]['(年-1)營業毛利率(%)']
            score+=f_score_data.loc[i]['(年)總資產週轉率(次)']>f_score_data.loc[i]['(年-1)總資產週轉率(次)']
            #s = np.append(s,[score])
            # print(f_score_data.loc[i]['代號'],':',score)
        #f_score_data['f_score'] = s
        #print(f_score_data.index)
        #顯示資訊
        # canvas.create_text(
        # 726.5, 135.0,
        # text = "2330",
        # fill = "#fd7014",
        # font = ("None", int(35.0)))

        #############分數計算######################
        skillpoint = [0,0,0,0] ##壓力 布林 均線 MACD
        last_gold = gold_cross[-1]
        # last_death = death_cross[-1]
        # last_gold = last_gold  - datetime.timedelta(days = 0)
        
        ######布林 
        # stock_df['upperband'],stock_df['middleband'],stock_df['lowerband']
        if stock_df["Close"][-1] > stock_df['lowerband'][-1] and stock_df["Close"][-2] < stock_df['lowerband'][-2]:
            skillpoint[1] = 100
            print(123)
        elif stock_df["Close"][-1] > stock_df['middleband'][-1] and stock_df["Close"][-2] < stock_df['middleband'][-2]:
            skillpoint[1] = 100
            print(456)
        flag = 1
        for i in range(5):
            a = stock_df["Close"][-1 - i]
            b = stock_df["middleband"][-1 - i]
            if a < b:
                flag = 0
                break
        if flag and stock_df["Close"][-1] < stock_df['middleband'][-1] * 1.1 and stock_df["Close"][-1] > stock_df['middleband'][-1]:
            skillpoint[1] = 100
        ######均線
        ##近3天多頭排列
        flag = 1
        for i in range(3):
            a = stock_df["EMA5"][-1 - i]
            b = stock_df["EMA10"][-1 - i]
            c = stock_df["EMA20"][-1 - i]
            if a < b or b < c:
                flag = 0
                break
        if flag:
            skillpoint[2] += 40
        #近3日>5MA
        flag = 1
        for i in range(3):
            a = stock_df["Close"][-1 - i]
            b = stock_df["EMA5"][-1 - i]
            if a < b:
                flag = 0
                break
        if flag:
            skillpoint[2] += 40
        #近三日黃金交叉
        flag = 0
        for i in range(3):
            a = stock_df.index.tolist()[-1 - i]
            if a == last_gold:
                flag = 1
                break
        if flag:
            skillpoint[2] += 20

        ####MACD 
        # stock_df["MACD"],stock_df["MACDsignal"],stock_df["MACDhist"]
        ##macd（对应dif） macdsignal（对应dea）macdhist（对应dif - dea）
        # 1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。       
        # 2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。       
        # 3.DEA线与K线发生背离，行情反转信号。       
        # 4.分析MACD柱状线，由正变负，卖出信号；由负变正，买入信号。
        if stock_df["MACDhist"][-1] > 0 and stock_df["MACDhist"][-2] < 0 :
            skillpoint[3] += 50
            if stock_df ["MACDsignal"][-1] > 0:
                skillpoint[3] += 50

        canvas.create_text(
        510.0, 785.5,
        text = "Open \n"+str(round(stock_df.at[last_day,"Open"],0))+"\nClose \n"+str(round(stock_df.at[last_day,"Close"],0))+"\nVolume \n"+str(round(stock_df.at[last_day,"Volume"],0)),
        fill = "#000000",
        #font = ("None", int(26.0)),
        font = f1,
        tag="info")

        #stock_df.at[last_day,"Open"]
        #print(stock_df.info())

        canvas.create_text(
        721.0, 789.5,
        text = "High \n"+str(round(stock_df.at[last_day,"High"],0))+"\nLow \n"+str(round(stock_df.at[last_day,"Low"],0)),
        fill = "#000000",
        #font = ("None", int(26.0)),
        font = f1,
        tag="info")

        # canvas.create_text(
        # 934.0, 789.5,
        # text = "CDP	\nB\n52 wk high\n688.00\n52 wk low	\n518.00",
        # fill = "#000000",
        # font = ("None", int(26.0)))


        #分數
        total = (skillpoint[1]+skillpoint[2]+skillpoint[3])/6
        total += (score/16)*100
        #print(skillpoint,score,total)
        canvas.create_text(
        1180, 345,
        text = round(total,2),
        fill = "#000000",
        font = f1,
        tag="info")

        canvas.create_text(
        1429.0, 454.0,
        #text = score,
        fill = "#000000",
        #font = ("None", int(100.0)),
        font = f1,
        tag="info")

        canvas.create_text(
        1497.0, 503.0,
        #text = "/9",
        fill = "#000000",
        #font = ("None", int(30.0)),
        font = f1,
        tag="info")

        good_or_bad = ["優","中","差"]
        print(skillpoint)
        if skillpoint[1]!=100:
            bband_text = good_or_bad[2]
        elif skillpoint[1]==100:
            bband_text = good_or_bad[0]
        
        if skillpoint[2]==100:
            ma_text = good_or_bad[0]
        elif skillpoint[2]>=60 and skillpoint[2]<100:
            ma_text = good_or_bad[1]
        elif skillpoint[2]<60:
            ma_text = good_or_bad[2]
        if skillpoint[3]==100:
            macd_text = good_or_bad[0]
        elif skillpoint[3]==50:
            macd_text = good_or_bad[1]
        elif skillpoint[3]<50:
            macd_text = good_or_bad[2]
        if score>=7:
            fscore_text = good_or_bad[0]
        elif score>=4 and score<7:
            fscore_text = good_or_bad[1]
        elif score<4:
            fscore_text = good_or_bad[2]
        canvas.create_text(
        1163.5, 581.5,
        text = "布林通道\n" + bband_text + "\n均線理論\n" + ma_text + "\nMACD\n" + macd_text+ "\nF-SCORE\n" + fscore_text,
        fill = "#000000",
        #font = ("None", int(25.0)),
        font = f1,
        tag="info")

        global trend_img
        trend_img = PhotoImage(file = stock_num+".png")
        trend_img = trend_img.zoom(4)
        trend_img = trend_img.subsample(5)
        canvas.create_image(
        720.0, 400.0,
        image = trend_img)

    else:
        print("wrong number")


# 主技術分析策略: 5/10/20/60MA 布林通道 RSI

# 副技術分析策略: VOL RSI MACD KD
trend_img = PhotoImage(file = "2330.png")

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

#文字
canvas.create_text(
1358.5, 226.0,
text = "score",
fill = "#eeeeee",
font = f1
)

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

