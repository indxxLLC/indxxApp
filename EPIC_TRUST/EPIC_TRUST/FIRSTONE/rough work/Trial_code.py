
#Snippet to import a python code as a module into the main code.
  #--->Status := Success and Fucntional.
'''import os
import sys
scriptpath = "C:\\Users\\ssstipirneni\\Desktop\\Python Codes\\functions.py"
sys.path.append(os.path.abspath(scriptpath))
import Functions as func

try:
    #Main Code
    print(asd)  #Example
    func.success_send_attach(op_file_path) 
except Exception as e:  
    func.error_msg(e)'''
    
    
#Function to offset the mnth of a given date wrt the given OFFSET val and to get the desired date in the derived month.
  #--->Status := Under Construction.  
  
import pymysql as ms
import pandas as pd
def DAY_IN_MONTH(CALENDAR_ID, DATE, OFFSET, BOF, IOE, N):
    cnx = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
    
    if (BOF == 'B'):
        BORF = '<'
    else:
        BORF = '>'
        
    if (IOE == 'I'):
        IORE = '='
    else:
        IORE = ' '
    
    sign = BORF + IORE
    QUE =  '''select * from d_calendar where TRADING_DAY = 1 and TR_DAY_MONTH  = {} and CALENDAR_ID = {}
    and TRADE_DATE {} '{}'  '''
    
    Q = QUE.format(N,CALENDAR_ID,sign,DATE)

    Meas = pd.read_sql(Q, con=cnx)
    
    if (SIGNAL == 'LAST'):
        OP = Meas.iloc[0]
        
    elif(SIGNAL == 'FIRST'):
        OP = Meas.iloc[-1]
       
    else:
        OP = Meas.iloc[N_DAY]
            
    cnx.close()
    return (OP)  

#Function to import values from d_price table.
  #--->Status := Under Construction.  
x = imp_d_price('2018-01-01','2018-01-21','SPYG US Equity','PX_SETTLE')
START_DATE = '2018-01-01'
END_DATE= '2018-01-21'
TICKER= 'SPYG US Equity'
REQ_TYPE=   'PX_SETTLE'

def imp_d_price_mn_end(START_DATE,END_DATE,TICKER,REQ_TYPE,DATA_SOURCE):
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
    
    QUE = '''select l.TRADE_DATE,l.TICKER,l.PRICE from d_price as l 
            inner join (SELECT   distinct TRADE_DATE FROM  d_calendar
            WHERE   TRADE_DATE IN (
            SELECT   MAX(TRADE_DATE)
            FROM     d_calendar
            where TRADING_DAY = 1 and TRADE_DATE <= '{}' and TRADE_DATE >= '{}'
            GROUP BY MONTH(TRADE_DATE), YEAR(TRADE_DATE)  )) as r on r.TRADE_DATE = l.TRADE_DATE
            where TICKER in {}
            and REQ_TYPE = '{}'
            and DATA_SOURCE = '{}';'''
    Q = QUE.format(START_DATE, END_DATE, TICKER, REQ_TYPE, DATA_SOURCE)
    Meas = pd.read_sql(Q, con=con)
    con.close()
    
    Pivo = Meas.pivot(index = 'TRADE_DATE' ,columns='TICKER', values= 'PRICE')
    return(Meas)

def imp_d_price(CALENDAR_ID, TR_DAY_MONTH, BOF, IOE, DATE, MNTH_OFFSET):
    
    if (BOF == 'B'):
        BORF = '<'
    else:
        BORF = '>'
        
    if (IOE == 'I'):
        IORE = '='
    else:
        IORE = ' '
    
    SIGN = BORF + IORE
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")    
    QUE = '''select r.TRADE_DATE, r.TICKER,  r.PRICE, r.DATA_SOURCE
             from d_price as r inner join 
             (select distinct TRADE_DATE  from d_calendar where TRADING_DAY = 1 and CALENDAR_ID = {} and TR_DAY_MONTH  = {} and TRADE_DATE {}  '{}') as l on r.TRADE_DATE = l.TRADE_DATE order by TRADE_DATE desc; '''  
             
    Q = QUE.format(CALENDAR_ID,TR_DAY_MONTH,SIGN,DATE)
    Meas = pd.read_sql(Q, con=con)
    con.close()
    
    Pivo = Meas.pivot(index = 'TRADE_DATE' ,columns='TICKER', values= 'PRICE')
    Pivo = Pivo.sort_index(ascending=False)
    
    Pivo = Pivo.iloc[MNTH_OFFSET]
    return(Pivo)    

    
Pivo.columns
    
TICKER = ('SPYG US EQUITY','SPY US EQUITY')
REQ_TYPE = 'PX_SETTLE'
TR_DAY_MONTH = 3
MNTH_OFFSET= [11,1,2]
DATA_SOURCE = 'BLOOMBERG'   
