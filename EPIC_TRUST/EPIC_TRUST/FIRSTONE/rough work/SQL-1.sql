SELECT * FROM epic_trust_vvr.d_dailydatareq;
SELECT * from d_ca;

CREATE TABLE IF NOT EXISTS epic_trust_vvr.d_dailydatareq (
  SLNO INT(11) NOT NULL ,
  INDEX_ID INT(11) NOT NULL ,
  TICKER VARCHAR(45) NOT NULL,
  ISIN VARCHAR(45) NOT NULL,
  CURRENCY VARCHAR(45) NOT NULL,
  SECURITY_TYPE VARCHAR(45) NOT NULL,
  FIELD VARCHAR(45) NOT NULL,
  VALID_FLAG  VARCHAR(5) NOT NULL,
  VALID_FROM date  NOT NULL,
  VALID_TO DATE NOT NULL,
  TS_CREATE  datetime default current_timestamp,
  TS_UPDATE datetime default current_timestamp on update current_timestamp,
  PRIMARY KEY (SLNO)
) ENGINE=InnoDB;

#DROP TABLE epic_trust_vvr.d_dailydatareq;

CREATE TABLE IF NOT EXISTS epic_trust_vvr.s_price (
  TRADE_DATE DATE  NOT NULL,
  TICKER VARCHAR(45) NOT NULL,
  REQ_TYPE VARCHAR(45) NOT NULL,  
  PRICE  double(15,8) NOT NULL,
  DATA_SOURCE VARCHAR(45)  NOT NULL,
  ts_create datetime default current_timestamp,
  ts_update datetime default current_timestamp on update current_timestamp
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS epic_trust_vvr.F_CALC (
  RUNTIMEID double(12,10)  NOT NULL,
  TRADE_DATE DATE  NOT NULL,
  INDEX_ID VARCHAR(45) NOT NULL,
  PORTFOLIO int(11) NOT NULL,
  DESCRIPTION VARCHAR(45) NOT NULL,
  VALUE  double(15,8) NOT NULL,
  VALID_FLAG  VARCHAR(4) NOT NULL,
  VALID_FROM date  NOT NULL,
  VALID_TO date  NOT NULL
  
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS epic_trust_vvr.d_index (
  INDEX_ID int(14)  NOT NULL,
  INDEX_NAME VARCHAR(45) NOT NULL,
  INDEX_ISIN VARCHAR(45) NOT NULL,
  CALENDAR_ID int(11) NOT NULL,
  VALID_FLAG  VARCHAR(4) NOT NULL,
  CURRENCY VARCHAR(10) NOT NULL,
  SCH_START_TIME datetime NOT NULL,
  SCH_END_TIME datetime NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS epic_trust_vvr.d_ca (
  ACTION_ID INT(11) NOT NULL ,

  CORPORATE_ACTION VARCHAR(45) NOT NULL,
  COUNTRY_CODE VARCHAR(10) NOT NULL,
  CURRENCY VARCHAR(45) ,
  DATAPROVIDER VARCHAR(45) NOT NULL,
  EX_DATE DATE NOT NULL,
  IDENTIFIER VARCHAR(45) NOT NULL,
  IDENTIFIER_NAME VARCHAR(45) NOT NULL,
  MODIFY_DATE DATE NOT NULL,
  NAME VARCHAR(100) NOT NULL, 
  RECORD_DATE  DATE NOT NULL,
  STATUS VARCHAR(4) NOT NULL,
  SYMBOL VARCHAR(45) NOT NULL,
  TICKER VARCHAR(45) NOT NULL,
  TS_CREATE  datetime default current_timestamp,
  TS_UPDATE datetime default current_timestamp on update current_timestamp
) ENGINE=InnoDB;

ALTER TABLE epic_trust_vvr.d_dailydatareq 
ADD COLUMN FIELD VARCHAR(45) NOT NULL COMMENT '' AFTER SECURITY_TYPE;

select * from d_calendar where TRADE_DATE >= '2018.01001';

SELECT * FROM epic_trust_vvr.d_dailydatareq;
SELECT * FROM epic_trust_vvr.d_price;
SELECT * FROM epic_trust_vvr.d_ca;
delete from d_price where TRADE_DATE = '2018-08-06';
describe s_ca;

LOAD DATA INFILE 'C:/EPIC TRUST/FIRSTONE/DATA/PRICE_IMPORT.csv'
INTO TABLE epic_trust_vvr.d_price
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n';


LOAD DATA INFILE 'C:/EPIC TRUST/FIRSTONE/DATA/DISTRIBUTION HISTORY Public.csv'
INTO TABLE epic_trust_vvr.d_ca
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n';

select * from d_ca;

insert into d_price (TRADE_DATE,TICKER,REQ_TYPE,DATA_SOURCE,PRICE)
select l.TRADE_DATE, l.TICKER, l.REQ_TYPE, l.DATA_SOURCE, l.PRICE
from s_price as l
    left outer join d_price as r on l.TRADE_DATE = r.TRADE_DATE and l.TICKER = r.TICKER  and l.REQ_TYPE = r.REQ_TYPE and l.DATA_SOURCE = r.DATA_SOURCE
where r.TRADE_DATE is null and r.TICKER is null and r.REQ_TYPE is null and r.DATA_SOURCE is null;

delete from d_price ;
delete from d_dailydatareq;

update d_price as l
inner join s_price as r on l.TRADE_DATE = r.TRADE_DATE and l.TICKER = r.TICKER  and l.REQ_TYPE = r.REQ_TYPE and l.DATA_SOURCE = r.DATA_SOURCE
set l.PRICE = r.PRICE;

select a.TRADE_DATE, a.TICKER from (select l.TRADE_DATE,l.TICKER,l.PRICE from d_price as l 
inner join (SELECT   TRADE_DATE FROM  d_calendar
WHERE   TRADE_DATE IN (
    SELECT   MAX(TRADE_DATE)
    FROM     d_calendar
    where TRADING_DAY = 1 and TRADE_DATE <= '2008-01-05' and TRADE_DATE >= DATE_ADD('2008-01-05', INTERVAL -1 MONTH)
    GROUP BY MONTH(TRADE_DATE), YEAR(TRADE_DATE)  )) as r on r.TRADE_DATE = l.TRADE_DATE
    where TICKER in ('SPYG US EQUITY','SPY US EQUITY')
    and REQ_TYPE = 'PX_SETTLE'
    and DATA_SOURCE = 'BLOOMBERG') as a 
PIVOT
    ( a.PRICE for a.TICKER in distinct a.TICKER ) as b
    order by a.TRADE_DATE;
    
    
    
    select l.TRADE_DATE,l.TICKER,l.PRICE from d_price as l 
inner join (SELECT   TRADE_DATE FROM  d_calendar
WHERE   TRADE_DATE IN (
    SELECT   MAX(TRADE_DATE)
    FROM     d_calendar
    where TRADING_DAY = 1 and TRADE_DATE <= '2008-01-05' and TRADE_DATE >= DATE_ADD('2008-01-05', INTERVAL -1 MONTH)
    GROUP BY MONTH(TRADE_DATE), YEAR(TRADE_DATE)  )) as r on r.TRADE_DATE = l.TRADE_DATE
    where TICKER in ('SPYG US EQUITY','SPY US EQUITY')
    and REQ_TYPE = 'PX_SETTLE'
    and DATA_SOURCE = 'BLOOMBERG';
    
    select l.TRADE_DATE,l.TICKER,l.PRICE from d_price as l 
    INNER join (SELECT   distinct TRADE_DATE FROM  d_calendar        WHERE  
    TRADE_DATE IN (        SELECT   MAX(TRADE_DATE)        FROM     d_calendar    
    where TRADING_DAY = 1 and TRADE_DATE <= '2008-01-05' and TRADE_DATE >= DATE_ADD('2008-01-05', INTERVAL -1 MONTH)
    GROUP BY MONTH(TRADE_DATE), YEAR(TRADE_DATE)  )) as r on r.TRADE_DATE = l.TRADE_DATE        where TICKER in ('SPYG US EQUITY', 'SPY US EQUITY')        and REQ_TYPE = 'PX_SETTLE'
    and DATA_SOURCE = 'BLOOMBERG';
    
    

    SELECT   MAX(TRADE_DATE)
    FROM     d_calendar
    where TRADING_DAY = 1 and TRADE_DATE <= '2018-01-05'
    GROUP BY MONTH(TRADE_DATE), YEAR(TRADE_DATE)  ;
    

 select * from f_calc where DESCRIPTION = 'DVD_CASH';
 
 update f_calc
set VALID_TO = DATE('2018-08-20' - INTERVAL 1 DAY)
where
DESCRIPTION = 'DVD_CASH' and RUNTIMEID != 20180820.013232and INDEX_ID = 1;

select DATE('2018-08-20' - INTERVAL 1 DAY);