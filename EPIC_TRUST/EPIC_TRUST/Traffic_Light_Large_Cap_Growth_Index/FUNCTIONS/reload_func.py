# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 12:11:10 2018

@author: Suraj SS Tipirneni
"""
#Test Values
#Example :  -- > Reload(DATE,1,1)
#DATE = '2019-11-01'
#INDEX_ID = 1
#CALENDAR_ID = 1
#Reload('2019-06-03',1,1)
#con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")

import sys
import time
import requests
import datetime
import pymysql as ms
import pandas as pd
#from datetime import timedelta
# sys.path.insert(0, 'E:\\EPIC_RUST\\Traffic_Light_Large_Cap_Growth_Index\\FUNCTIONS') 
# from FUNCTIONS  import price_adj_func as pa
from FUNCTIONS  import functions as func
from pandas import DataFrame
exec_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d.%H%M%S')

def Reload(DATE,INDEX_ID,CALENDAR_ID):   
    #Getting Required requests
    QUE = "select * from d_dailydatareq where INDEX_ID = {0}"
    Q = QUE.format(INDEX_ID)    
    
    con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")
    Meas = pd.read_sql(Q, con=con)
    con.close()
    
    Meas = Meas.drop(columns = {"SLNO", "VALID_FLAG"})# Dropping serial Number
    #Seperating Request Types
    CA_REQ = Meas[Meas["FIELD"] == 'CA']
    PRICE_REQ = Meas[Meas["FIELD"] == 'PX_SETTLE']
    CURR_REQ = Meas[Meas["FIELD"] == 'CURR']
    #Fetching data for corresponding Request types.
    #CA IMPORT. Currenty only looking for dividends.
    if (len(CA_REQ) > 0): 
        r_data = CA_DATALOAD(DATE).rename(columns = {'IDENTIFIER':'ISIN'})  
        CA_dat = pd.merge(CA_REQ[['ISIN']],r_data,on = 'ISIN', how='left',left_index=False, right_index=False)
        CA_dat = CA_dat[["ACTION_ID","CORPORATE_ACTION","COUNTRY_CODE","CURRENCY","DATAPROVIDER","EX_DATE","ISIN","IDENTIFIER_NAME","MODIFY_DATE","NAME","SYMBOL","TICKER",'VALUES']]
        
        CA_dat = CA_dat.dropna()
        try:
            if CA_dat.empty != 1: 
                CA_dat = CA_dat[CA_dat['CORPORATE_ACTION'] == 'DVD_CASH']
                up_pack = CA_dat['VALUES']
                up_pack.index = CA_dat['ISIN']
                #CA_dat.index = CA_dat['ISIN']
                
                tr = pd.DataFrame(up_pack)
                tr2 = pd.DataFrame()
                for i in range(len(tr)):
                    R1 = tr.iloc[i]
                    sd = R1.values.tolist()
                    r1 =DataFrame.from_records(sd[0])
                    tr1 = r1.set_index('name').T
                    x = tr1[['CP_GROSS_AMT','Frequency','Paydate','CP_DVD_TYP','Recdate']]
                    tr2 = pd.concat([tr2,x]).reset_index()
                    tr2.loc[i,'ISIN'] =  R1.name
                    #tr2['ISIN'] =  R1.name
                #tr2['ISIN']  = CA_dat['ISIN']#CA_dat.index
                
                tr2= tr2.drop(columns={'index'})
                
                CA_dat_f = pd.merge(CA_dat, tr2, on = 'ISIN',how = 'inner', left_index=False, right_index=False)
                CA_dat_f = CA_dat_f.rename(columns = {'Recdate':'Record_date', 'Paydate':'PAYMENT_DATE'}) 
                CA_dat_f.columns = map(str.upper, CA_dat_f.columns)
                CA_dat_f['TICKER'] = CA_dat_f['TICKER'].str.upper()
                CA_dat_f = CA_dat_f[["TICKER","ISIN","EX_DATE","CORPORATE_ACTION","CP_GROSS_AMT","CURRENCY","RECORD_DATE","PAYMENT_DATE","DATAPROVIDER","CP_DVD_TYP","FREQUENCY"]]
                vals = CA_dat_f.values.tolist()
                d_ca_DATALOAD(vals)
                TICK = list(CA_dat_f['TICKER'].unique())
                pa.Period_Divisor(DATE,TICK,CALENDAR_ID,INDEX_ID)
                
        except Exception as e:
            s = repr(e)
            con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")
            cursor = con.cursor() 
            vals = [exec_time,'Reload_Func',str(INDEX_ID),s,'N']
            cursor.execute("insert into d_run_exceptions (Runtimeid, Job_Failed, Index_ID, Error_Message, Resolution_Found) values (%s,%s,%s,%s,%s);",  vals)
            con.commit()
            con.close()
            func.error_msg(s,'CA not fulfilled.')
            
    #PRICE IMPORT    
    if (len(PRICE_REQ) > 0):  
        r_data = PRICE_DATALOAD(DATE)
        PRICE_dat = pd.merge(PRICE_REQ[['ISIN','TICKER','FIELD']],r_data[['ISIN','DATE','PRICE']],on = 'ISIN',how='left',left_index=False, right_index=False)
        PRICE_dat['DATA_SOURCE'] = 'BLOOMBERG'
        PRICE_dat = PRICE_dat.drop(columns = {"ISIN"})
        PRICE_dat = PRICE_dat[['DATE','TICKER','FIELD','PRICE','DATA_SOURCE']]
        PRICE_dat = PRICE_dat.dropna()
        PRICE_dat['TICKER'] = PRICE_dat['TICKER'].str.upper()
        vals = PRICE_dat.values.tolist()
        d_price_DATALOAD(vals) 

    #CURR IMPORT    
    if (len(CURR_REQ) > 0):
        r_data = CURR_DATALOAD(DATE).rename(columns = {'CURRENCY_TICKER':'TICKER'})        
        CURR_dat = pd.merge(CURR_REQ[['TICKER','FIELD']],r_data[['TICKER','DATE','PRICE']],on = 'TICKER', how='left',left_index=False, right_index=False)
        CURR_dat['DATA_SOURCE'] = 'BLOOMBERG'
        CURR_dat = CURR_dat[['DATE','TICKER','FIELD','PRICE','DATA_SOURCE']]
        CURR_dat['TICKER'] = CURR_dat['TICKER'].str.upper()
        vals = CURR_dat.values.tolist()
        d_price_DATALOAD(vals)

def PRICE_DATALOAD(DATE):
    url = 'http://146.20.65.208/central_db_edi/api/gettodayprice.php?type1=JSON&authcode=INDXX:931&date='+DATE
    temp3=requests.get(url).json()
    temp3 =temp3['data']
    rawdata=pd.DataFrame.from_dict(temp3, orient='columns')
    rawdata=pd.DataFrame.transpose(rawdata)
    rawdata.columns = map(str.upper, rawdata.columns)
    return(rawdata)
   
def CA_DATALOAD(DATE):
    url = 'http://146.20.65.208/central_db_edi/api/getdateca.php?type1=JSON&authcode=INDXX:931&date='+DATE
    temp3=requests.get(url).json()
    temp3 =temp3['data']
    rawdata = pd.DataFrame()
    for i in range(len(temp3)):
        dd = pd.DataFrame(temp3[i])
        dd1 = dd.transpose()
        rawdata = rawdata.append(dd1)    
    rawdata.index = rawdata['identifier']
    rawdata.columns = map(str.upper, rawdata.columns)
    return(rawdata)
    
def CURR_DATALOAD(DATE):
    url = 'http://146.20.65.208/central_db_edi/api/gettodaycurr.php?type1=JSON&authcode=INDXX:931&date='+DATE
    temp3=requests.get(url).json()
    temp3 =temp3['data']
    rawdata=pd.DataFrame.from_dict(temp3, orient='columns')
    rawdata=pd.DataFrame.transpose(rawdata)
    rawdata.columns = map(str.upper, rawdata.columns)
    return(rawdata)
    
def d_ca_DATALOAD(vals): 
    con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")
    cursor = con.cursor() 
    cursor.execute('''delete from s_ca;''')
    cursor.executemany("insert into s_ca (TICKER, ISIN, EX_DATE, CORPORATE_ACTION, CP_GROSS_AMT,CURRENCY, REC_DATE, PAYMENT_DATE, DATA_SOURCE, CA_TYPE_SP,FREQUENCY) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",  vals)

    cursor.execute('''insert into d_ca (TICKER,ISIN,EX_DATE,CORPORATE_ACTION,CP_GROSS_AMT,CURRENCY,REC_DATE,PAYMENT_DATE,DATA_SOURCE,CA_TYPE_SP,FREQUENCY)
                         select l.TICKER,
                                l.ISIN,
                                l.EX_DATE,
                                l.CORPORATE_ACTION,
                                l.CP_GROSS_AMT,
                                l.CURRENCY,
                                l.REC_DATE,
                                l.PAYMENT_DATE,
                                l.DATA_SOURCE,
                                l.CA_TYPE_SP,
                                l.FREQUENCY  from s_ca as l 
                          left outer join d_ca as r on
                                l.ISIN =  r.ISIN and
                                l.TICKER =  r.TICKER and
                                l.EX_DATE =  r.EX_DATE and
                                l.CORPORATE_ACTION =  r.CORPORATE_ACTION and
                                l.CP_GROSS_AMT =  r.CP_GROSS_AMT and
                                l.CURRENCY =  r.CURRENCY and
                                l.REC_DATE =  r.REC_DATE and
                                l.PAYMENT_DATE =  r.PAYMENT_DATE and
                                l.DATA_SOURCE =  r.DATA_SOURCE and
                                l.CA_TYPE_SP =  r.CA_TYPE_SP and
                                l.FREQUENCY =  r.FREQUENCY where r.TICKER is null and r.ISIN is null and r.CP_GROSS_AMT is null and r.CORPORATE_ACTION is null and  r.EX_DATE is null and r.CA_TYPE_SP is null ''')
    con.commit()
    con.close()
#    cursor.executemany("insert into s_price(TRADE_DATE, TICKER,REQ_TYPE,PRICE,DATA_SOURCE) values (%s, %s,%s, %s,%s)", vals )
#    cursor.execute("update  d_price set PRICE = %s where  TRADE_DATE = %s and TICKER = %s " , ('189', '2018-08-01', 'SHY US Equity'))
    con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")
    cursor = con.cursor() 
    cursor.execute('''update d_ca as l inner join s_ca as r on
                                l.ISIN =  r.ISIN and
                                l.TICKER =  r.TICKER and
                                l.EX_DATE =  r.EX_DATE and
                                l.CORPORATE_ACTION =  r.CORPORATE_ACTION and
                                l.CP_GROSS_AMT =  r.CP_GROSS_AMT and
                                l.CURRENCY =  r.CURRENCY and
                                l.REC_DATE =  r.REC_DATE and
                                l.PAYMENT_DATE =  r.PAYMENT_DATE and
                                l.DATA_SOURCE =  r.DATA_SOURCE and
                                l.CA_TYPE_SP =  r.CA_TYPE_SP and
                                l.FREQUENCY =  r.FREQUENCY
                            
                          set   l.ISIN =  r.ISIN ,
                                l.TICKER =  r.TICKER ,
                                l.EX_DATE =  r.EX_DATE ,
                                l.CORPORATE_ACTION =  r.CORPORATE_ACTION ,
                                l.CP_GROSS_AMT =  r.CP_GROSS_AMT ,
                                l.CURRENCY =  r.CURRENCY ,
                                l.REC_DATE =  r.REC_DATE ,
                                l.PAYMENT_DATE =  r.PAYMENT_DATE ,
                                l.DATA_SOURCE =  r.DATA_SOURCE ,
                                l.CA_TYPE_SP =  r.CA_TYPE_SP ,
                                l.FREQUENCY =  r.FREQUENCY''')
    cursor.execute('''delete from s_ca''')
    con.commit()
    con.close()
        
def d_price_DATALOAD(vals) :   
    con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")
    cursor = con.cursor() 
    cursor.execute('''delete from s_price ;''')
    cursor.executemany("insert into s_price(TRADE_DATE, TICKER,REQ_TYPE,PRICE,DATA_SOURCE) values (%s, %s,%s, %s,%s) ;", vals)
    
    cursor.execute('''insert into d_price (TRADE_DATE,TICKER,REQ_TYPE,DATA_SOURCE,PRICE) 
                      select l.TRADE_DATE, l.TICKER, l.REQ_TYPE, l.DATA_SOURCE, l.PRICE from s_price as l 
                      left outer join d_price as r on 
                      l.TRADE_DATE = r.TRADE_DATE and l.TICKER = r.TICKER  and l.REQ_TYPE = r.REQ_TYPE and   l.DATA_SOURCE = r.DATA_SOURCE where r.TRADE_DATE is null and r.TICKER is null and r.REQ_TYPE is null and r.DATA_SOURCE is null ;''');
#    cursor.executemany("insert into s_price(TRADE_DATE, TICKER,REQ_TYPE,PRICE,DATA_SOURCE) values (%s, %s,%s, %s,%s)", vals )
#    cursor.execute("update d_price set PRICE = %s where  TRADE_DATE = %s and TICKER = %s " , ('189', '2018-08-01', 'SHY US Equity') )
    cursor.execute('''update d_price as l inner join s_price as r on
                       l.TRADE_DATE = r.TRADE_DATE and l.TICKER = r.TICKER  and l.REQ_TYPE = r.REQ_TYPE and l.DATA_SOURCE = r.DATA_SOURCE  set l.PRICE = r.PRICE ;''')
    cursor.execute('''delete from s_price;''')
    con.commit()
    con.close()