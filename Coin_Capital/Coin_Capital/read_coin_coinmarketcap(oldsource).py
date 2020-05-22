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

resp = r.get('https://api.coinmarketcap.com/v2/listings/')

tickers = resp.json()
i = 0
for key, value in tickers.items():
    if key == 'data':
        
        while(i < 51):
            print(value[i]['name'])
            i += 1
        raise SystemExit