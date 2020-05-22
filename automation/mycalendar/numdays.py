import calendar
def num_of_days(mon1,year1):
    if(mon1==1 or mon1==3 or mon1==5 or mon1==7 or mon1==8 or mon1==10 or mon1==12):
        return 31
    elif(mon1==4 or mon1==6 or mon1==9 or mon1==11):
        return 30
    else:
        if(calendar.isleap(year1)):
            return 29
        else:
            return 28
