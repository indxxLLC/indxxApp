#!/usr/bin/env python



import smtplib
from email.message import EmailMessage
import email.utils

def send_mail(body):
	try:
		smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
	except Exception as e:
		print(e)
		smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login('notifications@indxx.com', "Traffic@1234")
	smtpObj.sendmail('notifications@indxx.com', ['pavank@indxx.com'], body) # Or recipient@outlook
	smtpObj.quit()
	pass

def my_scheduled_job():
	body = 'Subject: Email testing'+'\n' + '\nHello, \n\n Email testing for calendar automation\n' + '\nHave a nice day!'
	send_mail(body)