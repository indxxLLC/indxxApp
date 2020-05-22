# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:45:56 2019

@author: achauhan
"""
from requests import adapters, Session
from pandas import DataFrame, read_csv,read_excel
from datetime import date, timedelta, datetime, timezone
from time import sleep
from urllib3 import util
from os import path
import pandas as pd
import datetime as dt

# ----------------------------------------------------------------------------------------------------------------------
#  Maintaining the session with the data source API
def get_json_response(url_feed : str, url_params : dict = dict()) :

    # Create Session
    session = Session()
    session.mount("https://", adapter = http_adapter)

    # Hit URL
    response = session.get(url = url_feed, params = url_params)
    response_code : int = -1
    wait_time = 0
    data_struct : dict = dict()

    # Re-create Session for unexpected response
    while response.status_code != 200 :
        session.close()
        # Create Session again
        session = Session()
        session.mount("https://", adapter = http_adapter)
        response = session.get(url = url_feed, params = url_params)

    # Get JSON unless parsed correctly
    while response_code == -1 :
        try :
            sleep(wait_time)
            if response.json() :
                data_struct = response.json()
                response_code : int = 1

        except Exception as ex:
            print("Exception occurred during JSON parsing : " + str(ex))
            wait_time : int = 3
            response_code : int = -1

    return data_struct

# ======================================================================================================================


# Main Script
# -----------

# Define Variables
todays_date : date = date.today()
start_date : date = todays_date-timedelta(1)

crypto_urls : dict = {
    "api_coins_common" : "https://api.coingecko.com/api/v3/coins/",
    "api_all_coins" : "https://api.coingecko.com/api/v3/coins/list",
    "api_coinmetrics" : "https://community-api.coinmetrics.io/v2/"
}

api_coin_data_params : dict = {
    "localization" : "false",
    "sparkline" : "true"
}

num_retries : int = 3
# sleep for: {backoff factor} * (2 ^ ({number of total retries done} - 1)) within retries
retry = util.retry.Retry(total = num_retries, connect = num_retries, read = num_retries, backoff_factor = 0.2)
http_adapter: adapters.HTTPAdapter = adapters.HTTPAdapter(max_retries = retry)
columns_history_df : list = ["Date", "Current Price", "Trading Volume"]

crypto_df = read_excel("E:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Universe_Masterlist\\CryptoCoin_Masterlist2020-03-26.xlsx",sheet_name="Masterlist").head(25)

for index in crypto_df.index :
    print(index)
    if path.exists("E:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Prices\\" + crypto_df.at[index, "Coin"].title() + ".xlsx") :
        crypto_df.loc[index, "Coin Update"] = "Old"
        coin_history : DataFrame = read_excel( "E:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Prices\\" + crypto_df.at[index, "Coin"].title() + ".xlsx",sheet_name='Sheet1')
        crypto_df.loc[index, "Last Updated"] = datetime.strptime(str(coin_history.loc[0, "Date"]), '%d-%m-%Y')
    else :
        crypto_df.loc[index, "Coin Update"] = "New"
        crypto_df.loc[index, "Last Updated"] = "Never"

# ----------------------------------------------------------------------------------------------------------------------

# Update Data for Crypto assets in Masterlist
# Get Historical Data
# -------------------
for index_main in crypto_df.index:
    if crypto_df.at[index_main, "Coin Update"] == "Old" :
        start_date : date = crypto_df.at[index_main, "Last Updated"] + timedelta(days = 1)
        coin_history_dataframe : DataFrame = DataFrame(columns = columns_history_df, index = range((todays_date - start_date.date()).days + 1))
    else:
        start_date : date = date(year = 2018, month = 5, day = 1)
        coin_history_dataframe : DataFrame = DataFrame(columns = columns_history_df, index = range((todays_date - start_date).days + 1))
        
    num_days: int = 0

    for index_hist in coin_history_dataframe.index :

        # Create URL Feed
        url_coin_history : str = crypto_urls["api_coins_common"] + crypto_df.at[index_main, "Id"] + "/history"
        date_before_ndays : date = todays_date - timedelta(days = num_days)
        df_date=dt.datetime.strptime(str(date_before_ndays), '%Y-%m-%d').strftime('%d-%m-%Y')
        date_yyyy_mm_dd : str = str(date_before_ndays.day) + "-" + str(date_before_ndays.month) + "-" + str(date_before_ndays.year)
        param_history_url : dict = {
            "date": str(date_before_ndays.day) + "-" + str(date_before_ndays.month) + "-" + str(date_before_ndays.year),
            "localization": "en"
        }

        # Create Session
        session = Session()
        session.mount("https://", adapter = http_adapter)

        # Get Response from the API
        coin_history_data = get_json_response(url_feed = url_coin_history, url_params = param_history_url)
        coin_history_dataframe.at[index_hist, "Date"] = df_date

        if "market_data" in coin_history_data.keys() :

            # Fetching "Current Price"
            if "current_price" in coin_history_data["market_data"].keys() :
                if coin_history_data["market_data"]["current_price"] is not None :
                    coin_history_dataframe.at[index_hist, "Current Price"] = \
                        coin_history_data["market_data"]["current_price"]["usd"] \
                        if len(coin_history_data["market_data"]["current_price"]) > 0 else -1
                else :
                    coin_history_dataframe.at[index_hist, "Current Price"] = -1
            else :
                coin_history_dataframe.at[index_hist, "Current Price"] = -1

            # Fetching "Trading Volume"
            if "total_volume" in coin_history_data["market_data"].keys() :
                if coin_history_data["market_data"]["total_volume"] is not None :
                    coin_history_dataframe.at[index_hist, "Trading Volume"] = \
                            coin_history_data["market_data"]["total_volume"]["usd"]\
                            if len(coin_history_data["market_data"]["total_volume"]) > 0 else -1
                else :
                    coin_history_dataframe.at[index_hist, "Trading Volume"] = -1
            else :
                coin_history_dataframe.at[index_hist, "Trading Volume"] = -1

        # Create Coinmetrics url feed
        datetime_before_ndays : datetime = datetime(year = date_before_ndays.year, month = date_before_ndays.month,
                                                    day = date_before_ndays.day) - timedelta(days = 1)
        unix_timestamp : int = int(datetime_before_ndays.replace(tzinfo = timezone.utc).timestamp())
       

        print("General Data of " + crypto_df.at[index_main, "Coin"].title() + " at " + date_yyyy_mm_dd +
              " fetched successfully!")
        num_days += 1

    print("-" * 60 + "\n")

    if crypto_df.at[index_main, "Coin Update"] == "Old" :
        coin_history: DataFrame = read_excel( "E:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Prices\\" + crypto_df
                                           .at[index_main, "Coin"].title() + ".xlsx",sheet_name='Sheet1')
        coin_history_dataframe = coin_history_dataframe.append(coin_history)

    # Save Historical Data
    
    writer = pd.ExcelWriter('E:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Prices\\'+crypto_df.at[index_main, "Coin"].title()+'.xlsx') 
    coin_history_dataframe.to_excel(writer , index = False)
    writer.save()