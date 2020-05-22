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
    "api_coinmetrics" : "https://coinmetrics.io/api/v1/"
}

api_coin_data_params : dict = {
    "localization" : "false",
    "sparkline" : "true"
}

api_coinmetrics_params : dict = {
    "api" : "get_asset_data_for_time_range",
    "datatype" : "adjustedtxvolume(usd)"
}

num_retries : int = 3
# sleep for: {backoff factor} * (2 ^ ({number of total retries done} - 1)) within retries
retry = util.retry.Retry(total = num_retries, connect = num_retries, read = num_retries, backoff_factor = 0.2)
http_adapter: adapters.HTTPAdapter = adapters.HTTPAdapter(max_retries = retry)

columns_df : list = ["Id", "Symbol", "Coin", "Current Price", "MCap(MC)", "Trading Volume(V1)", "Num Markets(MK)",
                     "GitHub Commits(Last 4 weeks)", "Reddit Subscribers", "Fb Likes", "Twitter Followers",
                     "Coin Update", "Last Updated"]
columns_history_df : list = ["Date", "Current Price", "MCap(MC)", "Trading Volume", "GitHub Commits(Last 4 weeks)",
                             "Reddit Subscribers", "Fb Likes", "Twitter Followers", "Network Transaction Volume",
                             "Num Markets(MK)"]



crypto_df = read_csv(filepath_or_buffer = "C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Universe_Masterlist\\CryptoCoin_Masterlist2019-05-29.csv").head(25)


for index in crypto_df.index :
    print(index)
    if path.exists("C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\" + crypto_df.at[index, "Coin"].title() + ".xlsx") :
        crypto_df.loc[index, "Coin Update"] = "Old"
        coin_history : DataFrame = read_excel( "C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\" + crypto_df.at[index, "Coin"].title() + ".xlsx",sheet_name='Sheet1')
        crypto_df.loc[index, "Last Updated"] = datetime.strptime(str(coin_history.loc[0, "Date"]), '%d-%m-%Y')
    else :
        crypto_df.loc[index, "Coin Update"] = "New"
        crypto_df.loc[index, "Last Updated"] = "Never"

# ----------------------------------------------------------------------------------------------------------------------

# Update Data for Crypto assets in Masterlist
# Get Historical Data
# -------------------
#index_main=68
for index_main in crypto_df.index:
    if crypto_df.at[index_main, "Coin Update"] == "Old" :
        start_date : date = crypto_df.at[index_main, "Last Updated"] + timedelta(days = 1)
        coin_history_dataframe : DataFrame = DataFrame(columns = columns_history_df, index = range((todays_date - start_date.date()).days + 1))
    else:
        start_date : date = date(year = 2018, month = 6, day = 1)
        coin_history_dataframe : DataFrame = DataFrame(columns = columns_history_df, index = range((todays_date - start_date).days + 1))
    
    coin_history_dataframe["Num Markets(MK)"] = crypto_df.at[index_main, "Num Markets(MK)"]
    num_days: int = 0

    for index_hist in coin_history_dataframe.index :

        # Create URL Feed
        url_coin_history : str = crypto_urls["api_coins_common"] + crypto_df.at[index_main, "Id"] + "/history"
        date_before_ndays : date = todays_date - timedelta(days = num_days)
        df_date=dt.datetime.strptime(str(date_before_ndays), '%Y-%m-%d').strftime('%d-%m-%Y')
#        date_yyyy_mm_dd : str = str(date_before_ndays.year) + "-" + str(date_before_ndays.month) + "-" + \
#            str(date_before_ndays.day)
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

            # Fetching "MCap"
            if "market_cap" in coin_history_data["market_data"].keys() :
                if coin_history_data["market_data"]["market_cap"] is not None :
                    coin_history_dataframe.at[index_hist, "MCap(MC)"] = \
                        coin_history_data["market_data"]["market_cap"]["usd"]\
                        if len(coin_history_data["market_data"]["market_cap"]) > 0 else -1
                else :
                    coin_history_dataframe.at[index_hist, "MCap(MC)"] = -1
            else :
                coin_history_dataframe.at[index_hist, "MCap(MC)"] = -1

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

        if "community_data" in coin_history_data.keys() :

            # Fetching "Fb Likes"
            if "facebook_likes" in coin_history_data["community_data"].keys() :
                var = coin_history_data["community_data"]["facebook_likes"]
                coin_history_dataframe.at[index_hist, "Fb Likes"] = var if var is not None else -1
            else :
                coin_history_dataframe.at[index_hist, "Fb Likes"] = -1

            # Fetching "Twitter Followers"
            if "twitter_followers" in coin_history_data["community_data"].keys() :
                var = coin_history_data["community_data"]["twitter_followers"]
                coin_history_dataframe.at[index_hist, "Twitter Followers"] = var if var is not None else -1
            else :
                coin_history_dataframe.at[index_hist, "Twitter Followers"] = -1

            # Fetching "Reddit Subscribers"
            if "reddit_subscribers" in coin_history_data["community_data"].keys() :
                var = coin_history_data["community_data"]["reddit_subscribers"]
                coin_history_dataframe.at[index_hist, "Reddit Subscribers"] = var if var is not None else -1
            else :
                coin_history_dataframe.at[index_hist, "Reddit Subscribers"] = -1

        if "developer_data" in coin_history_data.keys() :

            # Fetching "GitHub Commits(Last 4 weeks)"
            if "commit_count_4_weeks" in coin_history_data["developer_data"].keys() :
                var = coin_history_data["developer_data"]["commit_count_4_weeks"]
                coin_history_dataframe.at[index_hist, "GitHub Commits(Last 4 weeks)"] = var if var is not None else -1
            else :
                coin_history_dataframe.at[index_hist, "GitHub Commits(Last 4 weeks)"] = -1

        # Create Coinmetrics url feed
        datetime_before_ndays : datetime = datetime(year = date_before_ndays.year, month = date_before_ndays.month,
                                                    day = date_before_ndays.day) - timedelta(days = 1)
        unix_timestamp : int = int(datetime_before_ndays.replace(tzinfo = timezone.utc).timestamp())
        url_asset_api_in_date : str = crypto_urls["api_coinmetrics"] + api_coinmetrics_params["api"] + "/" + \
            crypto_df.at[index_main, "Symbol"] + "/" + api_coinmetrics_params["datatype"] + "/" + \
            str(unix_timestamp) + "/" + str(unix_timestamp)

        # Get Response from the API
        '''coin_history_data = get_json_response(url_feed = url_asset_api_in_date)

        if "result" in coin_history_data.keys() :
            coin_history_dataframe.at[index_hist, "Network Transaction Volume"] = coin_history_data["result"][0][1] \
                if len(coin_history_data["result"]) > 0 else -1
        else :
            coin_history_dataframe.at[index_hist, "Network Transaction Volume"] = -1'''

        print("General Data of " + crypto_df.at[index_main, "Coin"].title() + " at " + date_yyyy_mm_dd +
              " fetched successfully!")
        num_days += 1

    print("-" * 60 + "\n")

    if crypto_df.at[index_main, "Coin Update"] == "Old" :
        coin_history: DataFrame = read_excel( "C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\" + crypto_df
                                           .at[index_main, "Coin"].title() + ".xlsx",sheet_name='Sheet1')
        coin_history_dataframe = coin_history_dataframe.append(coin_history)

    # Save Historical Data
    
    writer = pd.ExcelWriter('C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\'+crypto_df.at[index_main, "Coin"].title()+'.xlsx') 
    coin_history_dataframe.to_excel(writer , index = False)
    writer.save()