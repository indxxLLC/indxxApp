# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 15:48:55 2019

@author: achauhan
"""

from requests import adapters, Session
from pandas import DataFrame, read_csv
from datetime import date, timedelta, datetime, timezone
from time import sleep
from urllib3 import util
from os import path
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

#date check
check_date = date.today()
date_1=check_date.replace(day=1,month=check_date.month+1)-timedelta(days=4)
#check_date=(dt.datetime(2019,7,28)).date()

if check_date == date_1:

    # Main Script
    # -----------
    
    # Define Variables
    todays_date : date = date.today()
    
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
    
    # ----------------------------------------------------------------------------------------------------------------------
    # Create Universe
    
    # Fetch Initial coin Data
    # -----------------------
    
    all_coins = get_json_response(url_feed = crypto_urls["api_all_coins"])
    
    # Create DataFrame
    crypto_df: DataFrame = DataFrame(columns = columns_df, index = range(len(all_coins)))
    
    for index in crypto_df.index :
    
        # Fetching "Id", "Symbol" & "Coin"
        crypto_df.at[index, "Id"] = all_coins[index]["id"]
        crypto_df.at[index, "Symbol"] = all_coins[index]["symbol"]
        crypto_df.at[index, "Coin"] = all_coins[index]["name"]
    
        coin_data = get_json_response(url_feed = crypto_urls["api_coins_common"] + all_coins[index]["id"],
                                      url_params = api_coin_data_params)
    
        if "market_data" in coin_data.keys() :
    
            # Fetching "Current Price"
            if "current_price" in coin_data["market_data"].keys() :
                if len(coin_data["market_data"]["current_price"]) > 0 :
                    crypto_df.at[index, "Current Price"] = coin_data["market_data"]["current_price"]["usd"]
            else :
                crypto_df.at[index, "Current Price"] = -1
    
            # Fetching "MCap"
            if "market_cap" in coin_data["market_data"].keys() :
                if len(coin_data["market_data"]["market_cap"]) > 0 :
                    crypto_df.at[index, "MCap(MC)"] = coin_data["market_data"]["market_cap"]["usd"]
            else :
                crypto_df.at[index, "MCap(MC)"] = -1
    
            # Fetching "Trading Volume"
            if "total_volume" in coin_data["market_data"].keys() :
                if len(coin_data["market_data"]["total_volume"]) > 0 :
                    crypto_df.at[index, "Trading Volume(V1)"] = coin_data["market_data"]["total_volume"]["usd"]
            else :
                crypto_df.at[index, "Trading Volume(V1)"] = -1
    
        if "community_data" in coin_data.keys() :
    
            # Fetching "Fb Likes"
            if "facebook_likes" in coin_data["community_data"].keys() :
                crypto_df.at[index, "Fb Likes"] = coin_data["community_data"]["facebook_likes"]
            else :
                crypto_df.at[index, "Fb Likes"] = -1
    
            # Fetching "Twitter Followers"
            if "twitter_followers" in coin_data["community_data"].keys() :
                crypto_df.at[index, "Twitter Followers"] = coin_data["community_data"]["twitter_followers"]
            else :
                crypto_df.at[index, "Twitter Followers"] = -1
    
            # Fetching "Reddit Subscribers"
            if "reddit_subscribers" in coin_data["community_data"].keys() :
                crypto_df.at[index, "Reddit Subscribers"] = coin_data["community_data"]["reddit_subscribers"]
            else :
                crypto_df.at[index, "Reddit Subscribers"] = -1
    
        if "developer_data" in coin_data.keys() :
    
            # Fetching "GitHub Commits(Last 4 weeks)"
            if "commit_count_4_weeks" in coin_data["developer_data"].keys() :
                crypto_df.at[index, "GitHub Commits(Last 4 weeks)"] = coin_data["developer_data"]["commit_count_4_weeks"]
            else :
                crypto_df.at[index, "GitHub Commits(Last 4 weeks)"] = -1
    
        print("General Data fetched for coin " + all_coins[index]["name"].title())
    print("-"*40)
    
    # Save Coin Universe#######################################################################universe path
    crypto_df.to_csv(path_or_buf = "C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Universe_Masterlist\\CryptoCoin_Universe_"+str(todays_date)+".csv", index = False)
    print("\nUniverse saved at ./Data/CryptoCoin_Universe.csv\n")
    
    # ----------------------------------------------------------------------------------------------------------------------
    
    crypto_df1 : DataFrame = read_csv(filepath_or_buffer = "C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Universe_Masterlist\\CryptoCoin_Universe_"+str(todays_date)+".csv", encoding = "utf-8")
    
    
    #-----------------------------------------------------------------------------------------------------------------------Suraj's Code
    #Popular Stable Coins Add stable coins from universe
    TOP_STABLE_COINS = { "COINS" : ["tether","trueusd","makerdao","bit_shares","usdcoin","Paxos Standard","dogecoin"], "SYMBOL" : ["usdt","tusd","dai","bts","usdc","pax","doge"]}
    TOP_STABLE_COINS_df = DataFrame(TOP_STABLE_COINS)
    
    
    #Removing Stable coins from Master List
    #MOD_CRYPTO_MASTER_LIST = read_csv(filepath_or_buffer = DATA_FILES_PATH + "CryptoCoin_Masterlist.csv", encoding = "utf-8")
    #MOD_CRYPTO_MASTER_LIST.columns = map(str.upper, MOD_CRYPTO_MASTER_LIST.columns)
    
    common = crypto_df.merge(TOP_STABLE_COINS_df, left_on=['Symbol'], right_on=['SYMBOL'])
    FINAL_COIN_LIST = crypto_df1[(~crypto_df1.Symbol.isin(common.SYMBOL))]
    
    FINAL_COIN_LIST_sort = FINAL_COIN_LIST.sort_values(by = 'MCap(MC)', ascending = False)
    #----------------------TO MAINTAIN CONTINUITY
    crypto_df = FINAL_COIN_LIST_sort
    #----------------------TO MAINTAIN CONTINUITY
    
    # Make Masterlist
    crypto_df : DataFrame = crypto_df.sort_values(by = "MCap(MC)", ascending = False).head(25).reset_index(drop = True)
    #-----------------------------------------------------------------------------------------------------------------------Suraj's Code
    
    # Fetching Number of Exchanges as "Num Markets"
    for index in crypto_df.index :
        exchange_list : list = []
        coin_id: str = ""
        page_num: int = 1
        param_exchange_url: dict = {
            "page" : page_num
        }
        num_exchanges: int = 0
        coin_exchange_data = get_json_response(url_feed = crypto_urls["api_coins_common"] +
                                                          crypto_df.at[index, "Id"] + "/tickers",
                                               url_params = param_exchange_url)
    
        if "tickers" in coin_exchange_data.keys() :
            print("Markets counted for " + crypto_df.at[index, "Coin"].title() + " at Page " + str(page_num))
            size : int = len(coin_exchange_data["tickers"])
            while size != 0 :
                for idx in range(0, size) :
    
                    exchange_id : str = coin_exchange_data["tickers"][idx]["market"]["identifier"]
                    if "coin_id" in coin_exchange_data["tickers"][idx].keys() :
                        coin_id : str = coin_exchange_data["tickers"][idx]["coin_id"]
    
                    if exchange_id not in exchange_list and coin_id == crypto_df.at[index, "Id"]:
                        exchange_list.append(exchange_id)
                        num_exchanges += 1
    
                page_num += 1
                param_exchange_url["page"] = page_num
    #            session, coin_exchange_data = get_json_response(url_feed = crypto_urls["api_coins_common"] +
    #                                                                       crypto_df.at[index, "Id"] + "/tickers",
    #                                                            url_params = param_exchange_url)
                coin_exchange_data = get_json_response(url_feed = crypto_urls["api_coins_common"] + crypto_df.at[index, "Id"] + "/tickers",
                                                                url_params = param_exchange_url)
                size: int = len(coin_exchange_data["tickers"])
                if "tickers" not in coin_exchange_data.keys() : break
                print("Markets counted for " + crypto_df.at[index, "Coin"].title() + " at Page " + str(page_num))
    
            crypto_df.at[index, "Num Markets(MK)"] = num_exchanges
        else:
            crypto_df.at[index, "Num Markets(MK)"] = -1
    
    # Save the Masterlist
    crypto_df.to_csv(path_or_buf = "C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Universe_Masterlist\\CryptoCoin_Masterlist"+str(todays_date)+".csv", index = False)
    print("\nMasterlist saved at ./Data/CryptoCoin_Masterlist.csv\n")





