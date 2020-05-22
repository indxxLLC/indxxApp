# -*- coding: utf-8 -*-
"""
Index code using  TR Series values.
"""

#Removes all variables
#%reset -f

import pandas as pd
import numpy as np
import talib
#from fredapi import Fred
import pandas_datareader.data as web
import requests
import pymysql as ms
#import os
#import sys
#scriptpath = "C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\functions.py"
#sys.path.append("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\functions.py")
#import functions as func
import time
from datetime import datetime
timestamp =  int(datetime.now().strftime("%Y%m%d%H%M%S"))

def EMA1(CDATA,CDATE,PDATE,PERIOD,TICKER_LIST):

    x4=pd.ExcelFile("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\EMA\\EMA SHEET-"+str(PERIOD)+".xlsx")
    HIST=x4.parse(str(PERIOD))
    PREV = HIST.merge(pd.Series(PDATE).to_frame('Date'), left_index=False, right_index=False)
    EMAP = pd.DataFrame(columns = [['Date']+TICKER_LIST] )
    EMAP.loc[0,'Date'] = CDATE
    EMAP[TICKER_LIST] = np.asarray(PREV.iloc[0,1:5].values * (PERIOD-1)/(PERIOD+1) + CDATA.iloc[0,1:5].values * 2/(PERIOD+1))

    if (CDATE == HIST['Date']).sum() >0 :
        HIST.loc[CDATE == HIST['Date'],TICKER_LIST] = np.array(EMAP[TICKER_LIST])
    else :
        HIST = HIST.append( EMAP, ignore_index = True )[EMAP.columns.tolist()]

    writer =pd.ExcelWriter("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\EMA\\EMA SHEET-"+str(PERIOD)+".xlsx" ,engine ='xlsxwriter')
    HIST.to_excel(writer,str(PERIOD),index = False)

    return HIST

def WEIGTHS_CSV(Weights,DATE1):
    df_csv = pd.DataFrame(columns = ['code','ticker','isin','name','curr','divcurr','sedol','cusip','countryname', \
                                     'sector','industry','subindustry','share','weight'])
    df_csv['code'] = ['ABCDE','ABCDE','ABCDE','ABCDE','ABCDE']
    df_csv['ticker'] = ['SPYG US Equity','SPY US Equity','IWO US Equity','IWF US Equity','SHY US Equity']
    df_csv['isin'] = ['US78464A4094','US78462F1030','US4642876480','US4642876142','US4642874576']
    df_csv['name'] = ['SPDR S&P 500 Growth ETF','SPDR S&P 500 ETF','iShares Russell 2000 Growth ETF', \
                      'iShares Russell 1000 Growth ETF','iShares 1-3 Year Treasury Bond ETF']
    df_csv['curr'] = ['USD','USD','USD','USD','USD']
    df_csv['divcurr'] = ['USD','USD','USD','USD','USD']
    df_csv['countryname'] = ['United States','United States','United States','United States','United States']
    df_csv['weight'] = Weights

    df_csv.to_csv("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\EXPOSURE DATA\\ABCD_LIVE_" \
                            +DATE1.strftime("%d-%m-%Y")+".csv",index = False)

def BT_WEIGTHS_CSV(BT_Weights,Start,End):

    ISIN_ARRAY = ['US78464A4094','US78462F1030','US4642876480','US4642876142','US4642874576']
    df_csv = pd.DataFrame()
    for k in range(BT_Weights.shape[0]) :
        for l in range(BT_Weights.shape[1]-1):
            df_csv = df_csv.append(pd.Series([k+1,ISIN_ARRAY[l],BT_Weights.iloc[k,l+1]]), ignore_index = True)
    df_csv.columns = ['Period','ISIN','Weights']
    df_csv.to_csv("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\BACKTEST\\ABCDE_BT_" \
                            +Start.strftime("%d-%m-%Y")+"-"+End.strftime("%d-%m-%Y")+".csv",index = False)


def WORKDAY(CALC_DATE,CALENDAR_ID,OFFSET):
#    CALC_DATE = '2018-07-01'
#    CALENDAR_ID = 1
#    OFFSET = -1
    import pymysql as ms
    import pandas as pd
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")

    if (OFFSET < 0):
        OFFSET = abs(OFFSET)
        QUE = '''SELECT TRADE_DATE from d_calendar where CALENDAR_ID = {0} and TRADING_DAY = 1 and TRADE_DATE < '{1}' order by TRADE_DATE desc'''
        Q = QUE.format(CALENDAR_ID,CALC_DATE)
        Meas = pd.read_sql(Q, con=con)
        OP = Meas.iloc[OFFSET-1]

    elif(OFFSET > 0):
        OFFSET = abs(OFFSET)
        QUE = '''SELECT TRADE_DATE from d_calendar where CALENDAR_ID = {0} and TRADING_DAY = 1 and TRADE_DATE > '{1}' order by TRADE_DATE'''
        Q = QUE.format(CALENDAR_ID,CALC_DATE)
        Meas = pd.read_sql(Q, con=con)
        OP = Meas.iloc[OFFSET-1]

    else:
        OP = CALC_DATE

    con.close()
     
    OP = OP[0].strftime('%Y-%m-%d')    
    return (OP)

