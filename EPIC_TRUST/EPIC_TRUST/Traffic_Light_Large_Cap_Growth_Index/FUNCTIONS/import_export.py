# -*- coding: utf-8 -*-
"""
@author: Suraj SS Tipirneni
import from and export to f_calc
"""

#Import data from d_price  for ay date range for multiple Tickers and Req_Types.
#INDEX_ID = [1]/''
#REQ_TYPE = ['PX_SETTLE','PRICE']/''
#VARS = ['TRADE_DATE', 'INDEX_ID', 'PORTFOLIO', 'DESCRIPTION', 'VALUE', 'VALID_FROM', 'VALID_TO']
'''The function is flexible in terms of the columns to be selected and the columns by which the 
output should be sorted.
'''
#-->Example--->
'''
imp_f_calc('2018-06-01','2018-07-02','',[1],'',['TRADE_DATE', 'INDEX_ID', 'PORTFOLIO', 'DESCRIPTION', 'VALUE', 'VALID_FROM', 'VALID_TO'], ['TRADE_DATE', 'INDEX_ID'],['INDEX_ID'])
'''
# START_DATE='2005-03-31'
# END_DATE='2005-03-31'
# PORTFOLIO='0'
# INDEX_ID=[1]
# SECURITY_NAME=['SHY US EQUITY','SPYG US Equity']
# DESCRIPTION=['LIGHTS']
# VARS=['TRADE_DATE', 'INDEX_ID', 'PORTFOLIO', 'DESCRIPTION', 'VALUE', 'VALID_FROM', 'VALID_TO']
# SORT_ON=['TRADE_DATE', 'INDEX_ID']

import pymysql as ms
import pandas as pd
import time
import datetime

def imp_f_calc(START_DATE, END_DATE,SECURITY_NAME, PORTFOLIO, INDEX_ID, DESCRIPTION,VARS,SORT_ON):   
    if PORTFOLIO == '':
        port = '' 
        port2 = ''
    else:
        port = 'a.PORTFOLIO in (' + "','".join(str(e) for e in PORTFOLIO) + ') and '
        port2 = 'PORTFOLIO in (' + "','".join(str(e) for e in PORTFOLIO) + ') and '
    
    if INDEX_ID == '':
        index2 = ' '
        index = ' ' 
    else:
        index = 'a.INDEX_ID in (' + ','.join(str(e) for e in INDEX_ID) + ') and '
        index2 = 'INDEX_ID in (' + ','.join(str(e) for e in INDEX_ID) + ') and '
        
    if SECURITY_NAME == '' :
        str_sec1 = ' '
        str_sec2 = ' '
        sec_name = ''
    else:
        str_sec1 = 'and SECURITY_NAME in'
        str_sec2 = 'and a.SECURITY_NAME in'
        if (len(SECURITY_NAME) > 1):
            sec_name = tuple(SECURITY_NAME)
        else:
            sec_name = tuple(SECURITY_NAME) + ('filler_DOnt_care',)
        
    if DESCRIPTION == '' :
        str_dec1 = ' '
        str_dec2 = ' '
        desc = ''
    else:
        str_dec2 = 'and a.DESCRIPTION in'
        str_dec1 = 'and DESCRIPTION in'
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
    cond1 = port2 + index2
    QUE = '''select {}
             from f_calc as a 
             inner join
             (select max(RUNTIMEID) as RUNTIMEID,INDEX_ID,PORTFOLIO,DESCRIPTION  from f_calc  
             where {} TRADE_DATE between '{}' and '{}' {} {} {} {} and VALID_FLAG = 'Y' 
             group by  TRADE_DATE,INDEX_ID,PORTFOLIO,DESCRIPTION) as b
             on a.RUNTIMEID = b.RUNTIMEID and a.PORTFOLIO = b.PORTFOLIO and a.DESCRIPTION  = b.DESCRIPTION and a.INDEX_ID  = b.INDEX_ID
             where {} a.TRADE_DATE between '{}' and '{}' {} {} {} {} and VALID_FLAG = 'Y' {}; '''
             
    Q = QUE.format(var_names_o,cond1, START_DATE, END_DATE,str_dec1,desc,str_sec1,sec_name, cond,START_DATE, END_DATE,str_dec2,desc,str_sec2,sec_name,order_o )
    con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")        
    Meas = pd.read_sql(Q, con=con)
    Meas = Meas.drop_duplicates()
    con.close()
    del var_names, order
    return Meas


#function to exort intermediate measures to f_calc  table.
#The input paramter is a dataframe with all the columns of f_calc, except for RUNTIMEID.
'''                     EXAMPLE:
                                    exp_f_calc(df,1,'2018-08-20',['DVD_CASH'])'''
