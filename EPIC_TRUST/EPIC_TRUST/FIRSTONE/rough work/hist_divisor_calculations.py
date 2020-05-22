# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 13:04:09 2018
HISTORICAL DIVISORS CALCULATION
@author: Administrator
"""

def imp_d_ca_mod(TICKER, VARS):           
    if TICKER == '' :
        str1 = ' '
        desc = ''
    else:
        str1 = 'and a.TICKER in'
        if (len(TICKER) > 1):
            desc = tuple(TICKER)
        else:
            desc = tuple(TICKER) + ('filler_DOnt_care',)   
    if VARS == '':
        var_names_o = '*'
    else:    
        var_names = ''        
        for i in VARS:
            var_names1 = i + ','
            var_names = var_names1 + var_names
        var_names_o = var_names[:-1]  
         
    QUE = '''select {} from d_ca
             where CORPORATE_ACTION = 'DVD_CASH' and TICKER in {} 
             order by EX_DATE and TICKER'''            
    Q = QUE.format(var_names_o,desc)
    con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")        
    Meas = pd.read_sql(Q, con=con)
    con.close()
    return Meas

TICKER = ['SHY US Equity'],'SHYG US Equity','SLYG US Equity','SHY US Equity','IWF US Equity']
VARS = ['TICKER','CP_GROSS_AMT','EX_DATE']
SHY = imp_d_ca_mod(TICKER, VARS)

EX_DATE_TM1 = pd.DataFrame()
c = 0
for i in SHY.EX_DATE:
    EX_DATE_TM1.loc[c,'TM1'] = WORKDAY(str(i),CALENDAR_ID,-1)
    EX_DATE_TM1.loc[c,'EX_DATE'] = str(i)
    c = c+1
    
SHY_TM1_P = pd.DataFrame()
C = 0
for i in EX_DATE_TM1.TM1:
    SHY_TM1_P.loc[C,'price_tm1']= float(imp_d_price('',CALENDAR_ID,str(i),str(i),[TICKER[0]],['PX_SETTLE'],'BLOOMBERG').values)
    SHY_TM1_P['EX_DATE_TM1'] = EX_DATE_TM1.TM1
    C+=1
######  Period Divisor Calculation
SHY = SHY.sort_values(by='EX_DATE', ascending=False)
SHY_TM1_P = SHY_TM1_P.sort_values(by='EX_DATE_TM1', ascending=False)

PRICE = list(SHY_TM1_P.price_tm1)
CA_VALUE  = list(SHY.CP_GROSS_AMT)
diff  = [x1 - x2 for (x1, x2) in zip(PRICE, CA_VALUE)] 
SHY_divisor = [x1 / x2 for (x1, x2) in zip(diff, PRICE)]



len(SHY)
len(SHY_TM1_P)

