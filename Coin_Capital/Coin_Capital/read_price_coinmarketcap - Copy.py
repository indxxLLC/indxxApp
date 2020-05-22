"""
Created on Tue Jul 24 18:40:34 2018
@author: Kunal Ghildyal
"""
import requests as r
import pyodbc as ms, datetime as dt
import smtplib
 
""" MSSQL DB Connection """

sender = 'crypto@204.80.90.133.com'
receivers = ['mjain@indxx.com','pavank@indxx.com', 'rsingh@indxx.com']

db = ms.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=localhost;"
                        "Database=Coin_Capital_Indices;"
                        "uid=sa;pwd=f0r3z@786")
cursor = db.cursor()

""" GET price data from API"""

priceDate = (dt.datetime.today() - dt.timedelta(days= 1)).strftime('%Y-%m-%d')

resp = r.get('https://api.coinmarketcap.com/v2/ticker/?limit=50')

tickers = resp.json()

for key, value in tickers.items():
    if key == 'data':
        for key1, value1 in value.items():
            quotes = value1['quotes']['USD']
            sql = "INSERT INTO [dbo].[coin_price_marketcap] ([ticker], [date], [price], [volume_24h], [market_cap], [updated_at]) VALUES (?, ?, ?, ?, ?, ?)"    
            
            try:
                cursor.execute(sql, (value1['symbol'], priceDate, quotes['price'], quotes['volume_24h'], quotes['market_cap'], value1['last_updated']))
                cursor.commit()   
            except ms.Error as ex:
                sqlstate = ex.args[1]
                print(sqlstate)
db.close()
""" Send the email if prices are inserted in the database """

message = """From: CoinCapital Price Update <crypto@204.80.90.133.com>
To: Kunal Ghildyal <kghildyal@indxx.com>
MIME-Version: 1.0
Content-type: text/html
Subject: Prices inserted successfully for """+priceDate+"""

Price data entered successfully into the database.
"""
try:
    smtpObj = smtplib.SMTP(host='localhost',port=25)
    smtpObj.sendmail(sender, receivers, message)         
    print("Successfully sent email")
except smtplib.SMTPException as e:
    print(str(e))

smtpObj.quit()  
    