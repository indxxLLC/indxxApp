# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 00:24:13 2018

@author: Administrator
"""
#To import data from d_price for all the month end dates, including and btn START_DATE and END_DATE
def imp_d_price_mn_end(START_DATE, END_DATE, TICKER, REQ_TYPE, DATA_SOURCE, MNTH_OFFSET):
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
    
    QUE = '''select l.TRADE_DATE,l.TICKER,l.PRICE from d_price as l 
            inner join (SELECT   distinct TRADE_DATE FROM  d_calendar
            WHERE   TRADE_DATE IN (
            SELECT   MAX(TRADE_DATE)
            FROM     d_calendar
            where TRADING_DAY = 1 and CALENDAR_ID = {} and TRADE_DATE  between '{}' and '{}' 
            GROUP BY MONTH(TRADE_DATE), YEAR(TRADE_DATE)  )) as r on r.TRADE_DATE = l.TRADE_DATE
            where TICKER in {}
            and REQ_TYPE = '{}'
            and DATA_SOURCE = '{}'; '''
    Q = QUE.format(CALENDAR_ID,START_DATE, END_DATE, TICKER, REQ_TYPE, DATA_SOURCE)
    Meas = pd.read_sql(Q, con=con)
    con.close()   
    Pivo = Meas.pivot(index = 'TRADE_DATE' ,columns='TICKER', values= 'PRICE')
    return(Pivo) 
 
#To import data from d_price for  any given trading day of the month
def imp_d_price(CALENDAR_ID, TR_DAY_MONTH, BOF, IOE, DATE, MNTH_OFFSET, TICKER):
    
    if (BOF == 'B'):
        BORF = '<'
    else:
        BORF = '>'
        
    if (IOE == 'I'):
        IORE = '='
    else:
        IORE = ' '
    
    TICKER = TICKER.append(' ')
    SIGN = BORF + IORE
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")    
    QUE = '''select r.TRADE_DATE, r.TICKER,  r.PRICE, r.DATA_SOURCE
             from d_price as r inner join 
             (select distinct TRADE_DATE  from d_calendar where TRADING_DAY = 1 and CALENDAR_ID = {} and TR_DAY_MONTH  = {} and TRADE_DATE {}  '{}') as l on r.TRADE_DATE = l.TRADE_DATE where TICKER in {}; '''  
             
    Q = QUE.format(CALENDAR_ID,TR_DAY_MONTH,SIGN,DATE,TICKER)
    Meas = pd.read_sql(Q, con=con)
    con.close()
    
    Pivo = Meas.pivot(index = 'TRADE_DATE' ,columns='TICKER', values= 'PRICE')
    Pivo = Pivo.sort_index(ascending=False)
    
    Pivo = Pivo.iloc[MNTH_OFFSET]
    return(Pivo)
    
def imp_f_calc(START_DATE, END_DATE, PORTFOLIO, INDEX_ID, DESCRIPTION, ORDER_ON):
    
    if PORTFOLIO == ' ':
        port = ''       
    else:
        port = 'a.PORTFOLIO in (' + "','".join(str(e) for e in TICKER) + ') and '

    if INDEX_ID == '':
        port = ' ' 
    else:
        index = 'a.INDEX_ID in (' + ','.join(str(e) for e in INDEX_ID) + ') and '

    cond = port + index
    
    if ORDER_ON == '':
        order = ' ' 
    else:
        order =  (lambda s: " ".join(s),ORDER_ON)
        
        order = ','.join(str(e) for e in ORDER_ON) + ') and '
    
    QUE = '''select  a.TRADE_DATE, a.INDEX_ID, a.PORTFOLIO a.DESCRIPTION
             from f_calc as a 
             inner join
             (select max(RUNTIMEID) as RUNTIMEID from f_calc  group by  TRADE_DATE,INDEX_ID,PORTFOLIO,DESCRIPTION) as b
             on a.RUNTIMEID = b.RUNTIMEID
             where {}  a.TRADE_DATE between '{}' and '{}' 
             order by a.TRADE_DATE, a.PORTFOLIO a.DESCRIPTION; '''
             
    Q = QUE.format(cond, START_DATE, END_DATE)
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")        
    Meas = pd.read_sql(Q, con=con)
    con.close()
    
START_DATE = '2018-01-01'
END_DATE = '2018-01-02'
print()
PORTFOLIO = [1,2]
INDEX_ID=[1]
ORDER_ON = ['as']

TICKER = ['SPYG US EQUITY', 'SPY US EQUITY']

r_data1 = r_data[r_data['CORPORATE_ACTION'] == 'DVD_CASH']
up_pack = r_data1['VALUES'].reset_index()


un_pack = up_pack.iloc[0,1]
tr = pd.DataFrame(un_pack)
trr = tr.set_index('name').T
 
#-----set try   

r_data = CA_DATALOAD(DATE).rename(columns = {'IDENTIFIER':'ISIN'})  
CA_dat = pd.merge(CA_REQ[['ISIN']],r_data,on = 'ISIN', how='left',left_index=False, right_index=False)
CA_dat = CA_dat[["ACTION_ID","CORPORATE_ACTION","COUNTRY_CODE","CURRENCY","DATAPROVIDER","EX_DATE","ISIN","IDENTIFIER_NAME","MODIFY_DATE","NAME","RECORD_DATE","STATUS","SYMBOL","TICKER",'VALUES']]

CA_dat = CA_dat.dropna()

CA_dat = CA_dat[CA_dat['CORPORATE_ACTION'] == 'DVD_CASH']
up_pack = CA_dat['VALUES']
up_pack.index = CA_dat['ISIN']
CA_dat.index = CA_dat['ISIN']

tr = pd.DataFrame(up_pack)

for i in range(len(tr)):
    R1 = tr.iloc[i]
    sd = R1.values.tolist()
#    r11 = R1.values.tolist()
    r1 =DataFrame.from_records(sd[i])
    tr1 = r1.set_index('name').T
    tr2 = tr1[['CP_GROSS_AMT','Frequency']]
    tr2['ISIN'] =  R1.name
    CA_dat = pd.merge(CA_dat,tr2,on = 'ISIN', how='left',left_index=False, right_index=False)

trr = tr.set_index('name').T

vals = r1
d_ca_DATALOAD(vals)



### To be included in reload function
import time
import datetime
from datetime import timedelta
    
EX_DATE = '2018-03-16'    
TICKER = ['SPY US EQUITY']
VARS = ['TICKER','CP_GROSS_AMT','ts_update']
CALENDAR_ID = 1
INDEX_ID = 1
def Period_Divisor(EX_DATE,TICKER,CALENDAR_ID,INDEX_ID) :
    
    ######   Fetching the UTS and CA values for range of tickers
    INFO = imp_d_ca(EX_DATE, TICKER, ['TICKER','CP_GROSS_AMT','TS_UPDATE'])
    ts = time.time()
    curr_time = datetime.datetime.fromtimestamp(ts)
    curr_time = int(curr_time.strftime('%Y%m%d%H%M%S')) / 1000000
    cut_off_time = datetime.datetime.fromtimestamp(ts) - timedelta(hours=1)
    cut_off_time = cut_off_time.strftime('%Y-%m-%d %H:%M:%S')
     ####### Check if the TICKER EX_DATE combination ts_update is within one hour of systime
    INFO = INFO[(INFO.TS_UPDATE >= cut_off_time)]

    ######  Import one day less than EX_DATE price for the ticker
    EX_DATE_TM1 = WORKDAY(EX_DATE,CALENDAR_ID,-1)
    P = imp_d_price('',CALENDAR_ID,EX_DATE_TM1,EX_DATE_TM1,TICKER,['PX_SETTLE'],'BLOOMBERG')
    
    ######  Period Divisor Calculation
    PRICE = float(P.iloc[0].values)
    CA_VALUE  = float(INFO['CP_GROSS_AMT'].values)
    PERIOD_DIVISOR  = (PRICE - CA_VALUE)/PRICE

    ### 1 is the portfolio number for all tickers. INDEX_ID is same as TICKER as the period divisor is related to the ticker
    vals = [[curr_time,EX_DATE,INDEX_ID, 0, 'Period_Divisor',PERIOD_DIVISOR,'Y',EX_DATE,'2099-12-31']]
    ###### Push the value to F_calc
    exp_f_calc(vals,INDEX_ID,EX_DATE,['Period_Divisor'])





##########  To be included in the main function after the month end check    

def TR_SERIES(TICKER,CALENDAR_ID):   
    for j in 1: len(TICKER):
        ########  Fetch the entire history of prices for the ticker
        PR_SERIES = imp_d_price('',CALENDAR_ID,TICKER_START_DATE[j],CALC_DATE,TICKER,'PX_SETTLE','BLOOMBERG')
       ######## Fetch the entire period divisors <= TRADE_DATE along with VALID_FROM to VALID_TO
       DIVISORS = imp_f_calc(TICKER_START_DATE[j], END_DATE, 1, INDEX_ID, DESCRIPTION,['VALUE','VALID_FROM','VALID_TO'],['VALID_FROM'])


    ######## Create a frame with length equal to the history date range and fill the frame with period divisors
   

    ####### Multiply the period divisors going backwards
    from functools import reduce
    reduce(lambda x, y: x*y, [1,2,3,4,5,6])  ## apply this function backwards for all the elements in the period_divisors list

    RESULT =

    ###### Multiply the calculated frame with price frame element wise to get the TR series
    TR_SERIES = PR_SERIES * RESULT

    ###### return TR series as output
    return(TR_SERIES)