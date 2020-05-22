# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 19:16:25 2018

@author: Kunal
"""

import pyodbc as ms, datetime as dt
import smtplib

def sendMail(subject, content):
    sender = 'crypto@204.80.90.133.com'
    receivers = ['mjain@indxx.com', 'pavank@indxx.com','rsingh@indxx.com']
	# 'mjain@indxx.com', 'pavank@indxx.com','rsingh@indxx.com'
    message = """From: CoinCapital Index Value <crypto@204.80.90.133.com>
    To: Kunal Ghildyal <kghildyal@indxx.com>
    MIME-Version: 1.0
    Content-type: text/html
    
    Subject: """+subject+"""\n
    
    """+content

    try:
        smtpObj = smtplib.SMTP(host='192.168.201.55',port=25)
        smtpObj.sendmail(sender, receivers, message)         
        print("Successfully sent email")
    except smtplib.SMTPException as e:
        print(str(e))
    
    smtpObj.quit()  

def indexValue(investment):
    return investment/100

def indexMcap(price,shares):
    return price*shares
"""
/////////////////////// onnection string using at 204.80.90.133 server ////////////////////////
db = ms.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=localhost;"
                        "Database=Coin_Capital_Indices;"
                        "uid=sa;pwd=f0r3z@786")
"""

db = ms.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=192.168.201.55;DATABASE=Coin_Capital_Indices;UID=sa;PWD=f0r3z@786')
                        
cursor = db.cursor()

# # 435e79aa-4666-4682-8088-fc0e675ec8ac
calcdate = (dt.datetime.today()).strftime('%Y-%m-%d')
# - dt.timedelta(days= 1)

#calcdate = '2019-11-22'

cursor.execute("SELECT * FROM [dbo].[coin_price_marketcap] WHERE date = ?", calcdate)
#prices = cursor.fetchall()

if cursor.rowcount == 0:
    subject = "Prices for "+calcdate+" were not found in the db"
    content = "Index values cannot be calculated as the prices were not found." 
    sendMail(subject, content)

    raise SystemExit

sql = "SELECT * FROM [dbo].[index]"    
cursor.execute(sql)
results = cursor.fetchall()

for row in results:
    investmentValue = 0
    index_id = row[0]
    sql = "SELECT a.shares, a.ticker, b.price FROM [dbo].[index_weights_shares] a, [dbo].[coin_price_marketcap] b WHERE a.index_id = ? AND b.date=? AND a.ticker=b.ticker AND a.date = (SELECT MAX(date) FROM [Coin_Capital_Indices].[dbo].[index_weights_shares])"    
    cursor.execute(sql, index_id, calcdate)
    result_shares = cursor.fetchall()
    
    for row_share in result_shares:
        investmentValue += indexMcap(row_share[0], row_share[2])
        
    sql2 = "INSERT INTO [dbo].[index_values] ([index_id], [date], [levels]) VALUES (?, ?, ?)"    
    # execute SQL query using execute() method.
    try:
        cursor.execute(sql2, (index_id, calcdate, indexValue(investmentValue)))
        cursor.commit()
    except ms.Error as ex:
        sqlstate = ex.args[1]
        print(sqlstate) 

sendMail("Index values calculated for "+calcdate, "Index Values are saved in the database for "+calcdate)
db.close()