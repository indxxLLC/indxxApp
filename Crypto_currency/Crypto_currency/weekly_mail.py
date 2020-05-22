# -*- coding: utf-8 -*-
"""
 * Version : 1.0
 * Project: Indxx Crypto Currency 
 * Copyright : Indxx Capital Management
 * Author: Pavan Rajput
 * Created Date: 04-05-2020
 * Modified Date: dd-mm-yyyy
 * Licensed under : Self

@author: Pavan Rajput
"""
import datetime
#import timedelta
import pyodbc as ms
import xlsxwriter
import sys
import os
import smtplib

import email.utils
EMAIL_USE_SSL = False
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

today = (datetime.datetime.now()-datetime.timedelta(days=2)).strftime("%Y-%m-%d-%H-%M-%S")
week_start_date = (datetime.datetime.now()-datetime.timedelta(days=8)).strftime("%Y-%m-%d")
week_end_date = (datetime.datetime.now()-datetime.timedelta(days=2)).strftime("%Y-%m-%d")
print(today)
print(week_start_date)
print(week_end_date)
#sys.exit()

filePath = "C:\\Crypto_currency\\weekly_files\\"
#n_days_before = datetime.datetime.now()-datetime.timedelta(days=1)


db = ms.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=192.168.201.55;DATABASE=Cryptocurrency;UID=sa;PWD=f0r3z@786')

cursor = db.cursor()

fileName = 'Crypto_Currency_'+today+'.xlsx'
workbook = xlsxwriter.Workbook(filePath + fileName)
worksheet = workbook.add_worksheet()

SQLCommand = ("SELECT a.name, a.id, b.marketcap, b.Cprice, b.edate FROM  [Cryptocurrency].[dbo].[crypto-coin-detail-prog] a,[Cryptocurrency].[dbo].[daily-ohlcvm-prog] b WHERE a.id = b.coinId AND a.id in (1,2,3,10,4,2196,6,5,15,449,13,7,125,8,55,11,2056,14,16,12,2241,9,18,1751,22,37,19,40,46,17,2234,105,29,25,24,21,1771,1742,23,36,32,61,2208,39,42,52,1291,1382,1377,79,69,101,20,1364,34,38,164,1755,73,128,30,31,58,134,56,49,75,118,60,33,53,27,1871,35,26,54,2160,424,2057,108,64,43,486,731,1791,97,446,28,70,85,135,57,66,88,1991,420,1376,62,47,59) AND b.edate >='" +week_start_date+"' AND b.edate <='"+week_end_date+"'")

data =cursor.execute(SQLCommand)

columns = ['Name', 'Id', 'Marketcap', 'Cprice', 'Edate']

row = 0
col = 0
for j, t in enumerate(columns):
	worksheet.write(row, j, t)	
row +=1

for row_data in data:
	for col, col_data in enumerate(row_data):
		worksheet.write(row, col, col_data)
	print("Inserted row no. : "+str(row))
	row += 1
	
workbook.close()

# to send the mail
def send_mail(body):
    try:
        smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
    except Exception as e:
        print(e)
        smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
    #type(smtpObj) 
    #smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('notifications@indxx.com', "Traffic@1234") 
    smtpObj.sendmail('notifications@indxx.com', msg['To'].split(",")+msg['Cc'].split(","), body) # Or recipient@outlook

    smtpObj.quit()
    pass

if(fileName):
	msg = MIMEMultipart()
	file_location = filePath + fileName
	message = '\nDear Team, \n\n Please find the attached file of Crypto Currency Weekly data. \n' + '\n In case of any query, please contact indexoperations@indxx.com!\n' + '\n Regards, \n Indxx Team'
	msg.attach(MIMEText(message, 'plain'))
	msg['Subject'] = "Crypto Currency Weekly Data"
	msg['To'] = 'rsingh@indxx.com'
	msg['Cc'] = 'pavank@indxx.com'
	#msg['To'] = 'rsingh@indxx.com, skumari@indxx.com, srajvanshi@indxx.com'
	#msg['Cc'] = 'skelumalai@indxx.com, pavank@indxx.com, mjain@indxx.com, sgoyal@indxx.com'
	# Setup the attachment
	filename = os.path.basename(file_location)
	attachment = open(file_location, "rb")
	part = MIMEBase('application', 'octet-stream')
	part.set_payload(attachment.read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

	# Attach the attachment to the MIMEMultipart object
	msg.attach(part)

	text = msg.as_string()
	send_mail(text)
   