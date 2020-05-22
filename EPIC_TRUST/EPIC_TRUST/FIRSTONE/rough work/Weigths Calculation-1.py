# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:10:00 2018

@author: V Vardhan
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
timestamp =  int(datetime.now().strftime("%Y%m%d%H%M%S"))/1000000

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

def imp_f_calc(START_DATE, END_DATE, PORTFOLIO, INDEX_ID, DESCRIPTION,VARS,SORT_ON):  
    
#    START_DATE = '2018-07-01'
#    END_DATE = '2018-07-10'
#    PORTFOLIO  = ''
#    INDEX_ID = ''
#    DESCRIPTION = ''
#    VARS = ''       
#    SORT_ON = ''
        
    if PORTFOLIO == '':
        port = ''       
    else:
        port = 'a.PORTFOLIO in (' + "','".join(str(e) for e in PORTFOLIO) + ') and '
    
    if INDEX_ID == '':
        index = ' ' 
    else:
        index = 'a.INDEX_ID in (' + ','.join(str(e) for e in INDEX_ID) + ') and '
        
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
             where {} a.TRADE_DATE between '{}' and '{}' {} {}
             {}; '''
             
    Q = QUE.format(var_names_o,cond, START_DATE, END_DATE,str1,desc,order_o)
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")        
    Meas = pd.read_sql(Q, con=con)
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
############     CALCULATION DATES DETERMINATION      #####################################################
##TRADING DAYS LIST
#imp_d_price('E',1,'2018-07-01','2018-07-05',TICKER_LIST,'PX_SETTLE','BLOOMBERG')
###### CONSTANTS
COL_NAMES = ['Date','SPYG','SPY','SLYG','IWF','SHY']
IND_TICKER_LIST =  ['SPY US Equity','SPYG US Equity','SLYG US Equity','IWF US Equity']
TICKER_LIST = ['SPY US Equity','SPYG US Equity','SLYG US Equity','IWF US Equity','SHY US Equity']
TICKER_START_DATE = ['1993-01-29','2000-09-29','2000-09-29','2000-05-26','2002-07-26']
TICKER_NAMES = []
BT_START_DATE = datetime.strptime('31-12-2004', '%d-%m-%Y')
CALENDAR_ID=1

####### INITIALIZATION
SAVE_PRICE = pd.DataFrame(columns = COL_NAMES)
SAVE_INDICATORS = pd.DataFrame( )
SAVE_SIGNALS = pd.DataFrame( )
SAVE_LIGHTS = pd.DataFrame( )
SAVE_EXPOSURE = pd.DataFrame( )
INDEX_LEVEL = pd.DataFrame(columns = ['INDEX_VALUE'] )

##CALCULATION DAYS LIST
CALC_START_DATE = '2004-12-31'
CALC_END_DATE = '2018-06-30'
CDL = TDL(CALC_START_DATE,CALC_END_DATE,CALENDAR_ID) 
NO_CALDAYS = len(CDL)

for fk in  range(0,NO_CALDAYS):

    CALC_DATE = str(CDL[fk])
#    CALC_DATE_INDEX = TDL[TDL['Date'] == CALC_DATE].index
#    CP_CALC_DATE = imp_d_price('E',1,'2018-07-01','2018-07-05',TICKER_LIST,'PX_SETTLE','BLOOMBERG')
#    CP.merge(pd.Series(CALC_DATE).to_frame('Date'), left_index=False, right_index=False)

    ########Fetching month end dates###########################
    Monthendlist = imp_Nth_date(CALENDAR_ID, 'LAST', '', 'I', TICKER_START_DATE[0], MNTH_OFFSET(TICKER_START_DATE[0],CALC_DATE,'I'))
    
    if CALC_DATE == Monthendlist.iloc[-1] :

###################################       MACD SIGNAL       #################################################
        print(CP_CALC_DATE)
        ########Calculating 12EMA
        START_DATE = str(Monthendlist.loc[0,'TRADE_DATE'])
        END_DATE = str(Monthendlist.loc[len(Monthendlist.index)-1,'TRADE_DATE'])
        CP_MACD = imp_d_price('E',CALENDAR_ID,START_DATE,END_DATE,['SPY US Equity','SPYG US Equity','SLYG US Equity','IWF US Equity'],['PX_SETTLE'],'BLOOMBERG')
        
        macd, macdsignal, macdhist_IWF = talib.MACD(CP_MACD['IWF US Equity'].values, fastperiod=12, slowperiod=26, signalperiod=9)
        macd, macdsignal, macdhist_SPY = talib.MACD(CP_MACD['SPY US Equity'].values, fastperiod=12, slowperiod=26, signalperiod=9)
        macd, macdsignal, macdhist_SPYG = talib.MACD(CP_MACD['SPYG US Equity'].values, fastperiod=12, slowperiod=26, signalperiod=9)
        macd, macdsignal, macdhist_SLYG = talib.MACD(CP_MACD['SLYG US Equity'].values, fastperiod=12, slowperiod=26, signalperiod=9)
        
        ########INDICATOR DETERMINATION
        IND2=pd.concat([pd.DataFrame(macdhist_SPYG),pd.DataFrame(macdhist_SPY),pd.DataFrame(macdhist_SLYG),
                   pd.DataFrame(macdhist_IWF)],axis=1)
        IND2 = IND2[-2:] 
        IND2.columns = IND_TICKER_LIST
        
###############################        200DMA SIGNAL         ####################################################
        ########Fetching last 300 dates###########################
        TM250 = WORKDAY(CALC_DATE,CALENDAR_ID,-250)
        
        CP_175DMA = imp_d_price('',CALENDAR_ID,TM250,CALC_DATE,['SPY US Equity','SPYG US Equity','SLYG US Equity','IWF US Equity'],['PX_SETTLE'],'BLOOMBERG')
        ########Calculating 200DMA
        DMA175 = pd.DataFrame( )
        DMA175['Date'] = CP_175DMA.index
        DMA175 = DMA175.set_index('Date')
        DMA175['SPYG US Equity']=talib.SMA(CP_175DMA['SPYG US Equity'].values,timeperiod=175)
        DMA175['SPY US Equity']=talib.SMA(CP_175DMA['SPY US Equity'].values,timeperiod=175)
        DMA175['SLYG US Equity']=talib.SMA(CP_175DMA['SLYG US Equity'].values,timeperiod=175)
        DMA175['IWF US Equity']=talib.SMA(CP_175DMA['IWF US Equity'].values,timeperiod=175)
        ########INDICATOR DETERMINATION
        
        TEMP2 = pd.DataFrame(   )
        TEMP2[IND_TICKER_LIST] = CP_175DMA - DMA175
        TEMP2['TRADE_DATE'] = CP_175DMA.index
        IND1 = pd.DataFrame(   )
        IND1 = Monthendlist.merge(TEMP2, left_index=False, right_index=False) 
        IND1 = IND1[-2:]
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
        IND4 = (T10Y2Y_ME.loc[len(T10Y2Y_ME)-19:len(T10Y2Y_ME)-8,'T10Y2Y'] < 0).sum() > 0

################################           Weights Determination           #######################################
        GOLDEN_EXPOSURE = pd.Series([.6,.2,.1,.1,0])

        ##################################          LIGHTS DETERMINATION          ######################################
        IND1 [ IND1>0 ] = 1  ###SECURITY > 200DMA
        IND1 [ IND1<0 ] = -1  ###SECURITY <= 200DMA
        IND2 [ IND2>0 ] = 1  ### 12EMA > 26EMA
        IND2 [ IND2<0 ] = -1  ### 12EMA <= 26EMA

        IND3 = (IND1.values + IND2.values)/2

################################          EXPOSURE DETERMINATION           ########################################
        DIVEST= 0
        EXPOSURE = [0,0,0,0,0]
        if CALC_DATE == BT_START_DATE :
            INDEX_LEVEL.loc[fk,'INDEX_VALUE'] = 100
            EXPOSURE = GOLDEN_EXPOSURE
        else :
            if IND4 :
                    ##### All lights are red
                if IND3[-1].sum() == -4 :
                    EXPOSURE = [0,0,0,0,1]
                    ##### Rest of the scenarios
                else :
                    EXPOSURE = (GOLDEN_EXPOSURE+ GOLDEN_EXPOSURE.multiply(pd.Series(IND3[-1]).append(pd.Series([0]), ignore_index=True))) * 0.5
                    EXPOSURE[4] = 1- EXPOSURE.sum()
            else :

                for j in range(len(IND_TICKER_LIST)):

                    ################## GREEN SIGNAL ####################
                    if IND3[-1][j] == 1:
                        EXPOSURE[j] = GOLDEN_EXPOSURE[j]
                    ################## RED SIGNAL  ######################
                    elif IND3[-1][j] == -1:
                        EXPOSURE[j] = GOLDEN_EXPOSURE[j] * 0.5
                        DIVEST = DIVEST + 0.5 * GOLDEN_EXPOSURE[j]
                    else :
                        #################  YELLOW SIGNAL WITH RED MEMORY ########################
                        if IND3[0][j] == -1:
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

########################       WRITING VALUES TO EXCEL FILE IN DESIRED FORMAT        #######################################
        SAVE_LIGHTS.columns = ['Date'] +TICKER_LIST
        SAVE_EXPOSURE.columns = COL_NAMES
        
    #Exporting to f_calc
        SAVE_EXPOSURE['RUNTIMEID'] = timestamp / 1000000
        SAVE_LIGHTS['RUNTIMEID'] = timestamp / 1000000
        exp_f_calc(SAVE_EXPOSURE)
        exp_f_calc(SAVE_LIGHTS)


BT_WEIGTHS_CSV(SAVE_EXPOSURE,CALC_START_DATE,CALC_END_DATE)

del SAVE_PRICE,SAVE_INDICATORS,SAVE_SIGNALS,SAVE_LIGHTS,SAVE_EXPOSURE