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


from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from numpy import inf, nan
from pandas import DataFrame, read_csv
import math
import pandas as pd

# TODO : Improve Function to get Custom Effective dates
def get_backtest_dates(eff_date : date) :
    bktest_dates : list = [eff_date]
    for i in range(int(12*num_bktest_years)) :
        i_th_date : date = eff_date.replace(day = 1) - timedelta(days = 1)
        eff_date : date = i_th_date
        bktest_dates.append(eff_date)
#    DataFrame(data = bktest_dates[-1::-1], columns = ["Backtest Date"])\
#        .reset_index(drop = True)\
#        .to_csv(path_or_buf = "C://Users//Test/Desktop//Crypto Currency Index//Python Files//Crypto Index//Data//Index//Backtest_Dates.csv", index = False)
    return bktest_dates[-1::-1]

def date_convert(datetim):
    return str(datetim.strftime('%d-%m-%Y'))

def date_convert_1(datetim):
    return datetim.date()

check_date = date.today()
date_1=check_date.replace(day=1,month=check_date.month+1)-timedelta(days=4)

if check_date == date_1:
    
    rebal_date = datetime.strftime(date_1,"%Y-%m-%d")
    
    num_days : int = 1
    num_bktest_years : float = 0.08333
    crypto_masterlist : DataFrame = pd.read_csv(filepath_or_buffer="C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Universe_Masterlist\\CryptoCoin_Masterlist"+ rebal_date +".csv",encoding = "utf-8",parse_dates = ["Launch Date"], dayfirst = True)
    
    LAUNCH_DATES = pd.read_excel("C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Universe_Masterlist\\INFC10_coin_launch_date_look_up.xlsx",parse_dates = ["Launch Date"])
    LAUNCH_DATES = LAUNCH_DATES.drop(columns=['Id','Symbol'])
    LAUNCH_DATES['Launch Date'] = LAUNCH_DATES['Launch Date'].apply(date_convert_1)
    LAUNCH_DATES['Launch Date'] = LAUNCH_DATES['Launch Date'].apply(date_convert)
    
    crypto_masterlist = crypto_masterlist.merge(LAUNCH_DATES,left_on='Coin', right_on='Coin')
    
