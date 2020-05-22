import bs4 as bs
import requests
import pyodbc as ms

def save_crypto_tickers():
    resp = requests.get('https://coinmarketcap.com/all/views/all/')
    soup = bs.BeautifulSoup(resp.text)
    coins = []
    table = soup.find('table',{'id':"currencies-all"})
    for row in table.findAll('tr')[1:]:
        
        ticker = row.findAll('span',{'class':"currency-symbol"})[0].text
        link = row.findAll('a',{'class':"currency-name-container"})[0].get('href')
        urlname = link[12:-1]
        name = urlname.replace('-',' ').title()
        coin = [ticker, name, urlname]
        coins.append(coin)            
#        print(coin)
#    print(coins)
    return coins

"""
/////////////////////// onnection string using at 204.80.90.133 server ////////////////////////
db = ms.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=localhost;"
                        "Database=Cryptocurrency;"
                        "uid=sa;pwd=f0r3z@786")
"""

db = ms.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=192.168.201.55;DATABASE=Cryptocurrency;UID=sa;PWD=f0r3z@786')

cursor = db.cursor()
coinDetails = save_crypto_tickers()
#print(coinDetails)
for row in coinDetails:
    sql = "SELECT * FROM [dbo].[crypto-coin-detail-prog] WHERE [ticker] = ?"    
    cursor.execute(sql, row[0])
    results = cursor.fetchall()
    if(not results):
        
        sql = "INSERT INTO [dbo].[crypto-coin-detail-prog] ([ticker], [name], [url-name]) VALUES (?, ?, ?)"    
        # execute SQL query using execute() method.  
        try:
            cursor.execute(sql, (row[0], row[1], row[2]))
            cursor.commit()
        except ms.Error as ex:
            sqlstate = ex.args[1]
            print(sqlstate) 
    else:
        continue
    
db.close()