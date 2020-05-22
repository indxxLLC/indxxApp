# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 06:07:25 2018

@author: Suraj SS Tipirneni
"""

import sys
import time
import requests
import datetime
import pymysql as ms
import pandas as pd
from datetime import timedelta
from pandas import DataFrame

sys.path.insert(0, 'E:\\EPIC_RUST\\Traffic_Light_Large_Cap_Growth_Index\\FUNCTIONS') 
from FUNCTIONS import price_adj_func as pa
from FUNCTIONS  import date_functions as dt
from FUNCTIONS  import reload_func as re
from FUNCTIONS  import functions as func

exec_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d.%H%M%S')
###### Execution Parameters*
CALC_MODE = 'daily1' # possible values:- 'daily'  , 'recalc'
CALENDAR_ID = 1
###### CALCULATION DAYS LIST
n_days_before = datetime.datetime.now()-datetime.timedelta(days=1)
START_DATE = n_days_before.strftime("%Y-%m-0")+str(1)
END_DATE = n_days_before.strftime("%Y-%m-%d")

if CALC_MODE == 'daily':
    CDL = [datetime.datetime.today().strftime("%Y-%m-%d")]
    NO_CALDAYS = 1
else:
    CALC_START_DATE = START_DATE  #'2004-12-31'#
    CALC_END_DATE = END_DATE
    CDL = dt.TDL(CALC_START_DATE,CALC_END_DATE,CALENDAR_ID)
    NO_CALDAYS = len(CDL)

print(CALC_START_DATE)
print(CALC_END_DATE)
print(NO_CALDAYS)

try:
#    if CALC_MODE == 'daily':
#        Q = 'select max(Runtimeid) from d_run_exceptions'
#        con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")        
#        Meas = pd.read_sql(Q, con=con)
#        con.close()
#        if(exec_time - Meas > 1.0):
    for fk in  range(NO_CALDAYS):
        print(str(CDL[fk]))
        re.Reload(str(CDL[fk]),1,1)
    print('Code complete')
except Exception as e:
    func.error_msg(e,'Reload issue')