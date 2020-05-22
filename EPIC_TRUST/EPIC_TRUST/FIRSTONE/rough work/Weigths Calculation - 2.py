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
import datetime
import os
import sys
sys.path.append(os.path.abspath("C:/Users/V Vardhan/Desktop/EPICTRUST/functions.py"))
import functions as func    
    
x1=pd.ExcelFile("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\DATA\\PRICE.xlsx")
CP=x1.parse('Price') 
CP=CP.iloc[::-1]  
CNAV = x1.parse('NAV')
CNAV=CNAV.iloc[::-1] 

############     CALCULATION DATES DETERMINATION      #####################################################
##TRADING DAYS LIST
x2=pd.ExcelFile("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\DATA\\CALCULATION DATES.xlsx")
TDL=x2.parse('Sheet1')  

###### CONSTANTS
ISIN = ['US78464A4094','US78462F1030','US4642876480','US4642876142','US4642874576']
COL_NAMES = ['Date','SPYG','SPY','IWO','IWF','SHY']
TICKER_LIST = ['SPYG','SPY','IWO','IWF']
BT_START_DATE = datetime.datetime.strptime('31-12-2004', '%d-%m-%Y')

####### INITIALIZATION
SAVE_PRICE = pd.DataFrame(columns = COL_NAMES)
SAVE_INDICATORS = pd.DataFrame( )
SAVE_SIGNALS = pd.DataFrame( ) 
SAVE_LIGHTS = pd.DataFrame( )
SAVE_EXPOSURE = pd.DataFrame( )
INDEX_LEVEL = pd.DataFrame(columns = ['INDEX_VALUE'] )

##CALCULATION DAYS LIST
CALC_START_DATE = datetime.datetime.strptime('31-12-2004', '%d-%m-%Y')
CALC_END_DATE = datetime.datetime.strptime('30-06-2018', '%d-%m-%Y')
CDL = TDL[ (TDL['Date'] >= CALC_START_DATE) & (TDL['Date'] <= CALC_END_DATE) ]
CDL.index = range(len(CDL)) 
NO_CALDAYS = len(CDL)
    
for fk in  range(0,NO_CALDAYS):
    
    CALC_DATE = CDL.iloc[fk,0]
    CALC_DATE_INDEX = TDL[TDL['Date'] == CALC_DATE].index
    CP_CALC_DATE = CP.merge(pd.Series(CALC_DATE).to_frame('Date'), left_index=False, right_index=False)

    ########Fetching month end dates###########################
    TEMP1 = pd.DataFrame(TDL.loc[CALC_DATE_INDEX[0]-500:CALC_DATE_INDEX[0]+1,'Date'] )  
    TEMP1['Month']=TEMP1['Date'].dt.month
    TEMP1['Month-end']=TEMP1['Month'].diff(-1)
    Monthendlist =(TEMP1[TEMP1['Month-end'] != 0].dropna())['Date']
    del TEMP1
    
    if CALC_DATE == Monthendlist.iloc[-1] :
        
###################################       MACD SIGNAL       #################################################
        print(CP_CALC_DATE)    
        ########Calculating 12EMA
        CP_ME_12EMA = func.EMA1(CP_CALC_DATE,CALC_DATE,Monthendlist[-2:-1],12,TICKER_LIST)
        CP_ME_12EMA = CP_ME_12EMA[ CP_ME_12EMA['Date'] <= CALC_DATE ]
        CP_ME_26EMA = func.EMA1(CP_CALC_DATE,CALC_DATE,Monthendlist[-2:-1],26,TICKER_LIST)  
        CP_ME_26EMA = CP_ME_26EMA[ CP_ME_26EMA['Date'] <= CALC_DATE ]
   
        ########INDICATOR DETERMINATION
        INDICATOR2 = pd.DataFrame(   )
        INDICATOR2['Date'] = CP_ME_26EMA['Date']
        INDICATOR2[TICKER_LIST] = CP_ME_12EMA[TICKER_LIST] - CP_ME_26EMA[TICKER_LIST]

