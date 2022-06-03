import pandas as pd
import numpy as np
import openpyxl
data = pd.read_excel("123.xlsx")
data.set_index('代號')
s = np.array([])
for i in range(data.shape[0]):
    score = 0
    score+=data.loc[i]['(年)資產報酬率(%)']>0
    score+=data.loc[i]['(年)來自營運之現金流量(百萬)']>0
    score+=data.loc[i]['(年)來自營運之現金流量(百萬)']>data.loc[i]['(年)稅後淨利(百萬)']
    score+=data.loc[i]['(年)負債比率(%)']<data.loc[i]['(年-1)負債比率(%)']
    score+=data.loc[i]['(年)流動比率(%)']>data.loc[i]['(年-1)流動比率(%)']
    score+=data.loc[i]['(年)資產報酬率(%)']>data.loc[i]['(年-1)資產報酬率(%)']
    score+=data.loc[i]['(年)營業毛利率(%)']>data.loc[i]['(年-1)營業毛利率(%)']
    score+=data.loc[i]['(年)總資產週轉率(次)']>data.loc[i]['(年-1)總資產週轉率(次)']
    s = np.append(s,[score])
    print(data.loc[i]['代號'],':',score)
data['f_score'] = s
print(data)