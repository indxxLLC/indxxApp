# -*- coding: utf-8 -*-
"""
@author: ssstipirneni
"""
#Test Values

#Example :  -- > Reload('2018-08-06',1)
Reload(['2018-08-06','2018-08-07'],1)

import pymysql as ms
import pandas as pd
def Reload(DATE,INDEX_ID):
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
    
    #Getting Required requests
    QUE = "select * from d_dailydatareq where INDEX_ID = {0}"
    Q = QUE.format(INDEX_ID)       
    Meas = pd.read_sql(Q, con=con)
    Meas = Meas.drop(columns = {"SLNO", "VALID_FLAG"})# Dropping serial Number
    #Seperating Request Types
    CA_REQ = Meas[Meas["FIELD"] == 'CA']
    PRICE_REQ = Meas[Meas["FIELD"] == 'PX_SETTLE']
    CURR_REQ = Meas[Meas["FIELD"] == 'CURR']
    con.close()
    #Fetching data for corresponding Request types.
    #CA IMPORT
    if (len(CA_REQ) > 0):
        r_data = pd.DataFrame()
        for a in DATE:
            r_data_t = CA_DATALOAD(a).drop(columns = {"VALUES"}).rename(columns = {'IDENTIFIER':'ISIN'})  
            r_data = r_data.append(r_data_t)
        CA_dat = pd.merge(CA_REQ[['ISIN']],r_data,on = 'ISIN', how='left',left_index=False, right_index=False)
        CA_dat = CA_dat[["ACTION_ID","CORPORATE_ACTION","COUNTRY_CODE","CURRENCY","DATAPROVIDER","EX_DATE","ISIN",
                         "IDENTIFIER_NAME","MODIFY_DATE","NAME","RECORD_DATE","STATUS","SYMBOL","TICKER",]]
        CA_dat = CA_dat.dropna()
        vals = CA_dat.values.tolist()
        d_ca_DATALOAD(vals)
        
    #PRICE IMPORT    
    if (len(PRICE_REQ) > 0):  
        for a in DATE:
            r_data_t = PRICE_DATALOAD(a)
            r_data = r_data.append(r_data_t)
        PRICE_dat = pd.merge(PRICE_REQ[['ISIN','TICKER','FIELD']],r_data[['ISIN','DATE','PRICE']],on = 'ISIN',how='left',left_index=False, right_index=False)
        PRICE_dat['DATA_SOURCE'] = 'BLOOMBERG'
        PRICE_dat = PRICE_dat.drop(columns = {"ISIN"})
        PRICE_dat = PRICE_dat[['DATE','TICKER','FIELD','PRICE','DATA_SOURCE']]
        vals = PRICE_dat.values.tolist()
        d_price_DATALOAD(vals) 

    #CURR IMPORT    
    if (len(CURR_REQ) > 0):
        for a in DATE:
            r_data_t = CURR_DATALOAD(a).rename(columns = {'CURRENCY_TICKER':'TICKER'})
            r_data = r_data.append(r_data_t)
        CURR_dat = pd.merge(CURR_REQ[['TICKER','FIELD']],r_data[['TICKER','DATE','PRICE']],on = 'TICKER', how='left',left_index=False, right_index=False)
        CURR_dat['DATA_SOURCE'] = 'BLOOMBERG'
        CURR_dat = CURR_dat[['DATE','TICKER','FIELD','PRICE','DATA_SOURCE']]
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
    url = 'http://146.20.65.208/central_db_edi/api/getfutureca.php?type1=JSON&authcode=INDXX:931&date='+DATE
    temp3=requests.get(url).json()
    temp3 =temp3['data']
    rawdata=pd.DataFrame.from_dict(temp3, orient='columns')
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
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
    cursor = con.cursor() 
    cursor.execute('''delete from s_ca;''')
    cursor.executemany("insert into s_ca (ACTION_ID,CORPORATE_ACTION,COUNTRY_CODE,CURRENCY,DATAPROVIDER,EX_DATE,IDENTIFIER,IDENTIFIER_NAME,MODIFY_DATE,NAME,RECORD_DATE,STATUS,SYMBOL,TICKER) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",  vals)
    
    cursor.execute('''insert into d_ca (ACTION_ID,CORPORATE_ACTION,COUNTRY_CODE,CURRENCY,DATAPROVIDER
                                        ,EX_DATE,IDENTIFIER,IDENTIFIER_NAME,MODIFY_DATE,NAME,RECORD_DATE,STATUS,SYMBOL,TICKER) 
                         select l.ACTION_ID,
                                l.CORPORATE_ACTION,
                                l.COUNTRY_CODE,
                                l.CURRENCY,
                                l.DATAPROVIDER,
                                l.EX_DATE,
                                l.IDENTIFIER,
                                l.IDENTIFIER_NAME,
                                l.MODIFY_DATE,
                                l.NAME,
                                l.RECORD_DATE,
                                l.STATUS,
                                l.SYMBOL,
                                l.TICKER  from s_ca as l 
                          left outer join d_ca as r on 
                            l.ACTION_ID = r.ACTION_ID and
        								l.CORPORATE_ACTION = r.CORPORATE_ACTION and
        								l.COUNTRY_CODE = r.COUNTRY_CODE and
        								l.CURRENCY = r.CURRENCY and
        								l.DATAPROVIDER = r.DATAPROVIDER and
        								l.EX_DATE = r.EX_DATE and
        								l.IDENTIFIER = r.IDENTIFIER and
        								l.IDENTIFIER_NAME = r.IDENTIFIER_NAME and
        								l.MODIFY_DATE = r.MODIFY_DATE and
        								l.NAME = r.NAME and
        								l.RECORD_DATE = r.RECORD_DATE and
        								l.STATUS = r.STATUS and
        								l.SYMBOL = r.SYMBOL and
        								l.TICKER = r.TICKER 
                      where r.TICKER is null and r.SYMBOL is null and r.STATUS is null and r.IDENTIFIER is null and 
                      r.CORPORATE_ACTION is null and r.ACTION_ID is null ;''')
