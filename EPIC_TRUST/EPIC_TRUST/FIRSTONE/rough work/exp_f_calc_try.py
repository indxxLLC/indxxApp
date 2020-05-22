def exp_f_calc(vals,INDEX_ID,TRADE_DATE,RANGE_BREAK_DESC) : 
#    dff = df[['RUNTIMEID','TRADE_DATE', 'INDEX_ID', 'PORTFOLIO', 'DESCRIPTION', 'VALUE','VALID_FLAG', 'VALID_FROM', 'VALID_TO']]
#    vals = dff.values.tolist()   
    if (RANGE_BREAK_DESC == ''):
        con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
        cursor = con.cursor() 
        cursor.executemany("insert into f_calc(RUNTIMEID,TRADE_DATE, INDEX_ID, SECURITY_NAME, PORTFOLIO, DESCRIPTION, VALUE, VALID_FLAG, VALID_FROM, VALID_TO) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;", vals)
        con.commit()
        con.close()    
    
    else:    
        if (len(RANGE_BREAK_DESC) > 1):
            desc = tuple(RANGE_BREAK_DESC)
        else:
            desc = tuple(RANGE_BREAK_DESC) + ('filler_DOnt_care',)                   
        con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
        cursor = con.cursor() 
        cursor.executemany("insert into f_calc(RUNTIMEID,TRADE_DATE, INDEX_ID, SECURITY_NAME, PORTFOLIO, DESCRIPTION, VALUE, VALID_FLAG, VALID_FROM, VALID_TO) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;", vals)
        con.commit()
        
        QUE = '''SELECT INDEX_ID,RUNTIMEID,DESCRIPTION
                 FROM f_calc
                 WHERE RUNTIMEID = (SELECT MAX(RUNTIMEID) FROM F_CALC WHERE RUNTIMEID < (SELECT MAX(RUNTIMEID) FROM F_CALC))
                 AND INDEX_ID = {}  AND DESCRIPTION in {} '''
        Q = QUE.format(INDEX_ID, desc)
        Meas = pd.read_sql(Q, con=con)
        Meas =Meas.drop_duplicates()
        
        for i in Meas.index:
            runid = Meas.loc[i,'RUNTIMEID']
            in_id = Meas.loc[i,'INDEX_ID']
            var = Meas.loc[i,'DESCRIPTION']
            cursor.execute("update f_calc set VALID_TO = DATE(%s - INTERVAL 1 DAY) where DESCRIPTION = %s and RUNTIMEID = %s and INDEX_ID = %s;" , (TRADE_DATE,var,str(runid),in_id))
        
        con.commit()
        con.close()
        
        
def exp_f_calc(VAL,INDEX_ID,SECURITY_NAME,PORTFOLIO,TRADE_DATE,RANGE_BREAK_DESC,RBF) : 
#    dff = df[['RUNTIMEID','TRADE_DATE', 'INDEX_ID', 'PORTFOLIO', 'DESCRIPTION', 'VALUE','VALID_FLAG', 'VALID_FROM', 'VALID_TO']]
#    vals = dff.values.tolist()   
    if (RBF == 'N'):
        con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
        cursor = con.cursor() 
        cursor.executemany("insert into f_calc(RUNTIMEID,TRADE_DATE, INDEX_ID, SECURITY_NAME, PORTFOLIO, DESCRIPTION, VALUE, VALID_FLAG, VALID_FROM, VALID_TO) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;", VAL)
        con.commit()
        con.close()    
    
    else:  
        PORTFOLIO = str(PORTFOLIO)
        INDEX_ID = str(INDEX_ID)
        con = ms.connect("localhost","epicDB","epicDB","epic_trust_vvr")
        cursor = con.cursor() 
        
        QUE = '''SELECT max(RUNTIMEID) AS RUNTIMEID
                 FROM f_calc
                 where DESCRIPTION = '{}' and SECURITY_NAME = '{}' and PORTFOLIO = {} and INDEX_ID = {} '''
        Q = QUE.format(RANGE_BREAK_DESC,SECURITY_NAME,PORTFOLIO,INDEX_ID)
        Meas = pd.read_sql(Q, con=con)
        Meas =Meas.drop_duplicates()
        runid = str(Meas.loc[0,'RUNTIMEID'])
        
        cursor.execute('''  update f_calc
                            set valid_to = DATE(%s - INTERVAL 1 DAY)
                            where valid_to >= %s and valid_from <= %s and RUNTIMEID = %s and DESCRIPTION = %s 
                            and SECURITY_NAME = %s and PORTFOLIO = %s ''',[TRADE_DATE,TRADE_DATE,TRADE_DATE,runid,RANGE_BREAK_DESC,SECURITY_NAME,PORTFOLIO])
        con.commit()
        
        cursor.execute('''  update f_calc
                            set VALID_FLAG = 'N'
                            where  VALID_FROM <= %s and DESCRIPTION = %s and SECURITY_NAME = %s and PORTFOLIO = %s and INDEX_ID = %s''',
                            [TRADE_DATE, RANGE_BREAK_DESC,SECURITY_NAME,PORTFOLIO,INDEX_ID])
      
        cursor.executemany("insert into f_calc(RUNTIMEID,TRADE_DATE, INDEX_ID, SECURITY_NAME, PORTFOLIO, DESCRIPTION, VALUE, VALID_FLAG, VALID_FROM, VALID_TO) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;", VAL)
        
        con.commit()
        con.close()
        
        
exp_f_calc(VAL,INDEX_ID,SECURITY_NAME,PORTFOLIO,TRADE_DATE,RANGE_BREAK_DESC,RBF)