###############################        200DMA SIGNAL         ####################################################
        ########Fetching last 300 dates###########################
        DMA_DATES = pd.DataFrame(TDL.loc[CALC_DATE_INDEX[0]-400:CALC_DATE_INDEX[0],'Date'] )  
        
        ########Calculating 200DMA
        CP_240DMA=CP.merge(DMA_DATES, left_index=False, right_index=False)
        DMA240 = pd.DataFrame( )
        DMA240['Date'] = CP_240DMA['Date']
        DMA240['SPYG']=talib.SMA(CP_240DMA['SPYG'].values,timeperiod=240)
        DMA240['SPY']=talib.SMA(CP_240DMA['SPY'].values,timeperiod=240) 
        DMA240['IWO']=talib.SMA(CP_240DMA['IWO'].values,timeperiod=240)
        DMA240['IWF']=talib.SMA(CP_240DMA['IWF'].values,timeperiod=240) 
         
        ########INDICATOR DETERMINATION
        TEMP2 = pd.DataFrame(   )
        TEMP2['Date'] = CP_240DMA['Date']
        TEMP2[TICKER_LIST] = CP_240DMA[TICKER_LIST] -DMA240[TICKER_LIST]  
        INDICATOR1 = pd.DataFrame(   )
        INDICATOR1 = (Monthendlist.to_frame().merge(TEMP2, left_index=False, right_index=False))

########################        TREASURY INVERSION         #####################################################
        ########Fetching last 100 dates###########################
#        INVERSION_DATES = pd.DataFrame(TDL.loc[CALC_DATE_INDEX[0]-100:CALC_DATE_INDEX[0],'Date'] ) 
#        
##        ########Fetching Monthend T10Y2Y
#        start =INVERSION_DATES.iloc[0,0]
#        end =INVERSION_DATES.iloc[-1,0]
#        start = datetime.datetime.strptime('01-01-2002', '%d-%m-%Y')
#        end = datetime.datetime.strptime('30-06-2018', '%d-%m-%Y')
#        T10Y2Y = web.DataReader('T10Y2Y', 'fred', start, end)
#        T10Y2Y=T10Y2Y.ffill()
#        T10Y2Y['Date'] = T10Y2Y.index
#        T10Y2Y.index = range(len(T10Y2Y))
#        T10Y2Y.to_excel("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\DATA\\T10Y2Y.xlsx",index = False)
        x5=pd.ExcelFile("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\DATA\\T10Y2Y.xlsx")
        T10Y2Y=x5.parse('Sheet1')

        T10Y2Y_ME = T10Y2Y.merge(Monthendlist.to_frame(), left_index=False, right_index=False)
        IND4 = (T10Y2Y_ME.loc[len(T10Y2Y_ME)-19:len(T10Y2Y_ME)-8,'T10Y2Y'] < 0).sum() > 0

################################           Weights Determination           #######################################
        GOLDEN_EXPOSURE = pd.Series([.6,.2,.1,.1,0])

        ##################################          LIGHTS DETERMINATION          ######################################
        IND1 = INDICATOR1[-2:][TICKER_LIST]
        IND1 [ IND1>0 ] = 1  ###SECURITY > 200DMA
        IND1 [ IND1<0 ] = -1  ###SECURITY <= 200DMA
        
        IND2 = INDICATOR2[-2:][TICKER_LIST]
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
                
                for j in range(len(TICKER_LIST)):
                    
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
                EXPOSURE[4] = DIVEST  
        
        ###################   EXPORTING EXPOSURE VALUES FOR EVERY DATE    ###################################
        func.WEIGTHS_CSV(EXPOSURE,CALC_DATE)
        
        args = (np.array(DMA240[-1:]),np.array(CP_ME_12EMA[-1:][TICKER_LIST]),np.array(CP_ME_26EMA[-1:][TICKER_LIST]))
        SAVE_INDICATORS =  SAVE_INDICATORS.append( pd.DataFrame ( np.concatenate(args,axis=1) ),ignore_index = True)         
        args = (np.array(str(CALC_DATE)).reshape(1,1),np.array(IND1[-1:]),np.array(IND2[-1:]),np.array([int(IND4)]).reshape(-1,1))
        SAVE_SIGNALS = SAVE_SIGNALS.append( pd.DataFrame (np.concatenate(args,axis=1))  )
        args = (np.array(str(CALC_DATE)).reshape(1,1),np.array(IND3[-1:]))
        SAVE_LIGHTS =  SAVE_LIGHTS.append( pd.DataFrame (np.concatenate(args,axis=1)) )       
        args = (np.array(str(CALC_DATE)).reshape(1,1),np.array(EXPOSURE).reshape(1,5))      
        SAVE_EXPOSURE =  SAVE_EXPOSURE.append( pd.DataFrame ( np.concatenate(args,axis=1) ) )   

    SAVE_PRICE  = SAVE_PRICE.append(CP_CALC_DATE) 
    

