import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
data=pd.read_csv('./SVM/2330.csv')
df=data.copy()
reg_up=linregress(x=df.index,y=df.Close)
up_line=reg_up[1]+reg_up[0]*df.index

df_temp=df[df['Close']>up_line]
reg=linregress(x=df_temp.index,y=df_temp.Close)
df['HT']=reg[1]+reg[0]*data.index
while len(df_temp)>=5:
    reg=linregress(x=df_temp.index,y=df_temp.Close)
    up_line=reg[1]+reg[0]*data.index
    df_temp=df[df['Close']>up_line]

df['High_Trend']=reg[1]+reg[0]*data.index

reg_up2=linregress(x=df.index,y=df.Close)
up_line2=reg_up2[1]+reg_up2[0]*df.index
df_temp2=df[df['Close']<up_line2]
reg2=linregress(x=df_temp2.index,y=df_temp2.Close)
df['HT']=reg2[1]+reg2[0]*data.index
while len(df_temp2)>=5:
    reg2=linregress(x=df_temp2.index,y=df_temp2.Close)
    up_line2=reg2[1]+reg2[0]*data.index
    df_temp2=df[df['Close']<up_line2]

df['Low_Trend']=reg2[1]+reg2[0]*data.index

df['Close'].plot()
df['Low_Trend'].plot()
df['High_Trend'].plot()
plt.show()