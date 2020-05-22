import smtplib

# to send the mail
def send_mail(body):
    try:
        smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
    except Exception as e:
        print(e)
        smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
    #type(smtpObj) 
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('notifications@indxx.com', "Traffic@1234") 
    smtpObj.sendmail('notifications@indxx.com', ['pavank@indxx.com'], body) # Or recipient@outlook

    smtpObj.quit()
    pass

if True == True:
	body = 'Subject: Tuttle Response File'+'\n' + '\nHello, \n\n Advance and Decline issues are not available\n' + '\nHave a nice day!'
	send_mail(body)