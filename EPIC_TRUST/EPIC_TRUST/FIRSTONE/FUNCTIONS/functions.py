# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 12:43:08 2018

@author: V Vardhan
"""
import pandas as pd
import numpy as np
#from fredapi import Fred
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
import time
import base64
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def BT_WEIGTHS_CSV(ISIN_ARRAY,BT_Weights,Start,End):
    df_csv = pd.DataFrame()
    for k in range(BT_Weights.shape[0]) :
        for l in range(BT_Weights.shape[1]-1):
            df_csv = df_csv.append(pd.Series([k+1,ISIN_ARRAY[l],BT_Weights.iloc[k,l+1]]), ignore_index = True)
    df_csv.columns = ['Period','ISIN','Weights']
    df_csv.to_csv("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\BACKTEST\\ABCDE_BT_" \
                            +Start.strftime("%d-%m-%Y")+"-"+End.strftime("%d-%m-%Y")+".csv",index = False)
    

def EMA1(CDATA,CDATE,PDATE,PERIOD,TICKER_LIST):
    
    x4=pd.ExcelFile("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\EMA\\EMA SHEET-"+str(PERIOD)+".xlsx")
    HIST=x4.parse(str(PERIOD))  
    PREV = HIST.merge(pd.Series(PDATE).to_frame('Date'), left_index=False, right_index=False)
    EMAP = pd.DataFrame(columns = [['Date']+TICKER_LIST] )
    EMAP.loc[0,'Date'] = CDATE
    EMAP[TICKER_LIST] = np.asarray(PREV.iloc[0,1:5].values * (PERIOD-1)/(PERIOD+1) + CDATA.iloc[0,1:5].values * 2/(PERIOD+1))
   
    if (CDATE == HIST['Date']).sum() >0 :
        HIST.loc[CDATE == HIST['Date'],TICKER_LIST] = np.array(EMAP[TICKER_LIST])
    else :            
        HIST = HIST.append( EMAP, ignore_index = True )[EMAP.columns.tolist()]
        
    writer =pd.ExcelWriter("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\EMA\\EMA SHEET-"+str(PERIOD)+".xlsx" ,engine ='xlsxwriter')
    HIST.to_excel(writer,str(PERIOD),index = False)
    
    return HIST

def WEIGTHS_CSV(Weights,DATE1):
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
    
    df_csv.to_csv("E:\\EPIC TRUST\\FIRSTONE\\output\\TLLCGI_"+DATE1.strftime("%d-%m-%Y")+".csv",index = False)
    
    



fromaddr = "stipirneni@indxx.com" #Should be replaced by Prod mail_Id
toaddr = ["vvardhan@indxx.com"] # List of Handling team emails

#Error Notification
def error_msg(e):
    #Time stamp to req date format
    ts = time.time()
    exec_time = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    #Message Arrangement
    SUBJECT = "Error Message"
    message = 'Subject: {}\n\n Exec at: \n\t{} \n\n Error: \n\t{} '.format(SUBJECT, exec_time, e)
    #Server settings
    mailserver = smtplib.SMTP('smtp.office365.com',587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login('stipirneni@indxx.com', base64.b64decode('S2luZ0AxMjMk').decode('utf-8')) #Password for prod email.
    fromaddr = 'stipirneni@indxx.com'
    toaddr = ["stipirneni@indxx.com"]
    mailserver.sendmail(fromaddr,toaddr,message) 
    mailserver.quit()

#Completion mail with output file  
def success_send_attach(file_path):
    msg = MIMEMultipart()
    msg['Subject'] = "Weights File for ABCDE index" 
#    file_path = "C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\EXPOSURE DATA\\ABCD_LIVE_31-12-2009.csv"
    
    ######Attachment Arrangement
    attachment = open(file_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % file_path.split('\\')[-1])
    msg.attach(part)
    
    ########    Mail Body
    content = "Hi Team \n\nPFA weights file for ABCDE index. Kindly upload it to calculation engine. \n\nThanks \nVishnu "                         
    msg.attach(MIMEText(content.encode('utf-8'), 'plain', 'utf-8') )
    
    #########    Server settings
    server = smtplib.SMTP('smtp.office365.com',587)
    server.starttls()
    fromaddr = 'stipirneni@indxx.com'
    toaddr = ["stipirneni@indxx.com"]
    server.login(fromaddr, base64.b64decode('S2luZ0AxMjMk').decode('utf-8'))
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()
    attachment.close()  
    


