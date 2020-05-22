# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 07:18:10 2018

@author: Suraj SS Tipirneni
"""

### To be included in reload function
import sys
import time
import datetime
import pymysql as ms
import pandas as pd
from datetime import timedelta
# sys.path.insert(0, 'E:\\EPIC_RUST\\Traffic_Light_Large_Cap_Growth_Index\\FUNCTIONS') 

from FUNCTIONS import import_export as ie
from FUNCTIONS import date_functions as dt

#EX_DATE = '2019-09-20'    
#TICKER = ['SPY US EQUITY']
#VARS = ['TICKER','CP_GROSS_AMT','ts_update']
#CALENDAR_ID = 1
#INDEX_ID = 1

#con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")
'''    ---->   EXAMPLE:
    Period_Divisor('2018-03-16',['SPY US EQUITY'],1,1)           '''

#TICKER =['SPY US Equity','SPYG US Equity','SLYG US Equity','SHY US Equity','IWF US Equity']
#CALENDAR_ID = 1
#INDEX_ID =1
#EX_DATE = '2018-03-22'
#Period_Divisor('2019-01-31','SPYG US EQUITY',1,1)

def Period_Divisor(EX_DATE,TICKER,CALENDAR_ID,INDEX_ID) :    
######   Fetching the UTS and CA values for range of tickers
    ts = time.time()
    curr_time = datetime.datetime.fromtimestamp(ts)
    curr_time = int(curr_time.strftime('%Y%m%d%H%M%S')) / 1000000
    if EX_DATE == '':
        for i in TICKER:
            INFO = ie.imp_d_ca('A', '', '', [i], ['DVD_CASH'], ['TICKER','EX_DATE'])  
            EX_DATE = list(INFO['EX_DATE'].apply(lambda x:str(x)))
            for j in EX_DATE:
                EX_DATE_TM1 = dt.WORKDAY(j,CALENDAR_ID,-1)
                
                PRICE = ie.imp_d_price('',CALENDAR_ID,EX_DATE_TM1,EX_DATE_TM1,[i],['PX_SETTLE'],'BLOOMBERG')            
                CA_VALUE  = ie.imp_d_ca('r', j, j, [i], ['DVD_CASH'], ['TICKER','CP_GROSS_AMT']) #list(INFO['CP_GROSS_AMT'].values)[0]
                
                PERIOD_DIVISOR  = (PRICE - CA_VALUE.values)/PRICE
                
                vals = [[curr_time,j,INDEX_ID, [i],1,'Period_Divisor',str(PERIOD_DIVISOR),'Y',j,'2099-12-31']]
                ie.exp_f_calc(vals,INDEX_ID,i,'0',j,'Period_Divisor','')

    else:
        cut_off_time = datetime.datetime.fromtimestamp(ts) - timedelta(hours=1)
        cut_off_time = cut_off_time.strftime('%Y-%m-%d %H:%M:%S')
        EX_DATE_TM1 = dt.WORKDAY(EX_DATE,CALENDAR_ID,-1)
####### Check if the TICKER EX_DATE combination ts_update is within one hour of systime
        for i in TICKER:
            INFO = ie.imp_d_ca('', EX_DATE, EX_DATE, [i], ['DVD_CASH'], ['TICKER','CP_GROSS_AMT','TS_UPDATE','EX_DATE']) 
#            INFO = INFO[(INFO.TS_UPDATE >= cut_off_time)]
            PRICE = ie.imp_d_price('',CALENDAR_ID,EX_DATE_TM1,EX_DATE_TM1,[i],['PX_SETTLE'],'BLOOMBERG') 
######  Period Divisor Calculation
            PRICE = list(PRICE.iloc[0].values)[0]
            CA_VALUE  = list(INFO['CP_GROSS_AMT'].values)[0]
            PERIOD_DIVISOR  = (PRICE - CA_VALUE)/PRICE
   
            con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")
            cursor = con.cursor() 

            cursor.execute("update  f_calc set VALUE = %s ,  VALID_TO = %s  where INDEX_ID = %s and VALID_TO = '2099-12-31' and  DESCRIPTION = 'Period_Divisor' and SECURITY_NAME = %s;", [str(PERIOD_DIVISOR),EX_DATE_TM1,INDEX_ID, i]) 
            
            vals = [[curr_time,EX_DATE,INDEX_ID, i,'0','Period_Divisor','1.0','Y',EX_DATE,'2099-12-31']]
            cursor.executemany("insert into f_calc(RUNTIMEID,TRADE_DATE, INDEX_ID, SECURITY_NAME, PORTFOLIO, DESCRIPTION, VALUE, VALID_FLAG, VALID_FROM, VALID_TO) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;", vals)
            
            con.commit()
            con.close()
    
    
    
    
#TICKER = ['SPY US Equity'],'SPYG US Equity','SLYG US Equity','SHY US Equity','IWF US Equity']
''' ------->> EXAMPLE   
                        TR_SERIES(['SLYG US EQUITY'],1,'2019-05-31',1)  '''

def TR_SERIES(TICKER,CALENDAR_ID,TRADE_DATE,INDEX_ID):  
    ########  Fetch the entire history of prices for the ticker
    PR_SERIES = ie.imp_d_price('',CALENDAR_ID,'1900-01-01',TRADE_DATE, TICKER, ['PX_SETTLE'], 'BLOOMBERG')
    ######## Fetch the entire period divisors <= TRADE_DATE along with VALID_FROM to VALID_TO
    DIVISORS = ie.imp_f_calc('1900-01-01', TRADE_DATE, TICKER,'0', str(INDEX_ID), ['Period_Divisor'],['VALUE','VALID_FROM'],['VALID_FROM'])
    DIVISORS = DIVISORS.drop_duplicates(subset=['VALUE','VALID_FROM']).sort_values(by='VALID_FROM', ascending=True)
    
    DIVISORS['MUTIPLIER']  = DIVISORS.VALUE
    DIVISORS = DIVISORS.sort_values(by='VALID_FROM', ascending=False).reset_index()
    
    DIVISORS.loc[0,'MUTIPLIER'] = 1
    DIVISORS['MUTIPLIER']  = DIVISORS.MUTIPLIER.cumprod()
    
    DIVISORS['VALID_FROM'] = DIVISORS['VALID_FROM'].apply(lambda x:str(x))       
    PR_SERIES['TRADE_DATE'] = PR_SERIES.index
    PR_SERIES['TRADE_DATE'] = PR_SERIES['TRADE_DATE'].apply(lambda x:str(x))
    PR_SERIES=PR_SERIES.rename(columns={"TRADE_DATE": "TRADE_DATE1"})
    
    temp = PR_SERIES.merge(DIVISORS, left_on = 'TRADE_DATE1', right_on = 'VALID_FROM', how = 'left', left_index=False, right_index=False) 
    temp = temp.sort_values(by='TRADE_DATE1', ascending=True)
    
    temp['VALUE'] = temp['VALUE'].fillna(method='ffill')
    temp['MUTIPLIER'] = temp['MUTIPLIER'].fillna(method='ffill')
    t1 = temp[['TRADE_DATE1','VALID_FROM',TICKER[0],'MUTIPLIER','VALUE']].sort_values(by='TRADE_DATE1', ascending=False)  

    t1['TR_SERIES'] = t1['MUTIPLIER'] * t1[TICKER[0]]
    t1['TRADE_DATE'] = t1['TRADE_DATE1'].apply(lambda x:str(x))
#    writer = pd.ExcelWriter('C:\\Users\\Administrator\\Desktop\\'+j+'TR.xlsx')
#    t1.to_excel(writer,j)
#    writer.save()
    return(t1)  
    
    

#df2.to_excel(writer,'Sheet2')
