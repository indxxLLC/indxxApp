# calendar/effectivedate_rule1.py
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
from datetime import date,timedelta
import datetime as dt

def EffectiveDate_Calculate(month,year,rule,holidays):
  if rule==1 or rule==2:
    mycal = calendar.monthcalendar(year,month)
    w1 = mycal[0]
    w2 = mycal[1]
    w3 = mycal[2]
    w4 = mycal[3]

    if w1[calendar.FRIDAY] != 0:
      ad = w3[calendar.FRIDAY]
    else:
      ad = w4[calendar.FRIDAY]


    x = datetime.datetime(year,month,ad)

  elif(rule==3 or rule==4):
      mycal = calendar.monthcalendar(year,month)
      w1 = mycal[0]
      w2 = mycal[1]
      w3 = mycal[2]
      w4 = mycal[3]

      if w1[calendar.FRIDAY] != 0:
          ad = w2[calendar.FRIDAY]
      else:
          ad = w3[calendar.FRIDAY]


      x = datetime.datetime(year,month,ad)


  elif(rule==10 or rule==5):
      num_days = calendar.monthrange(year,month)[1]
      day= calendar.weekday(year,month,num_days)

      if day==6:
         last_day = num_days -2
      elif day == 5:
         last_day = num_days -1
      else:
         last_day = num_days

      x = datetime.datetime(year,month,last_day)

  elif(rule==6 or rule==7):
      mycal = calendar.monthcalendar(year,month)
      w1 = mycal[0]
      w2 = mycal[1]
      w3 = mycal[2]
      w4 = mycal[3]
      if(len(mycal)==5):
          w5 = mycal[4]
          if w5[calendar.FRIDAY] != 0:
              ad = w3[calendar.FRIDAY]
          else:
              ad = w2[calendar.FRIDAY]

      else:
          ad = w2[calendar.FRIDAY]

      x = datetime.datetime(year,month,ad)

  else:
      mycal = calendar.monthcalendar(year,month)
      w1 = mycal[0]
      w2 = mycal[1]
      w3 = mycal[2]
      w4 = mycal[3]
      if(len(mycal)==5):
          w5 = mycal[4]
          if w5[calendar.FRIDAY] != 0:
              ad = w4[calendar.FRIDAY]
          else:
              ad = w3[calendar.FRIDAY]

      else:
          ad = w3[calendar.FRIDAY]




      x = datetime.datetime(year,month,ad)
  if x in holidays:
      x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 1);
      return x.strftime("%x")
  else:
      return x.strftime("%x")











  

