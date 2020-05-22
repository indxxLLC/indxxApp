# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 17:31:35 2018

@author: Kunal
"""

import ftplib, smtplib
import datetime as dt, pyodbc as ms
import pandas as pd

"""
/////////////////////// onnection string using at 204.80.90.133 server ////////////////////////
db = ms.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=localhost;"
                        "Database=Coin_Capital_Indices;"
                        "uid=sa;pwd=f0r3z@786")
"""

db = ms.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=192.168.201.55;DATABASE=Coin_Capital_Indices;UID=sa;PWD=f0r3z@786')
cursor = db.cursor()

reviewDate = (dt.datetime.today() - dt.timedelta(days= 1)).strftime('%Y.%m.%d')
#reviewDate = '2019.01.31'


filename = 'Rebalancing_'+reviewDate+'.csv'
"""
path = '/'
ftp = ftplib.FTP("127.0.0.1") 
ftp.login("indxx_coincapital", "indxx_coincapital") 
ftp.cwd(path)
ftp.retrbinary("RETR " + filename, open('Review//'+filename, 'wb').write)
ftp.quit()
"""

csvfile = pd.read_csv('Review//' + filename)

for index, row in csvfile.iterrows():
    sql = "INSERT INTO [dbo].[index_weights_shares] ([index_id], [ticker], [date], [shares]) VALUES (?, ?, ?, ?)"    
    # execute SQL query using execute() 
    try:   
        cursor.execute(sql, (row['index_id'], row['tickers'], dt.datetime.strptime(row['date'], '%m/%d/%Y').strftime('%Y-%m-%d'), row['shares']))
        cursor.commit()
    except ms.Error as ex:
        sqlstate = ex.args[1]
        print(sqlstate)

sender = 'crypto@204.80.90.133.com'
receivers = ['rsingh@indxx.com','pavank@indxx.com']

message = """From: CoinCapial Review <crypto@204.80.90.133.com>
To: Pavan Kumar <pavank@indxx.com>
MIME-Version: 1.0
Content-type: text/html
Subject: Review Implemented for """+reviewDate+"""

New portfolio has been uploaded.
"""
try:
    smtpObj = smtplib.SMTP(host='192.168.201.55',port=25)
    smtpObj.sendmail(sender, receivers, message)         
    print("Successfully sent email")
except smtplib.SMTPException as e:
    print(str(e))

smtpObj.quit() 

db.close()