def Reload(DATE,INDEX_ID):
    #Getting Required requests
    QUE = "select * from d_dailydatareq where INDEX_ID = {0}"
    Q = QUE.format(INDEX_ID)

    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
    Meas = pd.read_sql(Q, con=con)
    con.close()

    Meas = Meas.drop(columns = {"SLNO", "VALID_FLAG"})# Dropping serial Number
    #Seperating Request Types
    CA_REQ = Meas[Meas["FIELD"] == 'CA']
    PRICE_REQ = Meas[Meas["FIELD"] == 'PX_SETTLE']
    CURR_REQ = Meas[Meas["FIELD"] == 'CURR']
    #Fetching data for corresponding Request types.
    #CA IMPORT
    if (len(CA_REQ) > 0):
        r_data = CA_DATALOAD(DATE).drop(columns = {"VALUES"}).rename(columns = {'IDENTIFIER':'ISIN'})
        CA_dat = pd.merge(CA_REQ[['ISIN']],r_data,on = 'ISIN', how='left',left_index=False, right_index=False)
        CA_dat = CA_dat[["ACTION_ID","CORPORATE_ACTION","COUNTRY_CODE","CURRENCY","DATAPROVIDER","EX_DATE","ISIN",
                         "IDENTIFIER_NAME","MODIFY_DATE","NAME","RECORD_DATE","STATUS","SYMBOL","TICKER",]]
        CA_dat = CA_dat.dropna()
        vals = CA_dat.values.tolist()
        d_ca_DATALOAD(vals)

    #PRICE IMPORT
    if (len(PRICE_REQ) > 0):
        r_data = PRICE_DATALOAD(DATE)
        PRICE_dat = pd.merge(PRICE_REQ[['ISIN','TICKER','FIELD']],r_data[['ISIN','DATE','PRICE']],on = 'ISIN',how='left',left_index=False, right_index=False)
        PRICE_dat['DATA_SOURCE'] = 'BLOOMBERG'
        PRICE_dat = PRICE_dat.drop(columns = {"ISIN"})
        PRICE_dat = PRICE_dat[['DATE','TICKER','FIELD','PRICE','DATA_SOURCE']]
        PRICE_dat = PRICE_dat.dropna()
        vals = PRICE_dat.values.tolist()
        d_price_DATALOAD(vals)

    #CURR IMPORT
    if (len(CURR_REQ) > 0):
        r_data = CURR_DATALOAD(DATE).rename(columns = {'CURRENCY_TICKER':'TICKER'})
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

def MNTH_OFFSET(date1 , date2, IOE):
    date1 = datetime.strptime(str(date1), '%Y-%m-%d')
    date2 = datetime.strptime(str(date2), '%Y-%m-%d')
    if (IOE == 'I'):
        if (date2 > date1):        
            MNTH_OFFSET = (date2.year - date1.year) * 12 + (date2.month - date1.month) +  1 
        else:
            MNTH_OFFSET = (date1.year - date2.year) * 12 + (date1.month - date2.month) + 1
    else:
        if (date2 > date1):        
            MNTH_OFFSET = (date2.year - date1.year) * 12 + (date2.month - date1.month)
        else:
            MNTH_OFFSET = (date1.year - date2.year) * 12 + (date1.month - date2.month)
    return(MNTH_OFFSET)
    
def TDL(START_DATE,END_DATE,CALENDAR_ID):
#    START_DATE = '2018-07-01'
#    END_DATE = '2018-07-10'
#    CALENDAR_ID = 1
    import pymysql as ms
    import pandas as pd
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")

    QUE = '''SELECT TRADE_DATE from d_calendar where CALENDAR_ID = {0} and TRADE_DATE >= '{1}' and TRADE_DATE <= '{2}' 
     and TRADING_DAY = 1 order by TRADE_DATE asc'''
    Q = QUE.format(CALENDAR_ID,START_DATE,END_DATE)
    Meas = pd.read_sql(Q, con=con)

    con.close()
    Meas=Meas.values.tolist()
    Meas = [item for sublist in Meas for item in sublist]  
    return (Meas)

