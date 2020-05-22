# calender/SelectionDate2_rule.py
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

def SelectionDate_Calculate(day,month,year,rule,holidays):
 if(rule==1):
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
  elif day==0:
    x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 3);
  elif day==1:
    x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 4);
  elif day==2:
    x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 5);
  elif day==3:
    x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 6);
  else:
    x = datetime.datetime(x.year,x.month,x.day)

 elif(rule==2):
     if(calendar.isleap(year)):
             if(month== 4 or month==6 or month == 9 or month==11 or month==1 or month==8 or month==2):
                 x = datetime.datetime(year,month,day) - timedelta(days = 31);
             elif(month==5 or month==10 or month==7 or month==12):
                 x = datetime.datetime(year,month,day) - timedelta(days = 30);
             else:
                 x = datetime.datetime(year,month,day) - timedelta(days = 29);
     else:
             if(month==5 or month==10 or month==7 or month==12 or month==1 or month==8):
                 x = datetime.datetime(year,month,day) - timedelta(days = 31);
             elif(month== 4 or month==6 or month == 9 or month==11):
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



 elif(rule==3):
     i =0;
     x = datetime.datetime(year,month,day);
     while(i<12):
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

 elif(rule==4):
     i =0;
     x = datetime.datetime(year,month,day);
     while(i<17):
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
         sel_date = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 2);
     if(day==5):
         sel_date = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 1);

 elif(rule==5):
     i =1;
     x = datetime.datetime(year,month,day);
     while(i<17):
         day= calendar.weekday(x.year,x.month,x.day)
         if(day!=5 and day!=6):
            i = i+1;
         x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 1)
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
        sel_date = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 2);
     if(day==5):
        sel_date = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 1);


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
      num_day = ad;
      week_day, lastday = calendar.monthrange(year,month)
      count_days = 0
      while(num_day != lastday):

         day= calendar.weekday(x.year,x.month,x.day)
         if(day!=5 and day!=6):
             count_days = count_days+1

         x = datetime.datetime(x.year,x.month,x.day) + timedelta(days = 1);
         num_day = num_day+1;

      if(count_days<=7):
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
 x_convention= x.strftime("%x")
 x_convention= datetime.datetime.strptime(x_convention,"%m/%d/%y").strftime("%Y/%m/%d")
 y1 = int(x_convention[:4])
 holiday_check = datetime.datetime(y1,x.month,x.day)
 if holiday_check in holidays:
        x = datetime.datetime(x.year,x.month,x.day) - timedelta(days = 1);
        return x.strftime("%x")
 else:
        return x.strftime("%x")

