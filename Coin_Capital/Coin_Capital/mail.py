import smtplib
import datetime as dt
#, pyodbc as ms
#import pandas as pd
reviewDate = (dt.datetime.today() - dt.timedelta(days= 1)).strftime('%Y.%m.%d')

sender = 'crypto@204.80.90.133.com'
receivers = ['pavank@indxx.com']

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
