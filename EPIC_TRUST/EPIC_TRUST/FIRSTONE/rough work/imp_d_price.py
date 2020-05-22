# -*- coding: utf-8 -*-

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
    
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
    Meas = pd.read_sql(Q, con=con)
    con.close()   
    Pivo = Meas.pivot(index = 'TRADE_DATE' ,columns='TICKER', values= 'PRICE')
    return(Pivo) 
    