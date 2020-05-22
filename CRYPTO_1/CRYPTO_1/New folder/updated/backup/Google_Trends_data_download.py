# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:58:46 2019
@author: stipirneni

Code tofetch the Google Trends data of the portfolio Constitunts on any given Selection date.
"""
import time
import pandas as pd
from pytrends.request import TrendReq
from openpyxl import load_workbook
import pandas as pd
import csv
import pandas as pd
import numpy as np
import datetime as dt
from datetime import date, timedelta

check_date = date.today()
date_1=check_date.replace(day=1,month=check_date.month+1)-timedelta(days=4)

if check_date == date_1:
    todays_date = date.today()
    DATA_FILES_PATH ="C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Universe_Masterlist\\"
    
    MOD_CRYPTO_MASTER_LIST = pd.read_csv(filepath_or_buffer = DATA_FILES_PATH + "CryptoCoin_Masterlist"+str(todays_date)+".csv", encoding = "utf-8")
    MOD_CRYPTO_MASTER_LIST.columns = map(str.upper, MOD_CRYPTO_MASTER_LIST.columns)
    FINAL_COIN_LIST_sort = MOD_CRYPTO_MASTER_LIST.sort_values(by = 'MCAP(MC)', ascending = False).reset_index(drop=True)
    
    kw_list = list(FINAL_COIN_LIST_sort['SYMBOL'])
    
    """ All the comparisions are done wrt BTC as that's the most famous Crypto Coin. 
        FUTURE TO DO--> In case a different coin gets a 100 score in the relative comparision we need to reset the loop and use that new coin sym as a ref 
                        instead of BTC."""
                        
    pytrends1 = TrendReq(hl='en-US', tz=360, geo='', proxies='')
    trend_data = pd.DataFrame()
    
    for i in range(0,len(kw_list)):
        if i > 0 :
            time.sleep(20)
            pytrends1.build_payload([kw_list[0],kw_list[i]], cat=814, timeframe='today 12-m')     #Building Payload
            sub_frame = pytrends1.interest_over_time()
            sub_frame =  sub_frame.drop(['isPartial','btc'],axis=1)
            trend_data = trend_data.join(sub_frame)
        else:
            pytrends1.build_payload([kw_list[0],kw_list[1]], cat=814, timeframe='today 12-m')
            sub_frame = pytrends1.interest_over_time()
            sub_frame =  sub_frame.drop(['isPartial'],axis=1)
            trend_data= sub_frame
        
    # Google Trends dat Backup
    trend_data.to_csv(path_or_buf = DATA_FILES_PATH+"Google_Trend_Data_100_new.csv", index = True)
    
    #Renaming column names from symbols to data file names
    sym_name=FINAL_COIN_LIST_sort[['SYMBOL','COIN']]
    TRENDS_DATA1 = trend_data
    
    for i in range(0,len(trend_data.columns)):
        TRENDS_DATA1 = TRENDS_DATA1.rename(columns={str(TRENDS_DATA1.columns[i]) : str(sym_name[sym_name['SYMBOL'] == TRENDS_DATA1.columns[i]]['COIN'].values[0])})
    
    TRENDS_DATA1["Date"] = (TRENDS_DATA1.index).date
    TRENDS_DATA2 = TRENDS_DATA1.reset_index(drop=True)
    
    #Changing date formats 
    def date_convert(datetim):
        return str(datetim.strftime('%d-%m-%Y'))
    
    TRENDS_DATA2['Date'] = TRENDS_DATA2['Date'].apply(date_convert)
    
    
    # -------------------------------- Adding Google Trends Data to the data files of individual Coin Files -----------------------------------------------
    
    for i in range(0,len(trend_data.columns)):    
        coin_file = pd.read_csv(filepath_or_buffer = "C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\"  + FINAL_COIN_LIST_sort['COIN'][i] +".csv",parse_dates = ["Date"], dayfirst = True)
        if 'Google_Trend_Data' in coin_file.columns:
            coin_file=coin_file.drop(['Google_Trend_Data'],axis=1)
        coin_file['Date'] = coin_file['Date'].apply(date_convert)
        coin_file_new = pd.merge(coin_file, TRENDS_DATA2[['Date',FINAL_COIN_LIST_sort['COIN'][i]]] ,on='Date',how='left')
        coin_file_new = coin_file_new.rename(columns = {FINAL_COIN_LIST_sort['COIN'][i] : "Google_Trend_Data"})
        coin_file_new["Google_Trend_Data"] = coin_file_new["Google_Trend_Data"].fillna(0)
        
        coin_file_new.to_csv(path_or_buf = "C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\after_google_trend\\" + FINAL_COIN_LIST_sort['COIN'][i] +
                                                    ".csv", index = False)
    

  
###########################ver
    