#INDEX_ID = '1'
#TRADE_DATE =  '2018-08-28'
#RANGE_BREAK_DESC = ['LIGHTS']
def exp_f_calc(VAL,INDEX_ID,SECURITY_NAME,PORTFOLIO,VALS_VALID_FROM,RANGE_BREAK_DESC,RBF) : 
#    dff = df[['RUNTIMEID','TRADE_DATE', 'INDEX_ID', 'PORTFOLIO', 'DESCRIPTION', 'VALUE','VALID_FLAG', 'VALID_FROM', 'VALID_TO']]
#    vals = dff.values.tolist()  
    if (RBF == 'N'):
        con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")
        cursor = con.cursor() 
        cursor.executemany("insert into f_calc(RUNTIMEID,TRADE_DATE, INDEX_ID, SECURITY_NAME, PORTFOLIO, DESCRIPTION, VALUE, VALID_FLAG, VALID_FROM, VALID_TO) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;", VAL)
        con.commit()
        con.close()    
    
    else: 
        if (len(SECURITY_NAME) > 1):
            sec_name = tuple(SECURITY_NAME)
        else:
            sec_name = tuple(SECURITY_NAME) + ('filler_DOnt_care',)
        con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")
        cursor = con.cursor() 
        
        QUE = '''SELECT max(RUNTIMEID) AS RUNTIMEID
                 FROM f_calc
                 where DESCRIPTION = '{}' and VALID_FLAG = 'Y' and SECURITY_NAME IN {} and PORTFOLIO = {} and INDEX_ID = {} 
                 and valid_to >= '{}' and valid_from <= '{}' '''
        Q = QUE.format(RANGE_BREAK_DESC,sec_name,PORTFOLIO,INDEX_ID,VALS_VALID_FROM,VALS_VALID_FROM)
        Meas = pd.read_sql(Q, con=con)
        Meas =Meas.drop_duplicates()
        runid = str(Meas.loc[0,'RUNTIMEID'])
        
        cursor.execute('''  update f_calc
                            set valid_to = DATE(%s - INTERVAL 1 DAY)
                            where valid_to >= %s and valid_from <= %s and RUNTIMEID = %s and DESCRIPTION = %s 
                            and SECURITY_NAME in %s and PORTFOLIO = %s ''',[VALS_VALID_FROM,VALS_VALID_FROM,VALS_VALID_FROM,runid,RANGE_BREAK_DESC,sec_name,PORTFOLIO])
        con.commit()
        
        cursor.execute('''  update f_calc
                            set VALID_FLAG = 'N'
                            where  VALID_FROM >= %s and DESCRIPTION = %s and SECURITY_NAME in %s and PORTFOLIO = %s and INDEX_ID = %s''', [VALS_VALID_FROM, RANGE_BREAK_DESC,sec_name,PORTFOLIO,INDEX_ID])
      
        cursor.executemany("insert into f_calc(RUNTIMEID,TRADE_DATE, INDEX_ID, SECURITY_NAME, PORTFOLIO, DESCRIPTION, VALUE, VALID_FLAG, VALID_FROM, VALID_TO) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;", VAL)
        
        con.commit()
        con.close()


#df =    pd.read_sql(" select * from f_calc where DESCRIPTION = 'DVD_CASH'; ",con=con)
#df['RUNTIMEID'] = timestamp/1000000
#df['VALID_FROM'] = '2018-08-20'
#df['TRADE_DATE'] = '2018-08-20'
#df['VALUE'] = 99.098
#VAL =   [[20180903.053456,'2018-09-01',1,['SHY US EQUITY'],0,'EXPOSURE',1222.22,'Y','2018-09-01','2099-06-01']]


#Import data from d_price  for ay date range for multiple Tickers and Req_Types.
  
#EX_DATE='2018-08-01'
#TICKER=['SHY US Equity']
#VARS=''
#Example -->
        #imp_d_ca('A', '2018-01-10', '2018-07-10', ['SPY US EQUITY'], ['DVD_CASH'], ['TICKER','CP_GROSS_AMT','TS_UPDATE','EX_DATE'])

def imp_d_ca(ROA, EX_DATE_START, EX_DATE_END, TICKER, CA, VARS): 
          
    if TICKER == '' :
        str1 = ' '
        desc = ''
    else:
        if (len(TICKER) > 1):
            desc = tuple(TICKER)
        else:
            desc = tuple(TICKER) + ('filler_DOnt_care',)
            
    if CA == '' :
        str2 = ' '
        desc1 = ''
    else:
        str2 = 'and CORPORATE_ACTION in  '
        if (len(CA) > 1):
            desc1 = tuple(CA)
        else:
            desc1 = tuple(CA) + ('filler_DOnt_care',)           
    
    if VARS == '':
        var_names_o = '*'
    else:    
        var_names = ''        
        for i in VARS:
            var_names1 = i + ','
            var_names = var_names1 + var_names
        var_names_o = var_names[:-1]
        
    if ROA == 'A':
        ex_date = ''
    else:
        ex_str =  "and EX_DATE between '{}' and '{}' "
        ex_date = ex_str.format(EX_DATE_START , EX_DATE_END)    
               
    QUE = '''select {} from d_ca
             where TICKER in {} {} {} {}
             order by EX_DATE and TICKER'''
             
    Q = QUE.format(var_names_o ,desc, str2, desc1 ,ex_date)
    con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")        
    Meas = pd.read_sql(Q, con=con)
    con.close()
    return Meas


#Import data from d_price for for multiple Tickers and Req_Types.
'''There are 2 modes dependng on thee i/p to the first parameter
mode1) When EOA = 'E' --> The end of the the month dates between the st_date and end_date are considered
mode2) When EOA != 'E' -->All the dates between the st_date and end_date are considered
'''
#TICKER = ['SPYG US EQUITY']
#REQ_TYPE = ['PX_SETTLE','PRICE']

#Example Input -->
#imp_d_price('E',1,'2016-01-01','2017-02-01',['SPYG US EQUITY','IWF US Equity'],'','BLOOMBERG')

import pymysql as ms
import pandas as pd
    
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
    
    con = ms.connect("127.0.0.1","root","Indxx@1234","epic_trust_vvr")
    Meas = pd.read_sql(Q, con=con)
    con.close()   
    Pivo = Meas.pivot(index = 'TRADE_DATE' ,columns='TICKER', values= 'PRICE')
    return(Pivo) 