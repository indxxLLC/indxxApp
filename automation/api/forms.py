# api/forms.py
"""
 * Version : 1.0
 * Project: Calendar Automation
 * Copyright : Indxx Capital Management
 * Author: Pavan Rajput
 * Created Date: 08-04-2019
 * Modified Date: dd-mm-yyyy
 * Licensed under : Self
"""
from django import forms
from django.forms import ModelForm
from api.models import Calendarlist, Reg_index

class RegIndexForm(ModelForm):
  class Meta:
    model = Reg_index
    fields = ["Ident_ISIN", "Ident_Bloomberg", "Ident_Reuters", "Index_Name", "Client_Name", "Ind_Sty", "Ind_Ver", "Ind_Ver_ID", "Calc", "Calc_Agent", "Data_Platform", "Data_Vendors", "Contract_Type", "Type_of_Ind", "Product_Status", "ETF_Launched", "Reconstitution", "Rebalance", "Review", "Theme_Review", "Selection_Date_Cycle_1", "Completion_Date", "Selection_Date_Cycle_2", "Ind_Cmte_Comm_Date", "Prelim_Comm_Date", "Weights_Share_Freeze_Date", "Public_Announcement_Date", "Client_Comm_Date", "Comm_to_Calc_Agent", "Effective_Date"]
