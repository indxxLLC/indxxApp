# calender/SelectionDate1_rule.py
"""
 * Version : 1.0
 * Project: Calendar Automation
 * Copyright : Indxx Capital Management
 * Author: Pavan Rajput
 * Created Date: 08-04-2019
 * Modified Date: dd-mm-yyyy
 * Licensed under : Self
"""
import calendar
import datetime
from datetime import date, timedelta
import datetime as dt

def selection_date_1_Calculate(day,month,year,holidays):
     if(calendar.isleap(year)):
             if(month== 4 or month==6 or month == 9 or month==11 or month==1 or month==8 or month==2):
                 x = datetime.datetime(year,month,day) - timedelta(days = 31);
             elif(month==5 or month==10 or month==7 or month==12):
                 x = datetime.datetime(year,month,day) - timedelta(days = 30);
             else:
                 x = datetime.datetime(year,month,day) - timedelta(days = 29);
     else:
             if(month== 4 or month==6 or month == 9 or month==11 or month==1 or month==8 or month==2):
                 x = datetime.datetime(year,month,day) - timedelta(days = 31);
             elif(month==5 or month==10 or month==7 or month==12):
                 x = datetime.datetime(year,month,day) - timedelta(days = 30);
             else:
                 x = datetime.datetime(year,month,day) - timedelta(days = 28);

     x_convention= x.strftime("%x")
     x_convention= datetime.datetime.strptime(x_convention,"%m/%d/%y").strftime("%Y/%m/%d")
     y1 = int(x_convention[:4])
     holiday_check = datetime.datetime(y1,x.month,x.day)
     if holiday_check in holidays:
         x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 1);
     else:
         pass

     
     day= calendar.weekday(x.year,x.month,x.day)

     if day==6:
       x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 2);
     elif day == 5:
       x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 1);
     else:
       x = datetime.datetime(x.year,x.month,x.day)

     x_convention= x.strftime("%x")
     x_convention= datetime.datetime.strptime(x_convention,"%m/%d/%y").strftime("%Y/%m/%d")
     y1 = int(x_convention[:4])
     holiday_check = datetime.datetime(y1,x.month,x.day)
     if holiday_check in holidays:
        x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 1);
        return x.strftime("%x")
     else:
        return x.strftime("%x")
