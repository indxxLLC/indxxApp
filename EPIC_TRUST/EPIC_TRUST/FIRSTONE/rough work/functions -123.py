# -*- coding: utf-8 -*-
"""
Functions.py

@author: ssstipirneni
"""
import datetime
import time
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "stipirneni@indxx.com" #Should be replaced by Prod mail_Id
toaddr = ["stipirneni@indxx.com"] # List of Handling team emails

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
    mailserver.sendmail(fromaddr,toaddr,message) 
    mailserver.quit()

#Completion mail with output file  
def success_send_attach(file_path):
    msg = MIMEMultipart()
    msg['Subject'] = "Otput File"    
    attachment = open(file_path, "rb") #Give a excel file and try this
    #Attachment Arrangement
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % file_path.split('\\')[-1])
    msg.attach(part)
    #Server settings
    server = smtplib.SMTP('smtp.office365.com',587)
    server.starttls()
    server.login(fromaddr, base64.b64decode('S2luZ0AxMjMk').decode('utf-8')) 
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    attachment.close()

#Finding the third friday of any given month
    