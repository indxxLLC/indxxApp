# calender/AnnouncementDate_rule.py
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

def AnnouncementDate_Calculate(day,month,year,rule,holidays):
    if(rule==1):
        i =0;
        x = datetime.datetime(year,month,day);
        while(i<4):
            day= calendar.weekday(x.year,x.month,x.day)
            if(day!=5 and day!=6):
                i = i+1;
            x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 1);
            x_convention= x.strftime("%x")
            x_convention= datetime.datetime.strptime(x_convention,"%m/%d/%y").strftime("%Y/%m/%d")
            y1 = int(x_convention[:4])
            holiday_check = datetime.datetime(y1,x.month,x.day)
            if holiday_check in holidays:
                x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 1);
            else:
                pass

        day= calendar.weekday(x.year,x.month,x.day)
        if(day==6):
            x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 2);
        if(day==5):
            x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 1);

    elif(rule==2):
        x = datetime.datetime(year,month,day) + timedelta(days = 1);
        day= calendar.weekday(x.year,x.month,x.day)
        if(day==6):
            x = datetime.datetime(x.year,x.month,x.day) + timedelta(days = 1);
        if(day==5):
            x = datetime.datetime(x.year,x.month,x.day) + timedelta(days = 2);
        x_convention= x.strftime("%x")
        x_convention= datetime.datetime.strptime(x_convention,"%m/%d/%y").strftime("%Y/%m/%d")
        y1 = int(x_convention[:4])
        holiday_check = datetime.datetime(y1,x.month,x.day)
        if holiday_check in holidays:
            x = datetime.datetime(x.year,x.month,x.day) + timedelta(days = 1);
        else:
            pass




    x_convention= x.strftime("%x")
    x_convention= datetime.datetime.strptime(x_convention,"%m/%d/%y").strftime("%Y/%m/%d")
    y1 = int(x_convention[:4])
    holiday_check = datetime.datetime(y1,x.month,x.day)
    if holiday_check in holidays:
        x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 1);
        return x.strftime("%x")
    else:
        return x.strftime("%x")




