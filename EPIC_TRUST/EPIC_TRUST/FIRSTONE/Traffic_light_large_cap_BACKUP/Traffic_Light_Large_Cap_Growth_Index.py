# -*- coding: utf-8 -*-
"""
Index code using  TR Series values.
"""

#Removes all variables
#%reset -f
import sys
import time
import talib
import pandas as pd
import numpy as np
from datetime import datetime
import pandas_datareader.data as web

sys.path.insert(0, 'E:\\EPIC TRUST\\Traffic_Light_Large_Cap_Growth_Index\\FUNCTIONS')
import import_export as ie
import date_functions as dt
import price_adj_func as pa
import reload_func as reload
import functions as func
ST = time.time()

###### Execution Parameters*
CALC_MODE = 'recalc' # possible values:- 'daily'  , 'recalc'

###### Index Constants
CALENDAR_ID=1
INDEX_ID = 1

###### Underlying constants
COL_NAMES = ['SPY','SPYG','SLYG','IWF','SHY']
FINAL_LIST = ['SPY US EQUITY', 'SPYG US EQUITY', 'SLYG US EQUITY', 'IWF US EQUITY', 'SHY US EQUITY']
IND_TICKER_LIST =  ['SPY US EQUITY','SPYG US EQUITY','SLYG US EQUITY','IWF US EQUITY']
ISIN_ARRAY = ['US78462F1030','US78464A4094','US78464A2015','US4642876142','US4642874576']
TICKER_START_DATE = ['1993-01-29','2000-09-29','2000-09-29','2000-05-26','2002-07-26']
TICKER_NAMES = []
BT_START_DATE = datetime.strptime('31-12-2004', '%d-%m-%Y')

####### INITIALIZATION
SAVE_PRICE = pd.DataFrame(columns = COL_NAMES)
SAVE_INDICATORS = pd.DataFrame( )
SAVE_SIGNALS = pd.DataFrame( )
SAVE_LIGHTS = pd.DataFrame( )
INDEX_LEVEL = pd.DataFrame(columns = ['INDEX_VALUE'] )

###### CALCULATION DAYS LIST

if CALC_MODE == 'daily':
    CDL = datetime.today().strftime("%Y-%m-%d")
    NO_CALDAYS = len(CDL)
else:
    CALC_START_DATE =  '2019-01-31'  #'2004-12-31'#
    CALC_END_DATE =  '2019-01-31'
    CDL = dt.TDL(CALC_START_DATE,CALC_END_DATE,CALENDAR_ID)
    NO_CALDAYS = len(CDL)

#Dummy dataframes for debugging and analysis
IND_1ALL  = pd.DataFrame()
IND_1ALL_BIN  = pd.DataFrame()
IND_2ALL  = pd.DataFrame()
IND_2ALL_BIN  = pd.DataFrame()
IND_3ALL_BIN  = pd.DataFrame()