def imp_f_calc(START_DATE, END_DATE,SECURITY_NAME, PORTFOLIO, INDEX_ID, DESCRIPTION,VARS,SORT_ON):   
    if PORTFOLIO == '':
        port = ''       
    else:
        port = 'a.PORTFOLIO in (' + "','".join(str(e) for e in PORTFOLIO) + ') and '
    
    if INDEX_ID == '':
        index = ' ' 
    else:
        index = 'a.INDEX_ID in (' + ','.join(str(e) for e in INDEX_ID) + ') and '
        
    if SECURITY_NAME == '' :
        str2 = ' '
        sec_name = ''
    else:
        str2 = 'and a.SECURITY_NAME in'
        if (len(SECURITY_NAME) > 1):
            sec_name = tuple(SECURITY_NAME)
        else:
            sec_name = tuple(SECURITY_NAME) + ('filler_DOnt_care',)
        
    if DESCRIPTION == '' :
        str1 = ' '
        desc = ''
    else:
        str1 = 'and a.DESCRIPTION in'
        if (len(DESCRIPTION) > 1):
            desc = tuple(DESCRIPTION)
        else:
            desc = tuple(DESCRIPTION) + ('filler_DOnt_care',)
    
    if VARS == '':
        var_names_o = 'a.*'
    else:    
        var_names = ''        
        for i in VARS:
            var_names1 = 'a.' + i + ','
            var_names = var_names1 + var_names
        var_names_o = var_names[:-1]
        
    if SORT_ON == '':
        order_o = 'order by a.TRADE_DATE,a.INDEX_ID,a.PORTFOLIO'
    else:
        order = ''
        for i in SORT_ON:
            order1 = 'a.' + i + ','
            order = order1 + order
        order_1 = 'order by ' + order
        order_o = order_1[:-1]
            
    cond = port + index 
    QUE = '''select {}
             from f_calc as a 
             inner join
             (select max(RUNTIMEID) as RUNTIMEID from f_calc  group by  TRADE_DATE,INDEX_ID,PORTFOLIO,DESCRIPTION) as b
             on a.RUNTIMEID = b.RUNTIMEID
             where {} a.TRADE_DATE between '{}' and '{}' {} {} {} {}
             {}; '''
             
    Q = QUE.format(var_names_o,cond, START_DATE, END_DATE,str1,desc,str2,sec_name,order_o)
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")        
    Meas = pd.read_sql(Q, con=con)
    Meas = Meas.drop_duplicates()
    con.close()
    del var_names, order
    return Meas

def imp_Nth_date(CALENDAR_ID, TR_DAY_MONTH, BOA, IOE, DATE, MNTH_OFFSET):
    if (BOA == 'B'):
        BORF = '<'
        order = 'desc'
    else:
        BORF = '>'
        order ='' 
        
    if (IOE == 'I'):
        IORE = '='
    else:
        IORE = ' '
    
    SIGN = BORF + IORE
    
    if (TR_DAY_MONTH == 'LAST'):
        QUE = ''' select TRADE_DATE from (
                    SELECT   max(TRADE_DATE) as TRADE_DATE
                    FROM     d_calendar
                    where CALENDAR_ID = {} and TRADING_DAY = 1 
                    group by YEAR, month) as a 
                 where a.TRADE_DATE {} '{}'
                 order by TRADE_DATE {}; '''
        Q = QUE.format(CALENDAR_ID, SIGN, DATE, order)
        con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
        Meas = pd.read_sql(Q, con=con)
        con.close()   
        
    else:
        TR_DAY_MONTH = int(TR_DAY_MONTH)
        QUE = '''select distinct TRADE_DATE  from d_calendar where TRADING_DAY = 1 and TR_DAY_MONTH  = {} and TRADE_DATE {}  '{}' and CALENDAR_ID = {} order by TRADE_DATE {}'''
        Q = QUE.format(TR_DAY_MONTH, SIGN, DATE, CALENDAR_ID, order)
        con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
        Meas = pd.read_sql(Q, con=con)
        con.close() 
    
    Op = Meas.iloc[0:MNTH_OFFSET]
    return Op 

def TR_SERIES(TICKER,CALENDAR_ID,TRADE_DATE,INDEX_ID):  
    ########  Fetch the entire history of prices for the ticker
    PR_SERIES = imp_d_price('',CALENDAR_ID,'1900-01-01',TRADE_DATE, TICKER, ['PX_SETTLE'], 'BLOOMBERG')
    ######## Fetch the entire period divisors <= TRADE_DATE along with VALID_FROM to VALID_TO
    DIVISORS = imp_f_calc('1900-01-01', TRADE_DATE, TICKER,'0', str(INDEX_ID), ['Period_Divisor'],['VALUE','VALID_FROM'],['VALID_FROM'])
    DIVISORS = DIVISORS.drop_duplicates(subset=['VALUE','VALID_FROM']).sort_values(by='VALID_FROM', ascending=True)
    
    DIVISORS['MUTIPLIER']  = DIVISORS.VALUE
    DIVISORS = DIVISORS.sort_values(by='VALID_FROM', ascending=False).reset_index()
    
    DIVISORS.loc[0,'MUTIPLIER'] = 1
    DIVISORS['MUTIPLIER']  = DIVISORS.MUTIPLIER.cumprod()
    
    DIVISORS['VALID_FROM'] = DIVISORS['VALID_FROM'].apply(lambda x:str(x))       
    PR_SERIES['TRADE_DATE'] = PR_SERIES.index
    PR_SERIES['TRADE_DATE'] = PR_SERIES['TRADE_DATE'].apply(lambda x:str(x))
    
    temp = PR_SERIES.merge(DIVISORS, left_on = 'TRADE_DATE', right_on = 'VALID_FROM', how = 'left', left_index=False, right_index=False) 
    temp = temp.sort_values(by='TRADE_DATE', ascending=True)
    
    temp['VALUE'] = temp['VALUE'].fillna(method='ffill')
    temp['MUTIPLIER'] = temp['MUTIPLIER'].fillna(method='ffill')
    t1 = temp[['TRADE_DATE','VALID_FROM',TICKER[0],'MUTIPLIER','VALUE']].sort_values(by='TRADE_DATE', ascending=False)  

    t1['TR_SERIES'] = t1['MUTIPLIER'] * t1[TICKER[0]]
    t1['TRADE_DATE'] = t1['TRADE_DATE'].apply(lambda x:str(x))
