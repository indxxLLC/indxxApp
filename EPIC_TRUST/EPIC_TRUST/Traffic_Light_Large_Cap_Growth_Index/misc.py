# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 08:34:20 2018

@author: Administrator
"""

SPY_TR = TR_SERIES(['SPY US Equity'],CALENDAR_ID,END_DATE,INDEX_ID)
SPYG_TR = TR_SERIES(['SPYG US Equity'],CALENDAR_ID,END_DATE,INDEX_ID)
SLYG_TR = TR_SERIES(['SLYG US Equity'],CALENDAR_ID,END_DATE,INDEX_ID)
SHY_TR = TR_SERIES(['SHY US Equity'],CALENDAR_ID,END_DATE,INDEX_ID)
IWF_TR = TR_SERIES(['IWF US Equity'],CALENDAR_ID,END_DATE,INDEX_ID)

TR_DF=pd.concat([SPY_TR[['TRADE_DATE','MUTIPLIER','TR_SERIES']],SPYG_TR[['TRADE_DATE','MUTIPLIER','TR_SERIES']],SLYG_TR[['TRADE_DATE','MUTIPLIER','TR_SERIES']],IWF_TR[['TRADE_DATE','MUTIPLIER','TR_SERIES']]],axis=1)

TR_DF.columns = ['SPY_DATE','SPY_MUL','SPY_TR','SPYG_DATE','SPYG_MUL','SPYG_TR','SLYG_DATE','SLYG_MUL','SLYG_TR','IWF_DATE','IWF_MUL','IWF_TR']

SPY_TEST = TR_SERIES(['SPY US Equity'],CALENDAR_ID,'2018-05-31',INDEX_ID)

writer = pd.ExcelWriter('C:\\Users\\Administrator\\Desktop\\TR_DF.xlsx')
TR_DF.to_excel(writer,'all tr val')
writer.save()


if 0:
    print('no')
else:
    print('nasd')
    
    
for i in range(0,len(l6)):
    SAVE_LIGHTS.loc[i,'SECUITY_NAME'] = COL_NAMES[i]   
    SAVE_LIGHTS.loc[i,'VALUE'] = str(l6[i])
    SAVE_LIGHTS.loc[i,'RUNTIMEID'] = str(timestamp / 1000000)
    SAVE_LIGHTS.loc[i,'TRADE_DATE'] = str(CALC_DATE)
    SAVE_LIGHTS.loc[i,'VALID_FROM'] = str(CALC_DATE)
    SAVE_LIGHTS.loc[i,'VALID_TO'] = '2099-01-01'
    SAVE_LIGHTS.loc[i,'INDEX_ID'] = 1
    SAVE_LIGHTS.loc[i,'PORTFOLIO'] = 0
    SAVE_LIGHTS.loc[i,'VALID_FLAG'] = 'Y'
    SAVE_LIGHTS.loc[i,'DESCRIPTION'] = 'LIGHTS' 
 

'''---------------EXPORTS---------------'''           
  
SPYG_lit = imp_f_calc('2004-12-31', '2018-07-31',['SPY US EQUITY','SPYG US EQUITY','SLYG US EQUITY','IWF US EQUITY','SHY US EQUITY'], '0', [1], ['LIGHTS'],['TRADE_DATE','SECURITY_NAME','VALUE'],['TRADE_DATE'])

l = pd.pivot_table(SPYG_lit, index = 'TRADE_DATE' ,columns='SECURITY_NAME', values= 'VALUE')
writer = pd.ExcelWriter('C:\\Users\\Administrator\\Desktop\\LIT1_24.xlsx')
l.to_excel(writer,'LIT')
writer.save()  

EXPOSURE = ie.imp_f_calc('2004-12-31', '2018-07-31',['SPY US EQUITY','SPYG US EQUITY','SLYG US EQUITY','IWF US EQUITY','SHY US EQUITY'], '0', [1], ['EXPOSURE'],['SECURITY_NAME','VALUE','VALID_FROM','VALID_TO'],['TRADE_DATE'])

l1 = pd.pivot_table(EXPOSURE, index = 'TRADE_DATE' ,columns='SECURITY_NAME', values= 'VALUE')
writer = pd.ExcelWriter('C:\\Users\\Administrator\\Desktop\\backtest.xlsx')
EXPOSURE.to_excel(writer,'exp')
writer.save()   

MEM_FLAG = imp_f_calc('2004-12-31', '2018-07-31',['SPY US EQUITY','SPYG US EQUITY','SLYG US EQUITY','IWF US EQUITY','SHY US EQUITY'], '0', [1], ['MEM_FLAG'],['TRADE_DATE','SECURITY_NAME','VALUE'],['TRADE_DATE'])

M1 = pd.pivot_table(MEM_FLAG, index = 'TRADE_DATE' ,columns='SECURITY_NAME', values= 'VALUE')
writer = pd.ExcelWriter('C:\\Users\\Administrator\\Desktop\\memory.xlsx')
M1.to_excel(writer,'MEM')
writer.save()   

'''---------------EXPORTS---------------'''           

ll = pd.DataFrame(IND_1ALL_BIN)

ll['ind'] = ll.index
asd = pd.pivot_table(ll, columns = 'ind', values = 0)

ind1_bin = pd.Dataframe(IND_1ALL_BIN)
writer = pd.ExcelWriter('C:\\Users\\Administrator\\Desktop\\IND_1ALL.xlsx')
IND_1ALL.to_excel(writer,'sh1')
writer.save()



TR['SPY'] = SPY_TR['TR_SERIES'].sort_values()
TR['DATE'] = SPY_TR['TRADE_DATE']
TR['SPYG'] = SPYG_TR['TR_SERIES']
TR['SLYG'] = SLYG_TR['TR_SERIES']
TR['SHY'] = SHY_TR['TR_SERIES']
TR['IWF'] = IWF_TR['TR_SERIES']

TR = pd.DataFrame()
        
IND1=pd.DataFrame()
IND2=pd.DataFrame()
IND3=[]
l5= []
l6=[]
IND_1ALL=pd.DataFrame()
IND_2ALL=pd.DataFrame()
IND_1ALL_BIN= pd.DataFrame()
IND_2ALL_BIN=pd.DataFrame()
IND_3ALL_BIN=pd.DataFrame()

        
CALC_START_DATE = '2004-12-31'#'2005-01-01'  #'2004-12-31'#
CALC_END_DATE =  '2018-07-31'#'2018-07-31'
CDL = dt.TDL(CALC_START_DATE,CALC_END_DATE,CALENDAR_ID)    
   
def WEIGTHS_CSV(Weights,DATE1):
    for fk in  range(0,NO_CALDAYS):   
        CALC_DATE = CDL[fk] 
        ########Fetching month end dates###########################
        Monthendlist = dt.imp_Nth_date(CALENDAR_ID, 'LAST', '', 'I', TICKER_START_DATE[0], dt.MNTH_OFFSET(TICKER_START_DATE[0],CALC_DATE,'I'))
    
        df_csv = pd.DataFrame(columns = ['code','ticker','isin','name','curr','divcurr','sedol','cusip','countryname', \
                                         'sector','industry','subindustry','share','weight'])
        df_csv['code'] = ['ABCDE','ABCDE','ABCDE','ABCDE','ABCDE'] 
        df_csv['ticker'] =['SPY US EQUITY', 'SPYG US EQUITY', 'SLYG US EQUITY', 'IWF US EQUITY', 'SHY US EQUITY']
        df_csv['isin'] = ['US78462F1030','US78464A4094','US78464A2015','US4642876142','US4642874576']
        df_csv['name'] = ['SPDR S&P 500 ETF','SPDR S&P 500 Growth ETF','S&P 600 Small Cap Growth ETF', \
                          'iShares Russell 1000 Growth ETF','iShares 1-3 Year Treasury Bond ETF']
        df_csv['curr'] = ['USD','USD','USD','USD','USD']
        df_csv['divcurr'] = ['USD','USD','USD','USD','USD']
        df_csv['countryname'] = ['United States','United States','United States','United States','United States']
        df_csv['weight'] = Weights
        
    df_csv.to_csv("E:\EPIC TRUST\Traffic_Light_Large_Cap_Growth_Index\\EXPOSURES\\TLLCGI_" 
                            +DATE1.strftime("%d-%m-%Y")+".csv",index = False)
    
    
    df_csv['weight'] = imp_f_calc('2004-12-31', '2018-07-31',['SPY US EQUITY','SPYG US EQUITY','SLYG US EQUITY','IWF US EQUITY','SHY US EQUITY'], '0', [1], ['EXPOSURE'],['TRADE_DATE','SECURITY_NAME','VALUE'],['TRADE_DATE'])


SPY_TR = pa.TR_SERIES(['SPY US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
SPYG_TR = pa.TR_SERIES(['SPYG US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
SLYG_TR = pa.TR_SERIES(['SLYG US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
SHY_TR = pa.TR_SERIES(['SHY US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID)
IWF_TR = pa.TR_SERIES(['IWF US EQUITY'],CALENDAR_ID,END_DATE,INDEX_ID) 

SPY_TR1 = SPY_TR[['TRADE_DATE','TR_SERIES']].rename(columns = {'TR_SERIES':'SPY'}) 
SPYG_TR1 = SPYG_TR[['TRADE_DATE','TR_SERIES']].rename(columns = {'TR_SERIES':'SPYG'}) 
SLYG_TR1 = SLYG_TR[['TRADE_DATE','TR_SERIES']].rename(columns = {'TR_SERIES':'SLYG'}) 
IWF_TR1 = IWF_TR[['TRADE_DATE','TR_SERIES']].rename(columns = {'TR_SERIES':'IWF'}) 
SHY_TR1 = SHY_TR[['TRADE_DATE','TR_SERIES']].rename(columns = {'TR_SERIES':'SHY'}) 

SPY_TR2 = SPY_TR1[SPY_TR1['TRADE_DATE'] >= '2004-12-31'].sort_values('TRADE_DATE')
SPYG_TR2 = SPYG_TR1[SPYG_TR1['TRADE_DATE'] >= '2004-12-31'].sort_values('TRADE_DATE')
SLYG_TR2 = SLYG_TR1[SLYG_TR1['TRADE_DATE'] >= '2004-12-31'].sort_values('TRADE_DATE')
IWF_TR3 = IWF_TR3[IWF_TR3['TRADE_DATE'] >= '2004-12-31'].sort_values('TRADE_DATE')
SHY_TR2 = SHY_TR1[SHY_TR1['TRADE_DATE'] >= '2004-12-31'].sort_values('TRADE_DATE')

SPY_TR3 = Monthendlist.merge(SPY_TR2, how= 'left', on ='TRADE_DATE', left_index=False, right_index=False) 
SPYG_TR3 = Monthendlist.merge(SPYG_TR2, how= 'left', on ='TRADE_DATE', left_index=False, right_index=False) 
SLYG_TR3 = Monthendlist.merge(SLYG_TR2, how= 'left', on ='TRADE_DATE', left_index=False, right_index=False)
IWF_TR3 = Monthendlist.merge(IWF_TR3, how= 'left', on ='TRADE_DATE', left_index=False, right_index=False)  
SHY_TR3 = Monthendlist.merge(SHY_TR2, how= 'left', on ='TRADE_DATE', left_index=False, right_index=False) 

OP = SPY_TR3.merge(SPYG_TR3, how= 'left', on ='TRADE_DATE', left_index=False, right_index=False) 
OP1 = OP.merge(SLYG_TR3, how= 'left', on ='TRADE_DATE', left_index=False, right_index=False) 
OP2 = OP1.merge(IWF_TR3, how= 'left', on ='TRADE_DATE', left_index=False, right_index=False) 
OP3 = OP2.merge(SHY_TR3, how= 'left', on ='TRADE_DATE', left_index=False, right_index=False) 

OP3 = OP3[OP3['TRADE_DATE'] >= '2004-12-31'].sort_values('TRADE_DATE')

Monthendlist = dt.imp_Nth_date(CALENDAR_ID, 'LAST', '', 'I', '2004-12-31', dt.MNTH_OFFSET('2004-12-31',END_DATE,'I'))

OP = []
  

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        