stamp =  int(datetime.now().strftime("%Y%m%d%H%M%S"))
#try:
for fk in  range(0,NO_CALDAYS):   
    CALC_DATE = CDL[fk] 
    ########Fetching month end dates###########################
    Monthendlist = dt.imp_Nth_date(CALENDAR_ID, 'LAST', '', 'I', TICKER_START_DATE[0], dt.MNTH_OFFSET(TICKER_START_DATE[0],CALC_DATE,'I'))
    
    if str(CALC_DATE) == str(Monthendlist.iloc[-1].TRADE_DATE):
        timestamp =  int(datetime.now().strftime("%Y%m%d%H%M%S"))
        print(CALC_DATE)
    ###################################       MACD SIGNAL       #################################################
        Monthendlist['TRADE_DATE'] = Monthendlist['TRADE_DATE'].apply(lambda x:str(x))
        END_DATE = str(Monthendlist.loc[len(Monthendlist.index)-1,'TRADE_DATE'])
    
    #TR Series Calculation        
        SPY_TR = pa.TR_SERIES(['SPY US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
        SPYG_TR = pa.TR_SERIES(['SPYG US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
        SLYG_TR = pa.TR_SERIES(['SLYG US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
        SHY_TR = pa.TR_SERIES(['SHY US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
        IWF_TR = pa.TR_SERIES(['IWF US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
        
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
        TM250 = dt.WORKDAY(CALC_DATE,CALENDAR_ID,-250)
        DT_RANGE = pd.DataFrame()
        DT_RANGE['TRADE_DATE'] = dt.TDL(TM250,CALC_DATE,CALENDAR_ID)
        DT_RANGE['TRADE_DATE'] = DT_RANGE['TRADE_DATE'].apply(lambda x:str(x))
        
        SPY_TR_CP_175DMA = DT_RANGE.merge(SPY_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)
        SPYG_TR_CP_175DMA = DT_RANGE.merge(SPYG_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)
        SLYG_TR_CP_175DMA = DT_RANGE.merge(SLYG_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)       
        SHY_TR_CP_175DMA = DT_RANGE.merge(SHY_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)       
        IWF_TR_CP_175DMA= DT_RANGE.merge(IWF_TR, on = 'TRADE_DATE', how = 'left', left_index=False, right_index=False)
    
        CP_175DMA = pd.DataFrame()
        CP_175DMA['SPY US EQUITY'] =  SPY_TR_CP_175DMA.TR_SERIES
        CP_175DMA['SPYG US EQUITY'] = SPYG_TR_CP_175DMA.TR_SERIES
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
        TM500 = dt.WORKDAY(CALC_DATE,CALENDAR_ID,-500)
        INVERSION_DATES = dt.TDL(TM500, CALC_DATE, CALENDAR_ID)
        start = INVERSION_DATES[0]
        end = INVERSION_DATES[-1]
        T10Y2Y = web.DataReader('T10Y2Y', 'fred', start, end) # END = CALC_DATE, START =  END - 24 MNTHS INCL
        T10Y2Y = T10Y2Y.ffill()
        
        T10Y2Y['TRADE_DATE'] = T10Y2Y.index
        T10Y2Y['TRADE_DATE'] = T10Y2Y['TRADE_DATE'].apply(lambda x:str(x.date()))
        Monthendlist['TRADE_DATE'] = Monthendlist['TRADE_DATE'].apply(lambda x:str(x))
        T10Y2Y_ME = Monthendlist.merge(T10Y2Y, left_index=False, right_index=False) 
        IND4 = int((T10Y2Y_ME.loc[len(T10Y2Y_ME)-25:len(T10Y2Y_ME)-8,'T10Y2Y'] < 0).sum() > 0)
        
        #Default Weights
        GOLDEN_EXPOSURE = pd.Series([.2,.6,.1,.1,0])
        
    ##################################          LIGHTS DETERMINATION
        IND_2ALL = IND_2ALL.append(IND2.iloc[-1])
        IND_2ALL = IND_2ALL[['SPY US EQUITY', 'SPYG US EQUITY', 'SLYG US EQUITY', 'IWF US EQUITY']]
        
    ########### LIGHTS Normalization
        IND1 [ IND1>0 ] = 1  ###SECURITY > 200DMA
        IND1 [ IND1<0 ] = -1  ###SECURITY <= 200DMA
        IND2 [ IND2>0 ] = 1  ### 12EMA > 26EMA
        IND2 [ IND2<0 ] = -1  ### 12EMA <= 26EMA
    
        IND3 = (IND1.values + IND2.values)/2
        
        #Intermediates For Debugging
        IN3 = (IND1 + IND2)/2
        IND_1ALL_BIN = IND_1ALL_BIN.append(IND1.iloc[-1])
        IND_2ALL_BIN = IND_2ALL_BIN.append(IND2.iloc[-1])
        IND_1ALL_BIN = IND_1ALL_BIN[IND_TICKER_LIST]
        IND_2ALL_BIN = IND_2ALL_BIN[IND_TICKER_LIST]
    
        
    ################################          EXPOSURE DETERMINATION
        DIVEST= 0
        MEM_FLAG = [0,0,0,0,0]
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
                            MEM_FLAG[j] = 1 
                            EXPOSURE[j] = 0
                            DIVEST = DIVEST +  GOLDEN_EXPOSURE[j]
                        else :
                        #################  YELLOW SIGNAL ########################                            
                            TM1 = pd.DataFrame()
                            TM1 = dt.imp_Nth_date(CALENDAR_ID, 'LAST', 'B', '', CALC_DATE.strftime('%Y-%m-%d'), 1)
                            
                            LIGHTS_TM1 = ie.imp_f_calc(str(TM1.loc[0,'TRADE_DATE']), str(TM1.loc[0,'TRADE_DATE']), [IND_TICKER_LIST[j]],'0', [INDEX_ID], ['LIGHTS'],['VALUE','VALID_FROM'],['VALID_FROM'])
                            MEM_FLAG_TM1 = ie.imp_f_calc(str(TM1.loc[0,'TRADE_DATE']), str(TM1.loc[0,'TRADE_DATE']), [IND_TICKER_LIST[j]],'0', [INDEX_ID], ['MEM_FLAG'],['VALUE','VALID_FROM'],['VALID_FROM'])
                            
                            if (LIGHTS_TM1.loc[0,'VALUE'] == -1): 
                                MEM_FLAG[j] = 1
                                IND3[-1][j] = 1
                                EXPOSURE[j] = GOLDEN_EXPOSURE[j]
                            ################ YELLOW SIGNAL WITHOUT RED MEMORY ####################
                            else :
                                if (MEM_FLAG_TM1.loc[0,'VALUE'] == 1) and (IND3[-1][j] == 0):
                                    MEM_FLAG[j] = 1
                                    IND3[-1][j] = 1
                                    EXPOSURE[j] = GOLDEN_EXPOSURE[j]
                                else:
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
                        TM1 = pd.DataFrame()
                        TM1 = dt.imp_Nth_date(CALENDAR_ID, 'LAST', 'B', '', CALC_DATE.strftime('%Y-%m-%d'), 1)
                        
                        LIGHTS_TM1 = ie.imp_f_calc(str(TM1.loc[0,'TRADE_DATE']), str(TM1.loc[0,'TRADE_DATE']), [IND_TICKER_LIST[j]],'0', [INDEX_ID], ['LIGHTS'],['VALUE','VALID_FROM'],['VALID_FROM'])
                        MEM_FLAG_TM1 = ie.imp_f_calc(str(TM1.loc[0,'TRADE_DATE']), str(TM1.loc[0,'TRADE_DATE']), [IND_TICKER_LIST[j]],'0', [INDEX_ID], ['MEM_FLAG'],['VALUE','VALID_FROM'],['VALID_FROM'])
                        
                        if (LIGHTS_TM1.loc[0,'VALUE'] == -1): 
                            MEM_FLAG[j] = 1 
                            IND3[-1][j] = 1
                            EXPOSURE[j] = GOLDEN_EXPOSURE[j]
    
                            ################ YELLOW SIGNAL WITHOUT RED MEMORY ####################
                        else :
                             if (MEM_FLAG_TM1.loc[0,'VALUE'] == 1) and (IND3[-1][j] == 0):
                                 MEM_FLAG[j] = 1
                                 IND3[-1][j] = 1
                                 EXPOSURE[j] = GOLDEN_EXPOSURE[j]
                             else:
                                 EXPOSURE[j] = GOLDEN_EXPOSURE[j] * 0.75
                                 DIVEST = DIVEST + 0.25 * GOLDEN_EXPOSURE[j]
    
                #########################   SCENARIO - 1    ###################################
                ###################  INVESTMENT INTO GREEN LIGHTED COMPONENTS  #########################
                if (IND3[-1] == 1).sum() >0 :
                    EXPOSURE = EXPOSURE + (DIVEST / (IND3[-1] == 1).sum()) * np.append((IND3[-1] == 1)  * 1,EXPOSURE[4])
    
                ##############        INVESTMENT INTO TREASURIES      ################
                else:
                    EXPOSURE[4] = DIVEST
    
    ##################    END of CALCULATION LOOP    ####################################         
    ###########   EXPORTING EXPOSURE, LIGHT VALUES FOR EVERY DATE    ##################################
        col = ['RUNTIMEID','TRADE_DATE','INDEX_ID','SECUITY_NAME','PORTFOLIO','DESCRIPTION','VALUE','VALID_FLAG','VALID_FROM', 'VALID_TO']    
        SAVE_LIGHTS = pd.DataFrame(columns = col)
        l5 = IND3.tolist()
        l6 = l5[-1]
        l6.append(IND4)
    
        #      Intermediates For Debugging  
        IND_3ALL_BIN = IND_3ALL_BIN.append(l6)
    
    #EXPORTING lights
        for i in range(0,len(FINAL_LIST)):
            SAVE_LIGHTS = pd.DataFrame({'RUNTIMEID' : str(timestamp / 1000000),'TRADE_DATE' : str(CALC_DATE) ,'INDEX_ID' : 1,'SECUITY_NAME' : FINAL_LIST[i] ,'PORTFOLIO' : 0,'DESCRIPTION' : 'LIGHTS','VALUE' : l6[i],'VALID_FLAG' : 'Y', 'VALID_FROM' : str(CALC_DATE), 'VALID_TO' : '2099-01-01' }, index=[0])
           
            SAVE_LIGHTS = SAVE_LIGHTS[col]
            vals = SAVE_LIGHTS.values.tolist()
            ie.exp_f_calc(vals,str(INDEX_ID),[FINAL_LIST[i]],'0',str(CALC_DATE),'LIGHTS','')
            
    #EXPORTING MEM_FLAG
        for i in range(0,len(FINAL_LIST)):
            SAVE_MEM = pd.DataFrame({'RUNTIMEID' : str(timestamp / 1000000),'TRADE_DATE' : str(CALC_DATE) ,'INDEX_ID' : 1,'SECUITY_NAME' : FINAL_LIST[i] ,'PORTFOLIO' : 0,'DESCRIPTION' : 'MEM_FLAG','VALUE' : MEM_FLAG[i],'VALID_FLAG' : 'Y', 'VALID_FROM' : str(CALC_DATE), 'VALID_TO' : '2099-01-01' }, index=[0])
           
            SAVE_MEM = SAVE_MEM[col]
            vals = SAVE_MEM.values.tolist()
            ie.exp_f_calc(vals,str(INDEX_ID),[FINAL_LIST[i]],'0',str(CALC_DATE),'MEM_FLAG','')     
            
    #Exporting EXPOSURE
        SAVE_EXPOSURE = pd.DataFrame(columns = col)
        EXPOSURE = list(EXPOSURE)
    
        for i in range(0,len(FINAL_LIST)):
            SAVE_EXPOSURE = pd.DataFrame({'RUNTIMEID' : str(timestamp / 1000000),'TRADE_DATE' : str(CALC_DATE) ,'INDEX_ID' : 1,'SECUITY_NAME' : FINAL_LIST[i] ,'PORTFOLIO' : 0,'DESCRIPTION' : 'EXPOSURE','VALUE' : EXPOSURE[i],'VALID_FLAG' : 'Y', 'VALID_FROM' : str(CALC_DATE), 'VALID_TO' : '2099-01-01' }, index=[0])
            
            SAVE_EXPOSURE = SAVE_EXPOSURE[col]
            vals = SAVE_EXPOSURE.values.tolist()
            ie.exp_f_calc(vals,str(INDEX_ID),[FINAL_LIST[i]],'0',str(CALC_DATE),'EXPOSURE','')
        print('exported to f_calc for '+str(CALC_DATE))
        #func.WEIGTHS_CSV([X*100 for X in EXPOSURE],CALC_DATE)
        #func.success_send_attach("E:\\EPIC TRUST\\FIRSTONE\\output\\TLLCGI_" +CALC_DATE.strftime("%d-%m-%Y")+".csv")
    
    else:
        print("n")
    print(time.time() - ST)
    
#except Exception as e:
#    func.error_msg(e)