#    crypto_masterlist["Launch Date"]=crypto_masterlist["Launch Date"].apply(date_convert)
    
    columns : list = ["Lifespan(L)", "Volatality(VOL)", "Trading Volume(V2)", "Trading Volume(V3)",
                      "Trading Volume(V4)", "Network Transaction Volume(NV1)", "Network Transaction Volume(NV2)",
                      "Network Transaction Volume(NV3)", "Network Transaction Volume(NV4)", "Start Price", "End Price","Google_Trend_Score"]
    old_columns : list = ["Current Price", "MCap(MC)", "Trading Volume(V1)", "Num Markets(MK)",
                          "GitHub Commits(Last 4 weeks)", "Reddit Subscribers", "Fb Likes", "Twitter Followers","Google_Trend_Data"]
    
    
    todays_date : date = date.today()
    effective_date : date = date.today()
    backtest_dates : list = get_backtest_dates(eff_date = effective_date)
    
    #crypto_masterlist["Date of Data"] = ""
    
    for eff_date in backtest_dates:
    
        factor_columns : list = ["MCap(MC)", "Num Markets(MK)", "Current Price", "GitHub Commits(Last 4 weeks)",
                                 "Reddit Subscribers", "Fb Likes", "Twitter Followers","Google_Trend_Data"]
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
                coin_history: DataFrame = read_csv(filepath_or_buffer ="C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\after_google_trend\\"+ crypto_masterlist
                                                   .at[index, "Coin"].title() + ".csv", encoding = "utf-8",
                                                   parse_dates = ["Date"], dayfirst = True) \
                    .replace(to_replace = -1, value = 0)
                coin_history["Date"] = coin_history["Date"].map(lambda dt : dt.date())
    
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
    
                # Network Transaction Volume(NV1) - 24h
                # -------------------------------------
                if latest_date >= crypto_launch_date :
                    crypto_masterlist.at[index, "Network Transaction Volume(NV1)"] = \
                        coin_history.loc[start_index, "Network Transaction Volume"]
                else :
                    crypto_masterlist.at[index, "Network Transaction Volume(NV1)"] = -1
    
                # Network Transaction Volume(NV2) - 30D
                # -------------------------------------
                # 1. Get Start/End Date across 30 days
                stop_date : date = latest_date - timedelta(days = 30)
    
                # 2. Calculate the Factor
                if stop_date >= crypto_launch_date :
                    # start_index = coin_history.index[coin_history["Date"] == latest_date].values[0]
                    stop_index = coin_history.index[coin_history["Date"] == stop_date].values[0]
                    crypto_masterlist.at[index, "Network Transaction Volume(NV2)"] = \
                        coin_history.loc[start_index : stop_index, "Network Transaction Volume"].mean()
                else :
                    crypto_masterlist.at[index, "Network Transaction Volume(NV2)"] = -1
    
                # Network Transaction Volume(NV3) - 180D
                # --------------------------------------
                # 1. Get Start/End Date across 30 days
                stop_date : date = latest_date - timedelta(days = 180)
    
                # 2. Calculate the Factor
                if stop_date >= crypto_launch_date :
                    # start_index = coin_history.index[coin_history["Date"] == latest_date].values[0]
                    stop_index = coin_history.index[coin_history["Date"] == stop_date].values[0]
                    crypto_masterlist.at[index, "Network Transaction Volume(NV3)"] = \
                        coin_history.loc[start_index : stop_index, "Network Transaction Volume"].mean()
                else :
                    crypto_masterlist.at[index, "Network Transaction Volume(NV3)"] = -1
    
                # Network Transaction Volume(NV4) - 360D
                # --------------------------------------
                # 1. Get Start/End Date across 30 days
                stop_date : date = latest_date - timedelta(days = 360)
    
                # 2. Calculate the Factor
                if stop_date >= crypto_launch_date :
                    # start_index = coin_history.index[coin_history["Date"] == latest_date].values[0]
                    stop_index = coin_history.index[coin_history["Date"] == stop_date].values[0]
                    crypto_masterlist.at[index, "Network Transaction Volume(NV4)"] = \
                        coin_history.loc[start_index : stop_index, "Network Transaction Volume"].mean()
                else :
                    crypto_masterlist.at[index, "Network Transaction Volume(NV4)"] = -1
    
                # ----------------------------------------------------------------------------------------------------------Suraj's Code
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
                # ----------------------------------------------------------------------------------------------------------Suraj's Code
                
                # Get Start/End Current Price of the Portfolio
                # --------------------------------------------
                '''crypto_masterlist.at[index, "Start Price"] = coin_history[coin_history["Date"] ==
                                                                          start_date]["Current Price"].values[0]
                crypto_masterlist.at[index, "End Price"] = coin_history[coin_history["Date"] ==
                                                                        end_date]["Current Price"].values[0]'''
    
                print("Factors calculated for coin " + str(crypto_masterlist.at[index, "Coin"]))
        print("-"*60)
    
    
        # ==================================================================================================================
    
        # Rating Crypto assets
        # --------------------
        '''factor_columns : list = ["MCap(MC)", "Num Markets(MK)", "Lifespan(L)", "Volatality(VOL)", "Trading Volume(V1)",
                                 "Trading Volume(V2)", "Trading Volume(V3)", "Trading Volume(V4)","Network Transaction Volume(NV1)",\
                                 "Network Transaction Volume(NV2)", "Network Transaction Volume(NV3)", "Network Transaction Volume(NV4)","Google_Trend_Score"]
        rating_columns : list = ["MC_Rating", "MK_Rating", "L_Rating", "VOL_Rating", "V1_Rating", "V2_Rating", "V3_Rating",
                                 "V4_Rating","NV1_Rating","NV2_Rating","NV3_Rating","NV4_Rating","Google_Rating"]'''
        factor_columns : list = ["MCap(MC)", "Num Markets(MK)", "Lifespan(L)", "Volatality(VOL)", "Trading Volume(V1)",
                                 "Trading Volume(V2)", "Trading Volume(V3)", "Trading Volume(V4)",\
                                 "Network Transaction Volume(NV2)", "Network Transaction Volume(NV3)", "Network Transaction Volume(NV4)","Google_Trend_Score"]
        rating_columns : list = ["MC_Rating", "MK_Rating", "L_Rating", "VOL_Rating", "V1_Rating", "V2_Rating", "V3_Rating",
                                 "V4_Rating","NV2_Rating","NV3_Rating","NV4_Rating","Google_Rating"]
    #    factor_columns : list = ["MCap(MC)", "Num Markets(MK)", "Lifespan(L)", "Volatality(VOL)", "Trading Volume(V2)", "Trading Volume(V4)",\
    #                             "Network Transaction Volume(NV2)", "Network Transaction Volume(NV4)","Google_Trend_Score"]
    #    rating_columns : list = ["MC_Rating", "MK_Rating", "L_Rating", "VOL_Rating", "V2_Rating",
    #                             "V4_Rating","NV2_Rating","NV4_Rating","Google_Rating"]
        
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
                crypto_masterlist_zero[factor_columns[factor]] = min_val
                
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
    
        # ------------------------------------------------------------------------------------------------------------------
    
        # Removing "Network Transaction Volume(NV1)","Network Transaction Volume(NV2)","Network Transaction Volume(NV3)"
        # and "Network Transaction Volume(NV4)" - As per Request
        
    #    crypto_masterlist : DataFrame = crypto_masterlist.drop(columns = [
    #        "Network Transaction Volume(NV1)", "Network Transaction Volume(NV2)", "Network Transaction Volume(NV3)",
    #        "Network Transaction Volume(NV4)"])
    
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
        crypto_index.to_csv(path_or_buf = "C:\\CRYPTO_1\\New folder\\Files\\Historical_Data\\Poortfolios\\CryptoIndex_" + str(eff_date).replace("-", "_") + ".csv",
                            index = False)
    
    # ======================================================================================================================
