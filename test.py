import pandas_datareader as pdr
import mplfinance as mpf
import datetime as datetime

<<<<<<< Updated upstream
=======
<<<<<<< HEAD
start = datetime.datetime(2021,9,27)
df_2330 = pdr.DataReader('2330.TW', 'yahoo', start=start)
print(df_2330)
mpf.plot(df_2330,type='candle', mav=(5,10,20),volume=True)
=======
>>>>>>> Stashed changes
dates = [20211001,20211101]
stockNo = 2330
url_template = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date={}&stockNo={}"

for date in dates :
    url = url_template.format(date, stockNo)
    file_name = "{}_{}.csv".format(stockNo, date)
    
    data = pd.read_html(requests.get(url).text)[0]
    data.columns = data.columns.droplevel(0)
    data.to_csv(file_name, index=False,encoding="utf-8-sig")
>>>>>>> 69ba26dbf8dccf86434e8d4e6b6d7e4923138e4b
