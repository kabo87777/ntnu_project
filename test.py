import requests
import pandas as pd

dates = [20211101]
stockNo = 2330
url_template = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date={}&stockNo={}"

for date in dates :
    url = url_template.format(date, stockNo)
    file_name = "{}_{}.csv".format(stockNo, date)
    
    data = pd.read_html(requests.get(url).text)[0]
    data.columns = data.columns.droplevel(0)
    data.to_csv(file_name, index=False,encoding="utf-8-sig")