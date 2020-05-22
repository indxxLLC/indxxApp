"""
Created on Tue Jul 24 18:40:34 2018
@author: Kunal Ghildyal
"""
import requests as r
import pyodbc as ms, datetime as dt
import smtplib
import sys
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
""" MSSQL DB Connection """

sender = 'crypto@204.80.90.133.com'
receivers = ['mjain@indxx.com', 'pavank@indxx.com','rsingh@indxx.com']

"""
/////////////////////// onnection string using at 204.80.90.133 server ////////////////////////
db = ms.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=localhost;"
                        "Database=Coin_Capital_Indices;"
                        "uid=sa;pwd=f0r3z@786")
"""

db = ms.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=192.168.201.55;DATABASE=Coin_Capital_Indices;UID=sa;PWD=f0r3z@786')
cursor = db.cursor()

""" GET price data from API"""

priceDate = dt.datetime.today().strftime('%Y-%m-%d')
# - dt.timedelta(days= 1)
t = dt.datetime.today() #.strftime('%Y-%m-%d %H:%M:%S')
t1 = t.timetuple()
last_updated = time.mktime(t1)

#resp = r.get('https://api.coinmarketcap.com/v2/ticker/?limit=50')

#tickers = resp.json()
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'50',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '435e79aa-4666-4682-8088-fc0e675ec8ac',
}

session = Session()
session.headers.update(headers)

try:
	response = session.get(url, params=parameters)
	jsondata = json.loads(response.text)
	#print(jsondata)
except (ConnectionError, Timeout, TooManyRedirects) as e:
	print(e)

tickers = jsondata
for key, value in tickers.items():
    if key == 'data':
        for value1 in value:
            quotes = value1['quote']['USD']
            value1['last_updated'] = last_updated
            sql = "INSERT INTO [dbo].[coin_price_marketcap] ([ticker], [date], [price], [volume_24h], [market_cap], [updated_at]) VALUES (?, ?, ?, ?, ?, ?)"    
            
            try:
                cursor.execute(sql, (value1['symbol'], priceDate, quotes['price'], quotes['volume_24h'], quotes['market_cap'], value1['last_updated']))
                cursor.commit()   
            except ms.Error as ex:
                sqlstate = ex.args[1]
                print(sqlstate)
db.close()
""" Send the email if prices are inserted in the database """
#if data:
message = """From: CoinCapital Price Update <crypto@204.80.90.133.com>
To: Pavan <pavank@indxx.com>
MIME-Version: 1.0
Content-type: text/html
Subject: Prices inserted successfully for """+priceDate+"""

Price data entered successfully into the database.
"""

    
    
try:
    smtpObj = smtplib.SMTP(host='192.168.201.55',port=25)
    smtpObj.sendmail(sender, receivers, message)         
    print("Successfully sent email")
except smtplib.SMTPException as e:
    print(str(e))

smtpObj.quit()  
    