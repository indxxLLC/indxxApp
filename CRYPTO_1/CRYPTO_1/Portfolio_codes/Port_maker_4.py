# Factors to calculate
# --------------------
# 1.Market Cap (MC)
# 2.Lifespan (L)
# 3.Trading Volume :
# 	a.24hr (V1)  # not needed
# 	b.30D (V2)
# 	c.180D (V3) # not needed
# 	d.360D (V4)
# 4.Volatility (VOL)
# 5.Number of Markets (MK)
# 6.Google Searches (GS)
#   7.Network Transaction Volume:
#  	a.24hr (NV1) # not needed
#  	b.30D (NV2)
#  	c.180D (NV3) # not needed
#   d.360D (NV4)
import datetime as dt
from time import sleep
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from openpyxl import load_workbook
from numpy import inf, nan
from pandas import DataFrame, read_csv,read_excel
import math
import pandas as pd
from requests import adapters, Session
from urllib3 import util
from os import path
import numpy as np

    
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

api_coinmetrics_params : dict = {
    "api" : "assets",
    "datatype" : "TxTfrValAdjUSD"
}

num_retries : int = 3
# sleep for: {backoff factor} * (2 ^ ({number of total retries done} - 1)) within retries
retry = util.retry.Retry(total = num_retries, connect = num_retries, read = num_retries, backoff_factor = 0.2)
http_adapter: adapters.HTTPAdapter = adapters.HTTPAdapter(max_retries = retry)

columns_df : list = ["Id", "Symbol", "Coin", "Current Price", "MCap(MC)", "Trading Volume(V1)"]
columns_history_df : list = ["Date", "Current Price", "Trading Volume"]
crypto_urls : dict = {
    "api_coins_common" : "https://api.coingecko.com/api/v3/coins/",
    "api_all_coins" : "https://api.coingecko.com/api/v3/coins/list",
    "api_coinmetrics" : "https://community-api.coinmetrics.io/v2/"
}

def date_convert(datetim):
    return str(datetim.strftime('%d-%m-%Y'))


crypto_masterlist : DataFrame = pd.read_excel("E:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Universe_Masterlist\CryptoCoin_Masterlist2020-04-27.xlsx",sheet_name='Masterlist')

crypto_masterlist["Launch Date"]=crypto_masterlist["Launch Date"].apply(date_convert)

columns : list = ["Lifespan(L)", "Volatality(VOL)", "Trading Volume(V2)", "Trading Volume(V3)",
                  "Trading Volume(V4)", "Network Transaction Volume(NV1)", "Network Transaction Volume(NV2)",
                  "Network Transaction Volume(NV3)", "Network Transaction Volume(NV4)", "Start Price", "End Price","Google_Trend_Score"]
old_columns : list = ["Current Price","Trading Volume(V1)","Google_Trend_Data"]

todays_date : date = date.today()
effective_date : date = todays_date
backtest_dates = []
backtest_dates.append(effective_date)

