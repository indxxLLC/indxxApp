# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 13:40:54 2018

@author: V Vardhan
"""

###################GET MORE KEYS 
fred = Fred(api_key='f676cd9ed62fc4f49df6aac66d290ba1')
T10Y2Y = fred.get_series('T10Y2Y', observation_start='2014-09-02', observation_end='2014-09-05')
start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2013, 1, 27)

  FROM = "vvardhan@indxx.com"  #Should be replaced by Prod mail_Id
    TO = ["vvardhan@indxx.com"] # List of Handling team emails
    mailserver = smtplib.SMTP('smtp.office365.com',587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login('stipirneni@indxx.com', 'King@123$') #Password for prod email.
    msg.attach(df_csv)
    mailserver.sendmail(FROM,TO,msg)
    mailserver.quit()
    
#import os
#fileslist = os.listdir("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\DATA")
#fileslist=[w.replace("XLSX", "xlsx") for w in fileslist]


#df =[]
#for i in range(len(fileslist)):
#    rawdata=[]
#    temp1=pd.ExcelFile('C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\DATA\\' + fileslist[i])
#    rawdata=temp1.parse('Price History') 
#    rawdata = rawdata[pd.notnull(rawdata.iloc[:,1])]
#    rawdata.columns = rawdata.iloc[0,:]
#    rawdata = rawdata.drop(rawdata.index[0])
#    
#

#    ############################   INDEX LEVEL CALCULATION    ########################################
#    if CALC_DATE != BT_START_DATE :
#        
#        PREV_REBAL_DATE = Monthendlist[CALC_DATE > Monthendlist].iloc[-1]
#        x3 = pd.ExcelFile("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\EXPOSURE DATA\\ABCD_E_" \
#                                +PREV_REBAL_DATE.strftime("%d-%m-%Y")+".xlsx")
#        EFILE=x3.parse('Sheet1') 
#        x4 = pd.ExcelFile("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\IL DATA\\ABCD_E_" \
#                                +PREV_REBAL_DATE.strftime("%d-%m-%Y")+".xlsx")
#        IL_REBAL_DATE = x4.parse('Sheet1')
#        CP_REBAL_DATE = CP.merge(pd.Series(PREV_REBAL_DATE).to_frame('Date'), left_index=False, right_index=False)
#        INDEX_LEVEL.loc[fk,'INDEX_VALUE']  =  IL_REBAL_DATE  * np.matmul(np.asarray(list(CP_CALC_DATE.iloc[0,1:] / CP_REBAL_DATE.iloc[0,1:])),np.array(EFILE))
#    
#    INDEX_LEVEL.to_excel("C:\\Users\\V Vardhan\\Desktop\\EPICTRUST\\IL DATA\\ABCD_E_" \
#                            +CALC_DATE.strftime("%d-%m-%Y")+".xlsx",index = False) 
    

###data load into d_price 
df = pd.read_csv('C:/EPIC TRUST/FIRSTONE/DATA/PRICE_IMPORT.csv',header = None)
df.columns = ['TRADE_DATE', 'TICKER','isin','REQ_TYPE','PRICE','DATA_SOURCE']
#pdb.set_trace()
del df['isin']
vals=df.values.tolist()

con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
cursor = con.cursor()
cursor.execute("delete  from d_price")
cursor.executemany("insert into d_price(TRADE_DATE, TICKER,REQ_TYPE,PRICE,DATA_SOURCE) values (%s, %s,%s, %s,%s)", vals)
con.commit()
con.close() 

df = pd.read_excel('C:/EPIC TRUST/FIRSTONE/DATA/all_dates.csv')
df.columns = ['CALENDAR_ID','TRADE_DATE','DAY','MONTH','YEAR','TRADING_DAY','DAYINWEEK','TR_DAY_MONTH']
vals=df.values.tolist()

con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
cursor = con.cursor()
cursor.execute("delete  from d_calendar")
cursor.executemany("insert into d_calendar(CALENDAR_ID,TRADE_DATE,DAY,MONTH,YEAR,TRADING_DAY,DAYINWEEK,TR_DAY_MONTH) values (%s, %s,%s, %s,%s,%s, %s,%s))", vals)
con.commit()
con.close() 



####loading data into data req table   
df = pd.read_csv('C:/EPIC TRUST/FIRSTONE/DATA/DISTRIBUTION HISTORY Public.csv')
#del df['SLNO']
vals=df.values.tolist()    

con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
cursor = con.cursor()
cursor.execute("delete  from d_ca")
cursor.executemany("insert into d_ca(TICKER,ISIN,EX_DATE,CORPORATE_ACTION,CP_GROSS_AMT,CURRENCY,REC_DATE,PAYMENT_DATE,DATA_SOURCE,CA_TYPE_SP,FREQUENCY) values (%s,%s, %s,%s, %s,%s, %s,%s,%s, %s,%s)", vals)
con.commit()
con.close()    


#    CALC_DATE_INDEX = TDL[TDL['Date'] == CALC_DATE].index
#    CP_CALC_DATE = imp_d_price('E',1,'2018-07-01','2018-07-05',TICKER_LIST,'PX_SETTLE','BLOOMBERG')
#    CP.merge(pd.Series(CALC_DATE).to_frame('Date'), left_index=False, right_index=False)