#    cursor.executemany("insert into s_price(TRADE_DATE, TICKER,REQ_TYPE,PRICE,DATA_SOURCE) values (%s, %s,%s, %s,%s)", vals )
#    cursor.execute("update  d_price set PRICE = %s where  TRADE_DATE = %s and TICKER = %s " , ('189', '2018-08-01', 'SHY US Equity'))
    cursor.execute('''update d_ca as l inner join s_ca as r on
                            l.ACTION_ID = r.ACTION_ID and
        								l.CORPORATE_ACTION = r.CORPORATE_ACTION and
        								l.COUNTRY_CODE = r.COUNTRY_CODE and
        								l.CURRENCY = r.CURRENCY and
        								l.DATAPROVIDER = r.DATAPROVIDER and
        								l.EX_DATE = r.EX_DATE and
        								l.IDENTIFIER = r.IDENTIFIER and
        								l.IDENTIFIER_NAME = r.IDENTIFIER_NAME and
        								l.MODIFY_DATE = r.MODIFY_DATE and
        								l.NAME = r.NAME and
        								l.RECORD_DATE = r.RECORD_DATE and
        								l.STATUS = r.STATUS and
        								l.SYMBOL = r.SYMBOL and
        								l.TICKER = r.TICKER
                       set l.ACTION_ID = r.ACTION_ID,
                            l.CORPORATE_ACTION = r.CORPORATE_ACTION,
                            l.COUNTRY_CODE = r.COUNTRY_CODE,
                            l.CURRENCY = r.CURRENCY,
                            l.DATAPROVIDER = r.DATAPROVIDER,
                            l.EX_DATE = r.EX_DATE,
                            l.IDENTIFIER = r.IDENTIFIER,
                            l.IDENTIFIER_NAME = r.IDENTIFIER_NAME,
                            l.MODIFY_DATE = r.MODIFY_DATE,
                            l.NAME = r.NAME,
                            l.RECORD_DATE = r.RECORD_DATE,
                            l.STATUS = r.STATUS,
                            l.SYMBOL = r.SYMBOL,
                            l.TICKER = r.TICKER ;''')
    cursor.execute('''delete from s_ca;''')
    con.commit()
    con.close()
        
def d_price_DATALOAD(vals) :   
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
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