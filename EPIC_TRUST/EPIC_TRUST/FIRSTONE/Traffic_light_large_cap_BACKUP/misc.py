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

SPYG_exp = imp_f_calc('2004-12-31', '2018-07-31',['SPY US EQUITY','SPYG US EQUITY','SLYG US EQUITY','IWF US EQUITY','SHY US EQUITY'], '0', [1], ['EXPOSURE'],['TRADE_DATE','SECURITY_NAME','VALUE'],['TRADE_DATE'])

l1 = pd.pivot_table(SPYG_exp, index = 'TRADE_DATE' ,columns='SECURITY_NAME', values= 'VALUE')
writer = pd.ExcelWriter('C:\\Users\\Administrator\\Desktop\\EXPOSURE.xlsx')
l1.to_excel(writer,'exp')
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

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        