##################    END of CALCULATION LOOP    #####################################
   
########################       WRITING VALUES TO EXCEL FILE IN DESIRED FORMAT        #######################################           
SAVE_INDICATORS.columns = [np.array(['INDICATOR','200DMA','200DMA','200DMA','200DMA','12EMA','12EMA','12EMA','12EMA',  \
                                    '26EMA','26EMA','26EMA','26EMA']), \
    np.array([['Date'] +TICKER_LIST + TICKER_LIST + TICKER_LIST]).reshape(13,)]
SAVE_SIGNALS.columns = [np.array(['ETF','SPYG','SPYG','SPY','SPY','IWO','IWO','IWF','IWF','SHY']), \
    np.array([['Date'] + ['DMA','MACD'] + ['DMA','MACD'] + ['DMA','MACD'] + ['DMA','MACD'] + ['INVERSION']]).reshape(10,)]
SAVE_LIGHTS.columns = ['Date'] +TICKER_LIST
SAVE_EXPOSURE.columns = COL_NAMES

writer =pd.ExcelWriter("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\PYTHON CALC-DUMPSHEETS\\DUMPSHEET.xlsx" ,engine ='xlsxwriter')
SAVE_PRICE.to_excel(writer,'PRICE',index = False)
SAVE_INDICATORS.to_excel(writer,'INDICATORS')
SAVE_SIGNALS.to_excel(writer,'SIGNALS')
SAVE_LIGHTS.to_excel(writer,'LIGHTS',index = False)
SAVE_EXPOSURE.to_excel(writer,'EXPOSURE',index = False)
writer.save()

func.BT_WEIGTHS_CSV(SAVE_EXPOSURE,CALC_START_DATE,CALC_END_DATE)

del SAVE_PRICE,SAVE_INDICATORS,SAVE_SIGNALS,SAVE_LIGHTS,SAVE_EXPOSURE

####IMPORTING DATA FROM API
import requests
import pymysql as ms
from pandas.io import sql
from sqlalchemy import create_engine
from mysql import connector
import time
import datetime
import pdb
ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

engine = create_engine("mysql+mysqldb://USER:"+'PASSWORD'+"@localhost/DATABASE")
con = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format("epicDB", "epicDB", 
                                                      "localhost", "epic_trust_vvr"))

engine = create_engine('sqlite://', echo=False)
#####  Price EXPORT  ############
ISIN = ['US78464A4094','US78462F1030','US4642876480','US4642876142','US4642874576']
DATA_LOAD = '2018-08-01'
url = 'http://146.20.65.208/central_db_edi/api/gettodayprice.php?type1=JSON&authcode=INDXX:931&date='+DATA_LOAD
temp3=requests.get(url).json()
temp3 =temp3['data']
rawdata=pd.DataFrame.from_dict(temp3, orient='columns')
rawdata=pd.DataFrame.transpose(rawdata)
CP = rawdata.merge(pd.DataFrame(ISIN,columns = ['isin']), left_index=False, right_index=False)
CP_INSERTDB = pd.DataFrame()