#    writer = pd.ExcelWriter('C:\\Users\\Administrator\\Desktop\\'+j+'TR.xlsx')
#    t1.to_excel(writer,j)
#    writer.save()
    return(t1)  

def exp_f_calc(vals,INDEX_ID,TRADE_DATE,RANGE_BREAK_DESC) : 
    
    if (RANGE_BREAK_DESC == ''):
        con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
        cursor = con.cursor() 
        cursor.executemany("insert into f_calc(RUNTIMEID,TRADE_DATE, INDEX_ID, SECURITY_NAME, PORTFOLIO, DESCRIPTION, VALUE, VALID_FLAG, VALID_FROM, VALID_TO) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;", vals)
        con.commit()
        con.close()    
    
    else:    
        if (len(RANGE_BREAK_DESC) > 1):
            desc = tuple(RANGE_BREAK_DESC)
        else:
            desc = tuple(RANGE_BREAK_DESC) + ('filler_DOnt_care',)                   
        con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
        cursor = con.cursor() 
        cursor.executemany("insert into f_calc(RUNTIMEID,TRADE_DATE, INDEX_ID, SECURITY_NAME, PORTFOLIO, DESCRIPTION, VALUE, VALID_FLAG, VALID_FROM, VALID_TO) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;", vals)
        con.commit()
        
        QUE = '''select INDEX_ID, DESCRIPTION, PORTFOLIO,max(RUNTIMEID) as RUNTIMEID from f_calc 
        where INDEX_ID = {} and DESCRIPTION in  {}
        group by INDEX_ID, DESCRIPTION, PORTFOLIO'''
        Q = QUE.format(INDEX_ID, desc)
        Meas = pd.read_sql(Q, con=con)
        
        for i in Meas.index:
            runid = Meas.loc[i,'RUNTIMEID']
            in_id = Meas.loc[i,'INDEX_ID']
            var = Meas.loc[i,'DESCRIPTION']
            cursor.execute("update f_calc set VALID_TO = DATE(%s - INTERVAL 1 DAY) where DESCRIPTION = %s and RUNTIMEID != %s and INDEX_ID = %s;" , (TRADE_DATE,var,str(runid),in_id))
        
        con.commit()
        con.close()
        
def imp_d_price(EOA, CALENDAR_ID, START_DATE, END_DATE, TICKER, REQ_TYPE, DATA_SOURCE):    

    if (len(TICKER) > 1):
        tick = tuple(TICKER)
    else:
        tick = tuple(TICKER) + ('filler_DOnt_care',)
     
    if REQ_TYPE == '' :
        str1 = ' '
        req_type = ''
    else:
        str1 = 'and l.REQ_TYPE in'
        if (len(REQ_TYPE) > 1):
            req_type = tuple(REQ_TYPE)
        else:
            req_type = tuple(REQ_TYPE) + ('filler_DOnt_care',)
    
    if EOA == 'E':
        sql1 = '''SELECT   MAX(TRADE_DATE) as TRADE_DATE FROM d_calendar where TRADING_DAY = 1 and CALENDAR_ID = {} and     TRADE_DATE  between '{}' and '{}' GROUP BY MONTH(TRADE_DATE), YEAR(TRADE_DATE)'''
    else:
        sql1 = '''SELECT  distinct TRADE_DATE FROM  d_calendar
            WHERE CALENDAR_ID = {} and TRADE_DATE BETWEEN '{}' and '{}' and TRADING_DAY = 1'''
    sql = sql1.format(CALENDAR_ID,START_DATE, END_DATE)
    
    QUE = '''select l.TRADE_DATE,l.TICKER,l.PRICE,l.REQ_TYPE from d_price as l 
            INNER JOIN ({}) as r
            on l.TRADE_DATE = r.TRADE_DATE
            where l.TICKER in {} {} {} and l.DATA_SOURCE = '{}'; '''
            
    Q = QUE.format(sql, tick, str1, req_type, DATA_SOURCE)
    
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
    Meas = pd.read_sql(Q, con=con)
    con.close()   
    Pivo = Meas.pivot(index = 'TRADE_DATE' ,columns='TICKER', values= 'PRICE')
    return(Pivo) 
