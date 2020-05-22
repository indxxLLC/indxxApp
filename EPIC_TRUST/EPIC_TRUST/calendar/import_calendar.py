import sys
import time
import requests
import datetime
import numpy as np
import pymysql as ms
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
df = pd.read_excel('tllcg_calendar_2020.xlsx')

"""
INDEX_ID =1
QUE = "select * from d_dailydatareq where INDEX_ID = {0}"
Q = QUE.format(INDEX_ID)    

con = ms.connect("127.0.0.1","root","123456789+","epic_trust_vvr")
Meas = pd.read_sql(Q, con=con)
print(Meas['TS_CREATE'])
con.close()
"""


connection = ms.connect("127.0.0.1","root","123456789+","epic_trust_vvr")
cursor = connection.cursor()
	
sql = """insert into d_calendar (CALENDAR_ID,TRADE_DATE,DAY,MONTH,YEAR,TRADING_DAY,DAYINWEEK,TR_DAY_MONTH) values (%s,%s,%s,%s,%s,%s,%s,%s)"""

for i in df.index:
	values = (df['CALENDAR_ID'][i],df['TRADE_DATE'][i].strftime("%Y-%m-%d"),df['DAY'][i],df['MONTH'][i],df['YEAR'][i],df['TRADING_DAY'][i],df['DAYINWEEK'][i],df['TR_DAY_MONTH'][i])
	
	#print(sql2)
	cursor.executemany(sql, values)
    
cursor.close()
cursor.commit()
cursor.close()
connection.close()
#print(cursor.rowcount, "record inserted.")