#crypto_masterlist["Date of Data"] = ""
NTV_Dataframe=pd.DataFrame()  
for eff_date in backtest_dates:

    factor_columns : list = ["Current Price","Google_Trend_Data"]
    start_date : date = eff_date + timedelta(days = 1)
    end_date = start_date + relativedelta(months = 1) if (effective_date - eff_date).days > 30 else effective_date

    # Make new columns
    for column in old_columns + columns :
        crypto_masterlist[column] = float(0)

    for index in crypto_masterlist.index :
        crypto_masterlist.at[index, "Date of Data"] = eff_date

        # Lifespan(L)
        # -----------
        launch_date : list = crypto_masterlist.at[index, "Launch Date"].split("-")
        crypto_launch_date : date = date(year = int(launch_date[2]), month = int(launch_date[1]),
                                         day = int(launch_date[0]))
        crypto_masterlist.at[index, "Lifespan(L)"] = (eff_date - crypto_launch_date).days

        # --------------------------------------------------------------------------------------------------------------
        if crypto_masterlist.at[index, "Lifespan(L)"] >= 0 :
            
            # Get Historical Data for the coin & replace Unknown values(-1)
            coin_history: DataFrame = read_excel("E:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Prices\\" + crypto_masterlist.at[index, "Coin"].title() + ".xlsx",sheet_name='Sheet1')
            def date_convert_1(datetim):
                return (datetime.strptime(datetim, '%d-%m-%Y')).date()
            coin_history["Date"] = coin_history["Date"].apply(date_convert_1)
            #coin_history["Date"] = coin_history["Date"].map(lambda dt : dt.date())

            # Setting index at Effective date
            # ---------------------------
            start_index = coin_history.index[coin_history["Date"] == eff_date].values[0]

            # Getting Market & Developer data as of Effective date
            # ----------------------------------------------------
            for factor in factor_columns :
                crypto_masterlist.at[index, factor] = coin_history.at[start_index, factor]

            # Volatality(VOL)
            # 1. Get Start/End Date across 1 year
            stop_date : date = eff_date - relativedelta(years = 1)
            num_trading_days: int = (eff_date - stop_date).days

            # 2. Calculate the Factor
            if stop_date < crypto_launch_date :
                stop_date : date = crypto_launch_date

            stop_index = coin_history.index[coin_history["Date"] == stop_date].values[0]
            current_date_data = coin_history.loc[start_index : stop_index - 1, "Current Price"] \
                .reset_index(drop = True)
            previous_date_data = coin_history.loc[start_index + 1 : stop_index, "Current Price"] \
                .reset_index(drop = True)
            coin_history["Daily Returns(%)"] = (current_date_data - previous_date_data) * 100 / previous_date_data
            crypto_masterlist.at[index, "Volatality(VOL)"] = coin_history["Daily Returns(%)"].std() * \
                                                             math.sqrt(num_trading_days)

            # ----------------------------------------------------------------------------------------------------------

            # Trading Volume(V1) - 24h
            # ------------------------
            # 1. Get Date across 1 day
            latest_date: date = eff_date - timedelta(days = 1)
            start_index = coin_history.index[coin_history["Date"] == latest_date].values[0]

            # 2. Calculate the Factor
            if latest_date >= crypto_launch_date :
                crypto_masterlist.at[index, "Trading Volume(V1)"] = coin_history.at[start_index, "Trading Volume"]
            else :
                crypto_masterlist.at[index, "Trading Volume(V1)"] = -1

            # Trading Volume(V2) - 30D
            # ------------------------
            # 1. Get Start/End Date across 30 days
            stop_date: date = latest_date - timedelta(days = 30)

            # 2. Calculate the Factor
            if stop_date >= crypto_launch_date :
                # start_index = coin_history.index[coin_history["Date"] == latest_date].values[0]
                stop_index = coin_history.index[coin_history["Date"] == stop_date].values[0]
                crypto_masterlist.at[index, "Trading Volume(V2)"] = coin_history.loc[
                                                                    start_index : stop_index, "Trading Volume"].mean()
            else :
                crypto_masterlist.at[index, "Trading Volume(V2)"] = -1

            # Trading Volume(V3) - 180D
            # -------------------------
            # 1. Get Start/End Date across 180 days
            stop_date: date = latest_date - timedelta(days = 180)

            # 2. Calculate the Factor
            if stop_date >= crypto_launch_date :
                # start_index = coin_history.index[coin_history["Date"] == latest_date].values[0]
                stop_index = coin_history.index[coin_history["Date"] == stop_date].values[0]
                crypto_masterlist.at[index, "Trading Volume(V3)"] = coin_history.loc[
                                                                    start_index : stop_index, "Trading Volume"].mean()
            else :
                crypto_masterlist.at[index, "Trading Volume(V3)"] = -1

            # Trading Volume(V4) - 360D
            # -------------------------
            # 1. Get Start/End Date across 360 days
            stop_date: date = latest_date - timedelta(days = 360)

            # 2. Calculate the Factor
            if stop_date >= crypto_launch_date :
                # start_index = coin_history.index[coin_history["Date"] == latest_date].values[0]
                stop_index = coin_history.index[coin_history["Date"] == stop_date].values[0]
                crypto_masterlist.at[index, "Trading Volume(V4)"] = coin_history.loc[
                                                                    start_index : stop_index, "Trading Volume"].mean()
            else :
                crypto_masterlist.at[index, "Trading Volume(V4)"] = -1

            # ----------------------------------------------------------------------------------------------------------
            
            Coin_api = get_json_response(url_feed = "https://community-api.coinmetrics.io/v2/assets/")
            
            
            
            eff_date_m1=eff_date-timedelta(1)
            eff_date_m360=eff_date-timedelta(360)
            All_dates = [datetime.strftime(eff_date_m360 + timedelta(days=x),'%Y-%m-%d') for x in range((eff_date_m1-eff_date_m360).days + 1)]
            NTV_Dataframe["Date"]=All_dates
            if crypto_masterlist.at[index, "Symbol"] in Coin_api["assets"] and crypto_masterlist.at[index, "Symbol"] not in 'xmr' and crypto_masterlist.at[index, "Symbol"] not in 'eos' and crypto_masterlist.at[index, "Symbol"] not in 'leo' and crypto_masterlist.at[index, "Symbol"] not in 'vet':
                url_asset_api_in_date : str = crypto_urls["api_coinmetrics"] + api_coinmetrics_params["api"] + "/" + \
                crypto_masterlist.at[index, "Symbol"] + "/metricdata?metrics=" + api_coinmetrics_params["datatype"] + "&start=" + \
                datetime.strftime(eff_date_m360,'%Y%m%d') + "&end=" + datetime.strftime(eff_date_m1,'%Y%m%d')
                Date_Array = []
                
                # Get Response from the API
                coin_history_data = get_json_response(url_feed = url_asset_api_in_date)
                Array=[] 
                for i in range(0,len(coin_history_data["metricData"]["series"])):
                    Array.append(float(coin_history_data["metricData"]["series"][i]["values"][0]))
                    Date_Array.append(coin_history_data["metricData"]["series"][i]["time"][:10])
                for i in range(0,len(NTV_Dataframe["Date"])):
                    if NTV_Dataframe["Date"][i] in Date_Array:
                        NTV_Dataframe.loc[i, crypto_masterlist.at[index, "Symbol"]]=Array[Date_Array.index(NTV_Dataframe["Date"][i])]
                    else:
                        NTV_Dataframe.loc[i, crypto_masterlist.at[index, "Symbol"]]=0
            else:
                Array=[]    
                for i in range(1,len(NTV_Dataframe["Date"])):
                    NTV_Dataframe[crypto_masterlist.at[index, "Symbol"]]=0
            

            NTV_Array=np.array(NTV_Dataframe[crypto_masterlist.at[index, "Symbol"]])
            
            # Network Transaction Volume(NV1) - 24h
            # -------------------------------------
            if latest_date >= crypto_launch_date :
                crypto_masterlist.at[index, "Network Transaction Volume(NV1)"] = (NTV_Dataframe[NTV_Dataframe['Date'] == datetime.strftime(latest_date,'%Y-%m-%d')])[crypto_masterlist.at[index, "Symbol"]].values[0]
            else :
                crypto_masterlist.at[index, "Network Transaction Volume(NV1)"] = 0

            # Network Transaction Volume(NV2) - 30D
            # -------------------------------------
            # 1. Get Start/End Date across 30 days
            stop_date : date = latest_date - timedelta(days = 30)

            # 2. Calculate the Factor
            if stop_date >= crypto_launch_date :
                # start_index = coin_history.index[coin_history["Date"] == latest_date].values[0]
                stop_index = coin_history.index[coin_history["Date"] == stop_date].values[0]
                crypto_masterlist.at[index, "Network Transaction Volume(NV2)"] = np.mean(np.array(NTV_Array[-30:-1]))
            else :
                crypto_masterlist.at[index, "Network Transaction Volume(NV2)"] = 0

            # Network Transaction Volume(NV3) - 180D
            # --------------------------------------
            # 1. Get Start/End Date across 30 days
            stop_date : date = latest_date - timedelta(days = 180)

            # 2. Calculate the Factor
            if stop_date >= crypto_launch_date :
                # start_index = coin_history.index[coin_history["Date"] == latest_date].values[0]
                stop_index = coin_history.index[coin_history["Date"] == stop_date].values[0]
                crypto_masterlist.at[index, "Network Transaction Volume(NV3)"] = np.mean(np.array(NTV_Array[-180:-1]))
            else :
                crypto_masterlist.at[index, "Network Transaction Volume(NV3)"] = 0

            # Network Transaction Volume(NV4) - 360D
            # --------------------------------------
            # 1. Get Start/End Date across 30 days
            stop_date : date = latest_date - timedelta(days = 360)

            # 2. Calculate the Factor
            if stop_date >= crypto_launch_date :
                # start_index = coin_history.index[coin_history["Date"] == latest_date].values[0]
                stop_index = coin_history.index[coin_history["Date"] == stop_date].values[0]
                crypto_masterlist.at[index, "Network Transaction Volume(NV4)"] = np.mean(np.array(NTV_Array))
            else :
                crypto_masterlist.at[index, "Network Transaction Volume(NV4)"] = 0

            # -------------------------------------------------------------------------------------------------------
            #Adding google trends data to factor calculation
            stop_date: date = latest_date - timedelta(days = 360)
            
            # 2. Calculate the Factor
            if stop_date >= crypto_launch_date :
                # start_index = coin_history.index[coin_history["Date"] == latest_date].values[0]
                stop_index = coin_history.index[coin_history["Date"] == stop_date].values[0]
                crypto_masterlist.at[index, "Google_Trend_Score"] = sum(coin_history.loc[
                                                                    start_index : stop_index, "Google_Trend_Data"])
            else :
                crypto_masterlist.at[index, "Google_Trend_Score"] = 0
            # ---------------------------------------------------------------------------------------------------------

            print("Factors calculated for coin " + str(crypto_masterlist.at[index, "Coin"]))
    print("-"*60)
    NTV_Dataframe.to_excel("E:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\NTV_"+str(eff_date)+".xlsx",sheet_name='NTV', header=True, index=False)


    # ==================================================================================================================

    # Rating Crypto assets
    factor_columns : list = ["MCap(MC)", "Num Markets(MK)", "Lifespan(L)", "Volatality(VOL)", "Trading Volume(V1)",
                             "Trading Volume(V2)", "Trading Volume(V3)", "Trading Volume(V4)",\
                             "Network Transaction Volume(NV2)", "Network Transaction Volume(NV3)", "Network Transaction Volume(NV4)","Google_Trend_Score"]
    rating_columns : list = ["MC_Rating", "MK_Rating", "L_Rating", "VOL_Rating", "V1_Rating", "V2_Rating", "V3_Rating",
                             "V4_Rating","NV2_Rating","NV3_Rating","NV4_Rating","Google_Rating"]
    
    Rating_column_Weights = [8, 15, 15, 15, 0, 8, 0, 8, 8, 0, 8, 15]
    crypto_masterlist = crypto_masterlist[(crypto_masterlist['Coin'] != 'Ethereum Classic') & (crypto_masterlist['Coin'] != 'Bitcoin Cash') & \
                                          (crypto_masterlist['Coin'] != 'Bitcoin Gold') & (crypto_masterlist['Coin'] != 'Dogecoin') & (crypto_masterlist['Coin'] != 'Bitcoin SV')]

    rate_num : int = 0
    crypto_masterlist = crypto_masterlist.replace(to_replace = -1, value = 0)

    for factor in range(len(factor_columns)):
        if factor_columns[factor] in ["Volatality(VOL)"] :
            zero_volatality_df : DataFrame = crypto_masterlist[crypto_masterlist["Volatality(VOL)"] <= 0]
            volatality_df : DataFrame = crypto_masterlist[crypto_masterlist["Volatality(VOL)"] > 0]
            volatality_df.sort_values(by = "Volatality(VOL)", ascending = True, inplace = True)
            volatality_df.reset_index(drop = True, inplace = True)
            crypto_masterlist : DataFrame = volatality_df.append(zero_volatality_df)

            crypto_masterlist[rating_columns[rate_num]] = \
                Rating_column_Weights[factor]/100 * crypto_masterlist.iloc[0][factor_columns[factor]] * 100 / crypto_masterlist[factor_columns[factor]]
        else :
            crypto_masterlist_not_zero = crypto_masterlist[crypto_masterlist[factor_columns[factor]] != 0]
            min_val =  min(crypto_masterlist_not_zero[factor_columns[factor]])
            
            crypto_masterlist_zero = crypto_masterlist[crypto_masterlist[factor_columns[factor]] == 0] 
            crypto_masterlist_zero.loc[:,factor_columns[factor]] = min_val
            
            crypto_masterlist = crypto_masterlist_not_zero.append(crypto_masterlist_zero)
            crypto_masterlist = crypto_masterlist.sort_values(by = factor_columns[factor], ascending = False)
            
            crypto_masterlist[rating_columns[rate_num]] = \
                Rating_column_Weights[factor]/100 * crypto_masterlist[factor_columns[factor]] * 100 / crypto_masterlist.iloc[0][factor_columns[factor]]

        rate_num += 1
        print("Factor " + str(factor_columns[factor]) + " rated for all crypto assets.")
    print("-" * 70)

    crypto_masterlist.replace([inf, nan, -inf], 0, inplace = True)
    crypto_masterlist["Net Rating"] = crypto_masterlist[rating_columns].sum(axis = 1)
    crypto_masterlist = crypto_masterlist.sort_values(by = "Net Rating", ascending = False)
    crypto_masterlist.reset_index(drop = True, inplace = True)
    crypto_masterlist.to_excel("E:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Factors"+str(eff_date).replace("-","_")+".xlsx",sheet_name="Sheet1",index=False)
    # ------------------------------------------------------------------------------------------------------------------

    # Removing "Network Transaction Volume(NV1)","Network Transaction Volume(NV2)","Network Transaction Volume(NV3)"
    # and "Network Transaction Volume(NV4)" - As per Request

    # Save Backtest Files
    index_date : str = str(eff_date)
    print("Factors calculated for the crpto --------------------------------------------------------------------" + str(eff_date).replace("-", "_") + ".csv")
    
    # ==================================================================================================================

    # Weighing Crypto Assets
    # ----------------------
    crypto_index : DataFrame = crypto_masterlist.head(10).reset_index(drop = True)
    for i in range(1,len(crypto_index)):
        if crypto_index.loc[i, 'Net Rating'] <= 0:
            crypto_index = crypto_index.drop(crypto_index.index[i])
    
    crypto_index["Weights"] = crypto_index["Net Rating"] * 100 / crypto_index["Net Rating"].sum(axis = 0)
    print("Index for the crpto assets prepared at " + str(eff_date) + " Effective.\n" + "=" * 80)
    crypto_index.to_csv(path_or_buf = "E:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Poortfolios\\" + "CryptoIndex_"+str(eff_date).replace("-", "_") + ".csv",
                        index = False)

# ======================================================================================================================