CP_INSERTDB['TRADE_DATE'] = CP['date']
#CP_INSERTDB['TRADE_DATE'] = pd.to_datetime(CP_INSERTDB['TRADE_DATE'],format = '%Y-%m-%d')
CP_INSERTDB['TICKER'] = CP['ticker']
CP_INSERTDB['REQ_TYPE'] = 'PX_SETTLE'
CP_INSERTDB['PRICE'] = CP['price']
CP_INSERTDB['DATA_SOURCE'] = 'BLOOMBERG'
#CP_INSERTDB.index = CP['date']

vals=CP_INSERTDB.values.tolist()

with con.cursor() as cursor:
    cursor.execute('''delete from s_price;''')
    cursor.executemany("insert into s_price(TRADE_DATE, TICKER,REQ_TYPE,PRICE,DATA_SOURCE) values (%s, %s,%s, %s,%s);", vals)
    
    cursor.execute('''insert into d_price (TRADE_DATE,TICKER,REQ_TYPE,DATA_SOURCE,PRICE) 
                      select l.TRADE_DATE, l.TICKER, l.REQ_TYPE, l.DATA_SOURCE, l.PRICE from s_price as l 
                      left outer join d_price as r on 
                      l.TRADE_DATE = r.TRADE_DATE and l.TICKER = r.TICKER  and l.REQ_TYPE = r.REQ_TYPE and   l.DATA_SOURCE = r.DATA_SOURCE
                      where r.TRADE_DATE is null and r.TICKER is null and r.REQ_TYPE is null and r.DATA_SOURCE is null''');
#    cursor.executemany("insert into s_price(TRADE_DATE, TICKER,REQ_TYPE,PRICE,DATA_SOURCE) values (%s, %s,%s, %s,%s)", vals )
#    cursor.execute("update  d_price set PRICE = %s where  TRADE_DATE = %s and TICKER = %s " , ('189', '2018-08-01', 'SHY US Equity') )
    
    cursor.execute('''update d_price as l inner join s_price as r on
                       l.TRADE_DATE = r.TRADE_DATE and l.TICKER = r.TICKER  and l.REQ_TYPE = r.REQ_TYPE and l.DATA_SOURCE = r.DATA_SOURCE
                       set l.PRICE = r.PRICE''')
    cursor.execute('''delete from s_price;''')
    con.commit()
    
con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")

CP_INSERTDB.to_sql(con=con,name='d_price',if_exists='append',index = False)

sql.write_frame(CP_INSERTDB, con=con, name='d_price',if_exists='replace', flavor='mysql')

#####  Curr EXPORT  ###########
ISIN = ['US78464A4094','US78462F1030','US4642876480','US4642876142','US4642874576']
DATA_LOAD = '2018-08-01'
url = 'http://146.20.65.208/central_db_edi/api/gettodaycurr.php?type1=JSON&authcode=INDXX:931&date='+DATA_LOAD
temp3=requests.get(url).json()
temp3 =temp3['data']
rawdata=pd.DataFrame.from_dict(temp3, orient='columns')
rawdata=pd.DataFrame.transpose(rawdata)
CP = rawdata.merge(pd.DataFrame(ISIN,columns = ['isin']), left_index=False, right_index=False)


##### CA EXPORT  ###############3
ISIN = ['US78464A4094','US78462F1030','US4642876480','US4642876142','US4642874576']
DATA_LOAD = '2018-08-01'
url = 'http://146.20.65.208/central_db_edi/api/getfutureca.php?type1=JSON&authcode=INDXX:931&date='+DATA_LOAD
temp3=requests.get(url).json()
temp3 =temp3['data']
rawdata=pd.DataFrame.from_dict(temp3, orient='columns')
rawdata.index = rawdata['identifier']
CP = rawdata.merge(pd.DataFrame(ISIN,columns = ['isin']), left_index=False, right_index=False)

rawdata.columns

#####EXPORTING INTO OUR TABLES
