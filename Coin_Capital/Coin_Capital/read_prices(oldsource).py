"""
Created on Tue Jul 24 18:40:34 2018
@author: Kunal Ghildyal
"""
import requests as r
import pyodbc as ms, datetime as dt
import smtplib

""" MSSQL DB Connection """

sender = 'crypto@204.80.90.133.com'
receivers = ['pavank@indxx.com']

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

priceDate = (dt.datetime.today() - dt.timedelta(days= 1)).strftime('%Y-%m-%d') 
resp = r.get('https://coinsquare.com/api/v1/kingslanding/public/indxx?start_date='+priceDate+'&end_date='+priceDate)

""" Store the data into the database """ 

tickers = resp.json()
for key, value in tickers.items():
    for value1 in value:
        dateFormat = dt.datetime.strptime(value1['date'],'%Y-%m-%d')
        sql = "INSERT INTO [dbo].[coin_price] ([ticker], [date], [high], [low], [open], [close], [24h_volume], [market_cap]) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"    
        
        try:
            cursor.execute(sql, (value1['ticker'], dateFormat.strftime('%Y-%m-%d'), value1['high'], value1['low'], value1['open'], value1['close'], value1['24h_volume'], value1['market_cap']))
            cursor.commit()   
        except ms.Error as ex:
            sqlstate = ex.args[1]
            print(sqlstate)
            
""" Send the email if prices are inserted in the database """

try:
    smtpObj = smtplib.SMTP(host='localhost',port=25)
    message = """From: From Crypto <crypto@204.80.90.133.com>
                To: To Person <kghildyal@indxx.com>
                Subject: Prices inserted successfully for """+priceDate+"""
                Price data entered successfully into the database"""
    smtpObj.sendmail(sender, receivers, message)         
    
except smtplib.SMTPException as e:
    print(str(e))

smtpObj.quit()  