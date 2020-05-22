import bs4 as bs
import requests
import pyodbc as ms
import time as dt
import datetime
import smtplib
import time

endDate = datetime.datetime.now().strftime('%Y%m%d')
startDate = datetime.datetime.now() - datetime.timedelta(days=6)
startDate = (startDate.strftime('%Y%m%d'))


def save_crypto_tickers(urlname):
    
#    resp = requests.get("https://coinmarketcap.com//currencies//"+urlname+"//historical-data//?start="+startDate+"&end="+endDate)

    resp = requests.get('https://coinmarketcap.com/currencies/'+urlname+'/historical-data/?start=20191104&end=20191110')
    
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table',{'class':"table"})
    tickers = []
    ticker = []
    for row in table.findAll('tr')[1:]:
        
        if(row.findAll('td')[0].text == "No data was found for the selected time period."):
            tickers = [('2019-11-04', '0', '0', '0', '0', '0', '0')]
        else:    
            rawDate = dt.strptime(row.findAll('td')[0].text, "%b %d, %Y")  
            date = dt.strftime("%Y-%m-%d", rawDate)
            opn = row.findAll('td')[1].text
            high =  row.findAll('td')[2].text
            low =  row.findAll('td')[3].text
            close =  row.findAll('td')[4].text
            volume =  row.findAll('td')[5].text.replace(',','')
            mcap =  row.findAll('td')[6].text.replace(',','')
            ticker = [date, opn, high, low, close, volume, mcap]
           
            tickers.append(ticker)            
            #with open("crypto.pickle","wb") as f:
            #   pickle.dump(tickers,f)

    #print(tickers)
    print(urlname)
    return tickers
#count = 0
db = ms.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=localhost;"                                                                                                                                                                                                                                                                                                                                                         
                        "Database=Cryptocurrency;"
                        "uid=sa;pwd=f0r3z@786")
cursor = db.cursor()
sql = "SELECT * FROM [dbo].[crypto-coin-detail-prog]"
# execute SQL query using execute() method.
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    #print(results)
    for row in results:
        if row[0] > 0:
            if row[0] % 3 == 0:
               time.sleep(30)
            if row[0] != 157 and row[0] != 168 and row[0] != 361 and row[0] != 400 and row[0] != 686 and row[0] != 773 and row[0] != 956 and row[0] != 1097 and row[0] != 226 and row[0] != 482 and row[0] != 497 and row[0] != 515 and row[0] != 541 and row[0] != 560 and row[0] != 800 and row[0] != 862 and row[0] != 900 and row[0] != 1090: #685 - parkbyte    #156 - arcblock 225 - blockmesh ,481 - uttoken
                coinPrice = save_crypto_tickers(row[3])
                
                #print(coinPrice)
                for row2 in coinPrice:
            #            print(row[0])
            #             sql2 = "INSERT INTO [dbo].[daily-ohlcvm-prog] ([coinId], [edate], [Oprice], [high], [low], [Cprice], [volume], [marketcap]) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                    sql2 = "INSERT INTO [dbo].[daily-ohlcvm-prog] ([coinId], [edate], [Oprice], [high], [low], [Cprice], [volume], [marketcap]) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"    
                    # execute SQL query using execute() method.
                    try:
            #                 cursor.execute(sql2, (row[0], row2[0], row2[1], row2[2], row2[3], row2[4], row2[5], row2[6]))
                        cursor.execute(sql2, (row[0], row2[0], row2[1], row2[2], row2[3], row2[4], row2[5], row2[6]))
                        cursor.commit()
                    except ms.Error as ex:
                        sqlstate = ex.args[1]
                        print(sqlstate) 
                    
    sender = 'crypto@204.80.90.133.com'
    #  receivers = ['kghildyal@indxx.com']
    receivers = ['mjain@indxx.com']

    
    message = """From: From Crypto <crypto@204.80.90.133.com>
    To: To Person <mjain@indxx.com>
    Subject: SMTP e-mail test
    
    This is a test e-mail message.
    """
    
    try:
       smtpObj = smtplib.SMTP('localhost:25')
       smtpObj.sendmail(sender, receivers, message)         
       print("Successfully sent email")
    except smtplib.SMTPException as e:
       print(str(e))   
     
    smtpObj.quit() 
except ms.Error as ex:
    sqlstate = ex.args[1]
    print(sqlstate)
db.close()