#%reset -f
############     CALCULATION DATES DETERMINATION      #####################################################
##TRADING DAYS LIST
#imp_d_price('E',1,'2018-07-01','2018-07-05',TICKER_LIST,'PX_SETTLE','BLOOMBERG')
###### CONSTANTS
COL_NAMES = ['SPY','SPYG','SLYG','IWF','SHY']
FINAL_LIST = ['SPY US EQUITY', 'SPYG US EQUITY', 'SLYG US EQUITY', 'IWF US EQUITY', 'SHY US EQUITY']
#IND_TICKER_LIST =  ['SPY US Equity','SPYG US Equity','SLYG US Equity','IWF US Equity']
IND_TICKER_LIST =  ['SPY US EQUITY','SPYG US EQUITY','SLYG US EQUITY','IWF US EQUITY']
#TICKER_LIST = ['SPYG US Equity','SPY US Equity','SLYG US Equity','IWF US Equity']
TICKER_START_DATE = ['1993-01-29','2000-09-29','2000-09-29','2000-05-26','2002-07-26']
TICKER_NAMES = []
BT_START_DATE = datetime.strptime('31-12-2004', '%d-%m-%Y')
CALENDAR_ID=1
INDEX_ID = 1
####### INITIALIZATION
SAVE_PRICE = pd.DataFrame(columns = COL_NAMES)
SAVE_INDICATORS = pd.DataFrame( )
SAVE_SIGNALS = pd.DataFrame( )
SAVE_LIGHTS = pd.DataFrame( )
INDEX_LEVEL = pd.DataFrame(columns = ['INDEX_VALUE'] )

##CALCULATION DAYS LIST
CALC_START_DATE = '2004-12-01'
CALC_END_DATE = '2018-07-31'
CDL = TDL(CALC_START_DATE,CALC_END_DATE,CALENDAR_ID) 
NO_CALDAYS = len(CDL)
ST = time.time()

IND_1ALL  = pd.DataFrame()
IND_1ALL_BIN  = pd.DataFrame()
IND_2ALL  = pd.DataFrame()
IND_2ALL_BIN  = pd.DataFrame()
IND_3ALL_BIN  = pd.DataFrame()

for fk in  range(0,NO_CALDAYS):

    CALC_DATE = CDL[fk] 

    ########Fetching month end dates###########################
    Monthendlist = imp_Nth_date(CALENDAR_ID, 'LAST', '', 'I', TICKER_START_DATE[0], MNTH_OFFSET(TICKER_START_DATE[0],CALC_DATE,'I'))
    
    if str(CALC_DATE) == str(Monthendlist.iloc[-1].TRADE_DATE):
        print(CALC_DATE)
###################################       MACD SIGNAL       #################################################
#        print(CP_CALC_DATE)
        ########Calculating 12EMA
#        START_DATE = str(Monthendlist.loc[0,'TRADE_DATE'])
        Monthendlist['TRADE_DATE'] = Monthendlist['TRADE_DATE'].apply(lambda x:str(x))
        END_DATE = str(Monthendlist.loc[len(Monthendlist.index)-1,'TRADE_DATE'])

