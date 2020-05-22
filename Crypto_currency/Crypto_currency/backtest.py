import pymysql as ms
#import time as dt
import datetime
import calendar

def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)

def portfolioFetch(startDate, limit, investmentVal):
    db = ms.connect("localhost","cry-user","Crypto@123","cryptocurrency")
    cursor = db.cursor()
    rawPortfolio = []
    portfolio = []
    totalMcap = 0
    sql = "SELECT a.id, a.name, b.volume, b.marketcap, b.date FROM `crypto-coin-detail-prog` a JOIN `daily-ohlcvm-prog` b ON a.id = b.coinId WHERE b.date = '"+startDate+"' ORDER BY b.marketcap DESC LIMIT 0,"+limit
    try:
         cursor.execute(sql)
         results = cursor.fetchall()
         for row in results:
             rawPortfolio.append(row)
             totalMcap = totalMcap + row[3]
    except ms.err.InternalError as e:
        msg = e.args
        print(msg)
    db.close()
    
    for row in rawPortfolio:
        weights = (row[3]*100)/totalMcap
        price = fetchPrice(row,startDate)
        shares = (investmentVal*weights)/float(price[1]*100)    
        row = row + (weights,shares,)
        portfolio.append(row)
        
    return(portfolio)

def rebalance(portfolio,date):
    db = ms.connect("localhost","cry-user","Crypto@123","cryptocurrency")
    cursor = db.cursor()
    rawPortfolio = []
    rebalancePortfolio = []
    totalMcap = 0
    for row in portfolio:
        sql = "SELECT marketcap FROM `daily-ohlcvm-prog` WHERE coinId ='"+str(row[0])+"' AND date= '"+ date +"'"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row2 in results:
                row = row + (row2[0],)
                rawPortfolio.append(row)
                totalMcap = totalMcap + row2[0]
        except ms.err.InternalError as e:
            msg = e.args
            print(msg)
    db.close()
    for row in rawPortfolio:
        #print(row)
        weights = (row[6]*100)/totalMcap
        row = row + (weights,)
        rebalancePortfolio.append(row)
    return(rebalancePortfolio)      


#def fetchPrice(portfolio,currDate):
#    price = []
#    db = ms.connect("localhost","cry-user","Crypto@123","cryptocurrency")
#    cursor = db.cursor()
#    for row in portfolio:
#        sql = "SELECT date, close FROM `daily-ohlcvm-prog` WHERE coinId ='"+str(row[0])+"' AND date= '"+ currDate +"'"
#        try:
#            cursor.execute(sql)
#            results = cursor.fetchall()
#            for row2 in results:
#                price.append(row2)
#        except ms.err.InternalError as e:
#            msg = e.args
#            print(msg)
#    db.close()
#    return(price)

def fetchPrice(coinDetails,currDate):
    price = []
    db = ms.connect("localhost","cry-user","Crypto@123","cryptocurrency")
    cursor = db.cursor()
    
    sql = "SELECT date, close FROM `daily-ohlcvm-prog` WHERE coinId ='"+str(coinDetails[0])+"' AND date= '"+ currDate +"'"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row2 in results:
            price = row2
    except ms.err.InternalError as e:
        msg = e.args
        print(msg)
    db.close()
    return(price)


def backtest(startDate, endDate, lastReconDate, lastRebDate, constituentsNumber):
    checkDate = datetime.datetime.strptime(startDate,"%Y-%m-%d").date()
    indexValue = 1000
    investmentValue = 100000
    divisor = 100
    cryptoPortfolio = portfolioFetch(startDate,constituentsNumber,investmentValue)
    print(cryptoPortfolio)
#    counter = 0 #counter for price
#    nofShares = []
    rebDate = []
    recDate = []    
    
#    price = fetchPrice(cryptoPortfolio,startDate)
#    for row in cryptoPortfolio:        
#        weights = row[5]
#        shares = (investmentValue*weights)/float(price[counter][1]*100)
#        #print(row[1]+" "+str(shares)+" "+str(row[5]))
#        counter = counter +1
#        nofShares.append(shares)
#    
    
#    newDate = datetime.datetime.strptime(startDate,"%Y-%m-%d").date()
#    while(lastRebDate > newDate): 
#        if(newDate != datetime.datetime.strptime(startDate,"%Y-%m-%d").date()):
#            rebDate.append(newDate) 
#        newDate = add_months(newDate,1)
       
    #print(rebDate)
    
    newDate = datetime.datetime.strptime(startDate,"%Y-%m-%d").date() +  datetime.timedelta(days = 1)
    while(lastReconDate > newDate): 
        #if(newDate != datetime.datetime.strptime(startDate,"%Y-%m-%d").date()):
        newDate = add_months(newDate,3)
        recDate.append(newDate) 
#        
    print(recDate)
    while(checkDate <= endDate):
        if(not(checkDate not in recDate)):
            cryptoPortfolio = portfolioFetch(str(checkDate),constituentsNumber,investmentValue)
            print(cryptoPortfolio)
#        elif(not(checkDate not in rebDate)):
#            cryptoPortfolio = rebalance(cryptoPortfolio,checkDate,investmentValue)
        
        #################
       ###Calculation###
      #################
        investmentValue = 0
           
        for row in cryptoPortfolio:
            price = fetchPrice(row,str(checkDate))
#            investmentValue = investmentValue + (nofShares[countIndex] * price[countIndex][1])
            investmentValue = investmentValue + (row[6] * price[1])
            
        indexValue = investmentValue / divisor
        print(str(checkDate)+" "+str(indexValue))
        checkDate = checkDate + datetime.timedelta(days = 1)  
        
recon = datetime.date(2017, 9, 30)
reb = datetime.date(2017, 11, 30)
end = datetime.date(2016, 6, 30)
backtest("2015-12-31", end, recon, reb, "25")
        
#def backtest(constituent, incDate):
#    db = ms.connect("localhost","cry-user","Crypto@123","cryptocurrency")
#    cursor = db.cursor()
#    for row in constituent:
#        sql = "SELECT date, close FROM `daily-ohlcvm-prog` WHERE coinId ='"+str(row[0])+"' AND date= '"+ date +"'"
#        try:
#            cursor.execute(sql)
#            results = cursor.fetchall()
#            for row2 in results:
#                row = row + (row2[0],)
#                rawPortfolio.append(row)
#                totalMcap = totalMcap + row2[0]
#        except ms.err.InternalError as e:
#            msg = e.args
#            print(msg)
#    db.close()
#        

#rebalancePortfolio = rebalance(cryptoPortfolio,'2015-01-')
#print(rebalancePortfolio)
#for row in currPortfolio:
