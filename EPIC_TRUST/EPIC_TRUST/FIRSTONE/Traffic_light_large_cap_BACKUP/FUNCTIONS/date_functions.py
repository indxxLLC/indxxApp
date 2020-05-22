# -*- coding: utf-8 -*-
"""
date functions
"""

#Function to pick any date in the calendar wrt an offset direction and distance from a given date.
#Example: 
#imp_Nth_date(1,'5','B','I','2017-01-01',4)

#NOTE------->The second parameter TR_DAY_MONTH should always be passed as a string.
import pymysql as ms
import pandas as pd
from datetime import datetime
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


def imp_N_dates(CALENDAR_ID, TR_DAY_MONTH, S_DATE, L_DATE, MNTH_OFFSET):    
    if (TR_DAY_MONTH == 'LAST'):
        QUE = '''SELECT   distinct TRADE_DATE FROM  d_calendar
                 WHERE   TRADE_DATE IN (
                 SELECT   MAX(TRADE_DATE)
                 FROM     d_calendar
                 where TRADING_DAY = 1 and CALENDAR_ID = {} and TRADE_DATE between '{}' and '{}'
                 GROUP BY MONTH(TRADE_DATE), YEAR(TRADE_DATE))
                 ORDER BY TRADE_DATE '''
        Q = QUE.format(CALENDAR_ID, S_DATE, L_DATE)
        con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
        Meas = pd.read_sql(Q, con=con)
        con.close()   
        
    elif TR_DAY_MONTH == '':
        QUE = '''select distinct TRADE_DATE  from d_calendar where TRADING_DAY = 1  and TRADE_DATE between '{}' and '{}' and CALENDAR_ID = {} order by TRADE_DATE '''
        Q = QUE.format(S_DATE, L_DATE, CALENDAR_ID)
        con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
        Meas = pd.read_sql(Q, con=con)
        con.close() 
        
    else:
        TR_DAY_MONTH = int(TR_DAY_MONTH)
        QUE = '''select distinct TRADE_DATE  from d_calendar where TRADING_DAY = 1 and TR_DAY_MONTH  = {} and TRADE_DATE between  '{}' and '{}' and CALENDAR_ID = {} order by TRADE_DATE '''
        Q = QUE.format(TR_DAY_MONTH, S_DATE, L_DATE, CALENDAR_ID)
        con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
        Meas = pd.read_sql(Q, con=con)
        con.close() 
        
    if MNTH_OFFSET == '':
        return Meas
    else:
        Op = Meas.iloc[0:MNTH_OFFSET]
        return Op 
    
    
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