#TR Series Calculation        
        SPY_TR = TR_SERIES(['SPY US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
        SPYG_TR = TR_SERIES(['SPYG US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
        SLYG_TR = TR_SERIES(['SLYG US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
        SHY_TR = TR_SERIES(['SHY US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
        IWF_TR = TR_SERIES(['IWF US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
        
        SPY_TR_m_end = Monthendlist.merge(SPY_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)
        SPYG_TR_m_end = Monthendlist.merge(SPYG_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)
        SLYG_TR_m_end = Monthendlist.merge(SLYG_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)       
        SHY_TR_m_end = Monthendlist.merge(SHY_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)       
        IWF_TR_m_end = Monthendlist.merge(IWF_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)
        
        macd, macdsignal, macdhist_IWF = talib.MACD(IWF_TR_m_end['TR_SERIES'].values, fastperiod=12, slowperiod=26, signalperiod=9)
        macd, macdsignal, macdhist_SPY = talib.MACD(SPY_TR_m_end['TR_SERIES'].values, fastperiod=12, slowperiod=26, signalperiod=9)
        macd, macdsignal, macdhist_SPYG = talib.MACD(SPYG_TR_m_end['TR_SERIES'].values, fastperiod=12, slowperiod=26, signalperiod=9)
        macd, macdsignal, macdhist_SLYG = talib.MACD(SLYG_TR_m_end['TR_SERIES'].values, fastperiod=12, slowperiod=26, signalperiod=9)
        
        ########INDICATOR DETERMINATION
        IND2=pd.concat([pd.DataFrame(macdhist_SPYG),pd.DataFrame(macdhist_SPY),pd.DataFrame(macdhist_IWF),pd.DataFrame(macdhist_SLYG)],axis=1)
        IND2 = IND2[-1:]   #####CHANGED
        IND2.columns = ['SPYG US EQUITY', 'SPY US EQUITY', 'IWF US EQUITY', 'SLYG US EQUITY']
        IND2 = IND2[['SPY US EQUITY', 'SPYG US EQUITY', 'SLYG US EQUITY', 'IWF US EQUITY']]
        ####################        200DMA SIGNAL         ####################################################
        ########Fetching last 250 dates###########################
        TM250 = WORKDAY(CALC_DATE,CALENDAR_ID,-250)
        DT_RANGE = pd.DataFrame()
        DT_RANGE['TRADE_DATE'] = TDL(TM250,CALC_DATE,CALENDAR_ID)
        DT_RANGE['TRADE_DATE'] = DT_RANGE['TRADE_DATE'].apply(lambda x:str(x))
#        CP_175DMA = imp_d_price('',CALENDAR_ID,TM250,CALC_DATE,['SPY US Equity','SPYG US Equity','SLYG US Equity','IWF US Equity'],['PX_SETTLE'],'BLOOMBERG')
        
        SPY_TR_CP_175DMA = DT_RANGE.merge(SPY_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)
        SPYG_TR_CP_175DMA = DT_RANGE.merge(SPYG_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)
        SLYG_TR_CP_175DMA = DT_RANGE.merge(SLYG_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)       
        SHY_TR_CP_175DMA = DT_RANGE.merge(SHY_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)       
        IWF_TR_CP_175DMA= DT_RANGE.merge(IWF_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)

        CP_175DMA = pd.DataFrame()
        CP_175DMA['SPY US EQUITY'] =  SPY_TR_CP_175DMA.TR_SERIES
        CP_175DMA['SPYG US EQUITY'] = SPYG_TR_CP_175DMA.TR_SERIES
#        CP_175DMA['SHY US Equity']= SHY_TR_CP_175DMA.TR_SERIES
        CP_175DMA['SLYG US EQUITY']= SLYG_TR_CP_175DMA.TR_SERIES
        CP_175DMA['IWF US EQUITY']= IWF_TR_CP_175DMA.TR_SERIES
        CP_175DMA['DATE'] = DT_RANGE['TRADE_DATE']      
        CP_175DMA = CP_175DMA.set_index('DATE')
        
        ########Calculating 200DMA
        DMA175 = pd.DataFrame( )
        DMA175['Date'] = DT_RANGE['TRADE_DATE']
        DMA175 = DMA175.set_index('Date')
        DMA175['SPYG US EQUITY']=talib.SMA(SPYG_TR_CP_175DMA['TR_SERIES'].values,timeperiod=175)
        DMA175['SPY US EQUITY']=talib.SMA(SPY_TR_CP_175DMA['TR_SERIES'].values,timeperiod=175)
        DMA175['SLYG US EQUITY']=talib.SMA(SLYG_TR_CP_175DMA['TR_SERIES'].values,timeperiod=175)
        DMA175['IWF US EQUITY']=talib.SMA(IWF_TR_CP_175DMA['TR_SERIES'].values,timeperiod=175)
        ########INDICATOR DETERMINATION
        
        TEMP2 = pd.DataFrame(   )
        CP_175DMA.sort_index(inplace=True)
        DMA175.sort_index(inplace=True)
        TEMP2[IND_TICKER_LIST] = CP_175DMA[IND_TICKER_LIST] - DMA175[IND_TICKER_LIST]
        TEMP2['TRADE_DATE'] = DMA175.index
        IND1 = pd.DataFrame(   )
        IND1 = Monthendlist.merge(TEMP2, how= 'left', on ='TRADE_DATE', left_index=False, right_index=False) 
        IND_1ALL = IND_1ALL.append(IND1.iloc[-1])
        IND_1ALL = IND_1ALL[IND_TICKER_LIST]
        IND1 = IND1[-1:]  ####  CHANGED
        del IND1['TRADE_DATE']
        
########################        TREASURY INVERSION         #####################################################
        ########Fetching last 500 dates###########################
        TM500 = WORKDAY(CALC_DATE,CALENDAR_ID,-500)
        INVERSION_DATES = TDL(TM500, CALC_DATE, CALENDAR_ID)
        start = INVERSION_DATES[0]
        end = INVERSION_DATES[-1]
        T10Y2Y = web.DataReader('T10Y2Y', 'fred', start, end) # END = CALC_DATE, START =  END - 24 MNTHS INCL
        T10Y2Y = T10Y2Y.ffill()
        
        T10Y2Y['TRADE_DATE'] = T10Y2Y.index
        T10Y2Y['TRADE_DATE'] = T10Y2Y['TRADE_DATE'].apply(lambda x:str(x.date()))
        Monthendlist['TRADE_DATE'] = Monthendlist['TRADE_DATE'].apply(lambda x:str(x))
        T10Y2Y_ME=Monthendlist.merge(T10Y2Y, left_index=False, right_index=False) 
        IND4 = int((T10Y2Y_ME.loc[len(T10Y2Y_ME)-19:len(T10Y2Y_ME)-8,'T10Y2Y'] < 0).sum() > 0)

################################           Weights Determination           #######################################
        GOLDEN_EXPOSURE = pd.Series([.6,.2,.1,.1,0])

        ##################################          LIGHTS DETERMINATION          ######################################
        IND_2ALL = IND_2ALL.append(IND2.iloc[-1])
        IND_2ALL = IND_2ALL[['SPY US EQUITY', 'SPYG US EQUITY', 'SLYG US EQUITY', 'IWF US EQUITY']]
###########
        IND1 [ IND1>0 ] = 1  ###SECURITY > 200DMA
        IND1 [ IND1<0 ] = -1  ###SECURITY <= 200DMA
        IND2 [ IND2>0 ] = 1  ### 12EMA > 26EMA
        IND2 [ IND2<0 ] = -1  ### 12EMA <= 26EMA

        IND3 = (IND1.values + IND2.values)/2
        IN3 = (IND1 + IND2)/2
        
        IND_1ALL_BIN = IND_1ALL_BIN.append(IND1.iloc[-1])
        IND_2ALL_BIN = IND_2ALL_BIN.append(IND2.iloc[-1])

        IND_1ALL_BIN = IND_1ALL_BIN[IND_TICKER_LIST]
        IND_2ALL_BIN = IND_2ALL_BIN[IND_TICKER_LIST]

        
################################          EXPOSURE DETERMINATION           ########################################
        DIVEST= 0
        EXPOSURE = [0,0,0,0,0]
        if CALC_DATE == BT_START_DATE :
            INDEX_LEVEL.loc[fk,'INDEX_VALUE'] = 100
            EXPOSURE = GOLDEN_EXPOSURE
        else :
            if IND4 :
                    ##### All lights are red
                    for j in range(len(IND_TICKER_LIST)):

                    ################## GREEN SIGNAL ####################
                        if IND3[-1][j] == 1:
                            EXPOSURE[j] = GOLDEN_EXPOSURE[j]
                    ################## RED SIGNAL  ######################
                        elif int(IND3[-1][j]) == -1:
                            EXPOSURE[j] = 0
                            DIVEST = DIVEST +  GOLDEN_EXPOSURE[j]
                        else :
                        #################  YELLOW SIGNAL ########################                            
                            TM1 = pd.DataFrame()
                            TM1 = imp_Nth_date(CALENDAR_ID, 'LAST', 'B', '', CALC_DATE.strftime('%Y-%m-%d'), 1)
                            LIGHTS_TM1 = imp_f_calc(str(TM1.loc[0,'TRADE_DATE']), str(TM1.loc[0,'TRADE_DATE']), [IND_TICKER_LIST[j]],'0', [INDEX_ID], ['LIGHTS'],['VALUE','VALID_FROM'],['VALID_FROM'])
                       
                            if (LIGHTS_TM1.loc[0,'VALUE'] == -1): 
                                IND3[-1][j] = 1
                                EXPOSURE[j] = GOLDEN_EXPOSURE[j]
                            ################ YELLOW SIGNAL WITHOUT RED MEMORY ####################
                            else :
                                EXPOSURE[j] = GOLDEN_EXPOSURE[j] * 0.5
                                DIVEST = DIVEST + 0.5 * GOLDEN_EXPOSURE[j]
                            
                    EXPOSURE[4] = DIVEST
            else :

                for j in range(len(IND_TICKER_LIST)):

                    ################## GREEN SIGNAL ####################
                    if IND3[-1][j] == 1:
                        EXPOSURE[j] = GOLDEN_EXPOSURE[j]
                    ################## RED SIGNAL  ######################
                    elif int(IND3[-1][j]) == -1:
                        EXPOSURE[j] = GOLDEN_EXPOSURE[j] * 0.5
                        DIVEST = DIVEST + 0.5 * GOLDEN_EXPOSURE[j]
                    else :
                        #################  YELLOW SIGNAL WITH RED MEMORY ########################
######   IMPORT PREVIOUS MONTHS LIGHTS and USE IT HERE 
#                        TM1 = WORKDAY(CALC_DATE,CALENDAR_ID,-1)
                        TM1 = pd.DataFrame()
                        TM1 = imp_Nth_date(CALENDAR_ID, 'LAST', 'B', '', CALC_DATE.strftime('%Y-%m-%d'), 1)
                        LIGHTS_TM1 = imp_f_calc(str(TM1.loc[0,'TRADE_DATE']), str(TM1.loc[0,'TRADE_DATE']), [IND_TICKER_LIST[j]],'0', [INDEX_ID], ['LIGHTS'],['VALUE','VALID_FROM'],['VALID_FROM'])
                       
                        if (LIGHTS_TM1.loc[0,'VALUE'] == -1): 
                            IND3[-1][j] = 1
                            EXPOSURE[j] = GOLDEN_EXPOSURE[j]
                            ################ YELLOW SIGNAL WITHOUT RED MEMORY ####################
                        else :
                            EXPOSURE[j] = GOLDEN_EXPOSURE[j] * 0.75
                            DIVEST = DIVEST + 0.25 * GOLDEN_EXPOSURE[j]

                #########################   SCENARIO - 1    ###################################
                ###################  INVESTMENT INTO GREEN LIGHTED COMPONENTS  #########################
                if (IND3[-1] == 1).sum() >0 :
                    EXPOSURE = EXPOSURE + (DIVEST / (IND3[-1] == 1).sum()) * np.append((IND3[-1] == 1)  * 1,EXPOSURE[4])

                ##############        INVESTMENT INTO TREASURIES      ################
                else:
                    EXPOSURE[4] = DIVEST

        ###################   EXPORTING EXPOSURE VALUES FOR EVERY DATE    ###################################


##################    END of CALCULATION LOOP    #####################################
     
########### EXPORT LIGHTS ALSO TO F _CALC 
        col = ['RUNTIMEID','TRADE_DATE','INDEX_ID','SECUITY_NAME','PORTFOLIO','DESCRIPTION','VALUE','VALID_FROM', 'VALID_TO']    
        SAVE_LIGHTS = pd.DataFrame(columns = col)
        l5 = IND3.tolist()
        l6 = l5[-1]
        l6.append(IND4)
        
        IND_3ALL_BIN = IND_3ALL_BIN.append(l6)
#        IND_3ALL_BIN = IND_3ALL_BIN[['SPY US Equity', 'SPYG US Equity', 'SLYG US Equity', 'IWF US Equity','SHY']]
        
        for i in range(0,len(l6)):
            SAVE_LIGHTS.loc[i,'SECUITY_NAME'] = FINAL_LIST[i]   
            SAVE_LIGHTS.loc[i,'VALUE'] = str(l6[i])
            SAVE_LIGHTS.loc[i,'RUNTIMEID'] = str(timestamp / 1000000)
            SAVE_LIGHTS.loc[i,'TRADE_DATE'] = str(CALC_DATE)
            SAVE_LIGHTS.loc[i,'VALID_FROM'] = str(CALC_DATE)
            SAVE_LIGHTS.loc[i,'VALID_TO'] = '2099-01-01'
            SAVE_LIGHTS.loc[i,'INDEX_ID'] = 1
            SAVE_LIGHTS.loc[i,'PORTFOLIO'] = 0
            SAVE_LIGHTS.loc[i,'VALID_FLAG'] = 'Y'
            SAVE_LIGHTS.loc[i,'DESCRIPTION'] = 'LIGHTS' 
            
        SAVE_LIGHTS = SAVE_LIGHTS[['RUNTIMEID','TRADE_DATE','INDEX_ID','SECUITY_NAME','PORTFOLIO','DESCRIPTION','VALUE','VALID_FLAG', 'VALID_FROM', 'VALID_TO']]
        vals = SAVE_LIGHTS.values.tolist()
        exp_f_calc(vals,1,str(CALC_DATE),'')
        
    #Exporting to f_calc   
        SAVE_EXPOSURE = pd.DataFrame(columns = col)
        EXPOSURE = list(EXPOSURE)
            
        for i in range(0,len(EXPOSURE)):
            SAVE_EXPOSURE.loc[i,'SECUITY_NAME'] = FINAL_LIST[i]   
            SAVE_EXPOSURE.loc[i,'VALUE'] = str(round(EXPOSURE[i],10))
            SAVE_EXPOSURE.loc[i,'RUNTIMEID'] = str(timestamp / 1000000)
            SAVE_EXPOSURE.loc[i,'TRADE_DATE'] = str(CALC_DATE)
            SAVE_EXPOSURE.loc[i,'VALID_FROM'] = str(CALC_DATE)
            SAVE_EXPOSURE.loc[i,'VALID_TO'] = '2099-01-01'
            SAVE_EXPOSURE.loc[i,'INDEX_ID'] = 1
            SAVE_EXPOSURE.loc[i,'PORTFOLIO'] = 0
            SAVE_EXPOSURE.loc[i,'VALID_FLAG'] = 'Y'
            SAVE_EXPOSURE.loc[i,'DESCRIPTION'] = 'EXPOSURE' 
            
        SAVE_EXPOSURE = SAVE_EXPOSURE[['RUNTIMEID','TRADE_DATE','INDEX_ID','SECUITY_NAME','PORTFOLIO','DESCRIPTION','VALUE','VALID_FLAG', 'VALID_FROM', 'VALID_TO']]
        vals = SAVE_EXPOSURE.values.tolist()
        exp_f_calc(vals,1,str(CALC_DATE),'')
            
        print('exported to f_calc for '+str(CALC_DATE))


#BT_WEIGTHS_CSV(SAVE_EXPOSURE,CALC_START_DATE,CALC_END_DATE)
#
#del SAVE_PRICE,SAVE_INDICATORS,SAVE_SIGNALS,SAVE_LIGHTS,SAVE_EXPOSURE
end = time.time()
print(end - ST)