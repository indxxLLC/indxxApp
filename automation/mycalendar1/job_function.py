from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import loader
from django.template.loader import render_to_string
import calendar
from api.models import Calendarlist, Registerindex, Ruleslist,Priordays
from mycalendar.Priorday import priorday_calculate
from django.utils.translation import ugettext as _
from mycalendar.effectivedate_rule1 import EffectiveDate_Calculate
from mycalendar.AnnouncementDate_rule import AnnouncementDate_Calculate
from mycalendar.SelectionDate2_rule import SelectionDate_Calculate
from mycalendar.FreezeDate_rule import FreezeDate_Calculate
from mycalendar.QualityDate_rule import QualityDate_Calculate
from datetime import date, datetime, timedelta
from mycalendar.Preliminarycommdate_rule import PreliminaryCommDate_Calculate
from mycalendar.CompletionDate_cycle1_rule import CompletionDate_Calculate
from mycalendar.Committee_commdate_rule import Committe_comm_date_Calculate
from mycalendar.SelectionDate1_rule import selection_date_1_Calculate
from django.db.models import Q
from mycalendar.numdays import num_of_days
from openpyxl import Workbook
from mycalendar.mail import send_mail
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
import pdb;

import datetime as dt
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, \
    USMartinLutherKingJr, USPresidentsDay, GoodFriday, USMemorialDay, \
    USLaborDay, USThanksgivingDay


class USTradingCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('NewYearsDay', month=1, day=1, observance=nearest_workday),
        USMartinLutherKingJr,
        USPresidentsDay,
        GoodFriday,
        USMemorialDay,
        Holiday('USIndependenceDay', month=7, day=4, observance=nearest_workday),
        USLaborDay,
        USThanksgivingDay,
        Holiday('Christmas', month=12, day=25, observance=nearest_workday)
    ]
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)

from django.template.loader import render_to_string
from django.utils.html import strip_tags
def mail_index(request):
	client_name = Calendarlist.objects.filter(category = 'Client_Name')
	info = Registerindex.objects.all().order_by('id').reverse()
	inst = USTradingCalendar()
	y1 = date.today().year
	months = dict(January=1, February=2, March=3, April = 4, May=5, June=6, July=7, August=8,September=9, October=10, November=11, December=12)
	holidays = inst.holidays(dt.datetime(y1-1, 9, 30), dt.datetime(y1, 12, 31))
	informa=[]
	months = dict(January=1, February=2, March=3, April = 4, May=5, June=6, July=7, August=8,September=9, October=10, November=11, December=12)
	for ind in info:
		eff_rule=""
		eff_rule_review="";
		eff_rule_rebal="";
		month1="";
		eff_mon=0;
		month1_rebal="";
		eff_mon_rebal=0;
		month1_review="";
		eff_mon_review=0;
		num_month=0;
		num_month_rebal=0;
		num_month_review=0;

		rulelist = Ruleslist.objects.get(index_id=ind.id)
		if(rulelist.eff_rule!=""):
			eff_rule = rulelist.eff_rule
			sel_rule = rulelist.sel_rule1
			sel_rule2 = rulelist.sel_rule2
			fre_rule = rulelist.freeze_rule
			ann_rule = rulelist.announce_rule
			client_comm_rule = rulelist.clientcomm_rule
			Prelim_comm_rule = rulelist.prelim_rule
			month1 = months[ind.reconst_month]
			time = ind.Reconstitution
			cal_month = month1
			if(time=="Annual"):
				num_month=1
				gap=12
			elif(time=="Monthly"):
				num_month =12
				gap=1
			elif(time=="Quarterly"):
				num_month=4
				gap=3
			else:
				num_month=2
				gap=6
			month1 = int(month1)
		if(rulelist.eff_rule_rebal!=""):
			eff_rule_rebal = rulelist.eff_rule_rebal
			sel_rule_rebal = rulelist.sel_rule1_rebal
			sel_rule2_rebal = rulelist.sel_rule2_rebal
			fre_rule_rebal = rulelist.freeze_rule_rebal
			ann_rule_rebal = rulelist.announce_rule_rebal
			client_comm_rule_rebal = rulelist.clientcomm_rule_rebal
			Prelim_comm_rule_rebal = rulelist.prelim_rule_rebal
			month1_rebal = months[ind.rebalance_month]

			month1_rebal = int(month1_rebal)

			time_rebal = ind.Rebalance
			cal_month_rebal = month1_rebal
			if(time_rebal=="Annual"):
				num_month_rebal=1
				gap_rebal=12
			elif(time_rebal=="Monthly"):
				num_month_rebal =12
				gap_rebal=1
			elif(time_rebal=="Quarterly"):
				num_month_rebal=4
				gap_rebal=3
			else:
				num_month_rebal=2
				gap_rebal=6

		if(rulelist.eff_rule_review!=""):
			eff_rule_review = rulelist.eff_rule_review
			sel_rule2_review = rulelist.sel_rule2_review
			fre_rule_review = rulelist.freeze_rule_review
			ann_rule_review = rulelist.announce_rule_review
			client_comm_rule_review = rulelist.clientcomm_rule_review
			Prelim_comm_rule_review = rulelist.prelim_rule_review
			month1_review = months[ind.review_month]
			month1_review = int(month1_review)

			time_review = ind.Review
			cal_month_review = month1_review
			if(time_review=="Annual"):
				num_month_review=1
				gap_review=12
			elif(time_review=="Monthly"):
				num_month_review =12
				gap_review=1
			elif(time_review=="Quarterly"):
				num_month_review=4
				gap_review=3
			else:
				num_month_review=2
				gap_review=6
		d = date.today()
		next_monday = next_weekday(d, 0)
		next_friday = next_weekday(next_monday, 4)

		ind.Selection_Date_Cycle_1_rec="";
		ind.Completion_Date_rec ="";
		ind.Selection_Date_Cycle_2_rec="";
		ind.Ind_Cmte_Comm_Date_rec=""
		ind.Prelim_Comm_Date_rec=""
		ind.Weights_Share_Freeze_Date_rec=""
		ind.Public_Announcement_Date_rec=""
		ind.Client_Comm_Date_rec=""
		ind.Effective_Date_rec=""
		ind.Ind_Cmte_Comm_Date_re=""
		ind.Prelim_Comm_Date_re=""
		ind.Weights_Share_Freeze_Date_re=""
		ind.Public_Announcement_Date_re=""
		ind.Client_Comm_Date_re=""
		ind.Effective_Date_re=""
		ind.Selection_Date_Cycle_2_rev="";
		ind.Ind_Cmte_Comm_Date_rev=""
		ind.Prelim_Comm_Date_rev=""
		ind.Weights_Share_Freeze_Date_rev=""
		ind.Public_Announcement_Date_rev=""
		ind.Client_Comm_Date_rev=""
		ind.Effective_Date_rev=""
		flag=0

		for i in range(0,num_month):
			year = y1
			if(month1>12):
				month1 = month1%12;
			if(month1<cal_month):
				year = year+1
			if eff_rule:
				date1 = EffectiveDate_Calculate(month1,year,int(eff_rule),holidays)
				eff_day = int(date1[3:5])
				eff_month = int(date1[0:2])
				eff_year = int(date1[6:8])
				dt_obj = datetime.strptime(date1,'%m/%d/%y')
				e_date = datetime.strftime(dt_obj, "%Y-%m-%d")
				e_y = int(e_date[:4])
				e_date = date(e_y,eff_month,eff_day)
			if sel_rule2:
				sel_date = SelectionDate_Calculate(eff_day,eff_month,eff_year,int(sel_rule2),holidays)
				sel_day = int(sel_date[3:5])
				sel_month = int(sel_date[0:2])
				sel_year = int(sel_date[6:8])
				dt_obj = datetime.strptime(sel_date,'%m/%d/%y')
				s_date = datetime.strftime(dt_obj, "%Y-%m-%d")
				s_y = int(s_date[:4])
				s_date = date(s_y,sel_month,sel_day)

			if fre_rule:
				freeze_date = FreezeDate_Calculate(eff_day,eff_month,eff_year,int(fre_rule),holidays)
				freeze_day = int(freeze_date[3:5])
				freeze_month = int(freeze_date[0:2])
				freeze_year = int(freeze_date[6:8])
				dt_obj = datetime.strptime(freeze_date,'%m/%d/%y')
				f_date = datetime.strftime(dt_obj, "%Y-%m-%d")
				f_y = int(f_date[:4])
				f_date = date(f_y,freeze_month,freeze_day)
			if(int(ann_rule)==1):
				announce_date = AnnouncementDate_Calculate(eff_day,eff_month,eff_year,int(ann_rule),holidays)
			else:
				announce_date = AnnouncementDate_Calculate(freeze_day,freeze_month,freeze_year,int(ann_rule),holidays)
			announce_day = int(announce_date[3:5])
			announce_month = int(announce_date[0:2])
			announce_year = int(announce_date[6:8])
			dt_obj = datetime.strptime(announce_date,'%m/%d/%y')
			a_date = datetime.strftime(dt_obj, "%Y-%m-%d")
			a_y = int(a_date[:4])
			a_date = date(a_y,announce_month,announce_day)

			if(int(client_comm_rule)==1):
				client_comm_date = AnnouncementDate_Calculate(eff_day,eff_month,eff_year,int(client_comm_rule),holidays)
			else:
				client_comm_date = AnnouncementDate_Calculate(freeze_day,freeze_month,freeze_year,int(client_comm_rule),holidays)
			Client_comm_day = int(client_comm_date[3:5])
			Client_comm_month = int(client_comm_date[0:2])
			Client_comm_year = int(client_comm_date[6:8])
			dt_obj = datetime.strptime(client_comm_date,'%m/%d/%y')
			cl_date = datetime.strftime(dt_obj, "%Y-%m-%d")
			cl_y = int(cl_date[:4])
			cl_date = date(cl_y,Client_comm_month,Client_comm_day)
			Prelim_comm_date = PreliminaryCommDate_Calculate(announce_day,announce_month,announce_year,holidays)
			Prelim_comm_day = int(Prelim_comm_date[3:5])
			Prelim_comm_month = int(Prelim_comm_date[0:2])
			Prelim_comm_year = int(Prelim_comm_date[6:8])
			dt_obj = datetime.strptime(Prelim_comm_date,'%m/%d/%y')
			p_date = datetime.strftime(dt_obj, "%Y-%m-%d")
			p_y = int(p_date[:4])
			p_date = date(p_y,Prelim_comm_month,Prelim_comm_day)

			Completion_date = CompletionDate_Calculate(sel_day,sel_month,sel_year,holidays)
			Completion_month = int(Completion_date[0:2])
			Completion_day = int(Completion_date[3:5])
			dt_obj = datetime.strptime(Completion_date,'%m/%d/%y')
			c_date = datetime.strftime(dt_obj, "%Y-%m-%d")
			c_y = int(c_date[:4])
			c_date = date(c_y,Completion_month,Completion_day)

			if(Prelim_comm_rule==""):
				Committee_comm_date = Committe_comm_date_Calculate(Client_comm_day,Client_comm_month,Client_comm_year,holidays)
			else:
				Committee_comm_date = Committe_comm_date_Calculate(Prelim_comm_day,Prelim_comm_month,Prelim_comm_year,holidays)
			Committee_comm_month = int(Committee_comm_date[0:2])
			Committee_comm_day = int(Committee_comm_date[3:5])
			dt_obj = datetime.strptime(Committee_comm_date,'%m/%d/%y')
			com_date = datetime.strftime(dt_obj, "%Y-%m-%d")
			com_y = int(com_date[:4])
			com_date = date(com_y,Committee_comm_month,Committee_comm_day)
			selection_date1 = selection_date_1_Calculate(sel_day,sel_month,sel_year,holidays)
			sel_1_month = int(selection_date1[0:2])
			sel_1_day = int(selection_date1[3:5])
			dt_obj = datetime.strptime(selection_date1,'%m/%d/%y')
			s1_date = datetime.strftime(dt_obj, "%Y-%m-%d")
			s1_y = int(s1_date[:4])
			sel_1_date = date(s1_y, sel_1_month, sel_1_day)

			cal_month = month1
			month1= month1+gap

			if(next_monday <= e_date and e_date <= next_friday):

				flag=1
				ind.Effective_Date_rec = ind.Effective_Date_rec + date1 + "\n"
			if(next_monday <= s_date and s_date <= next_friday):
				flag=1
				ind.Selection_Date_Cycle_2_rec = ind.Selection_Date_Cycle_2_rec + sel_date + "\n"
			if(next_monday <= f_date and f_date <= next_friday):
				flag=1
				ind.Weights_Share_Freeze_Date_rec = ind.Weights_Share_Freeze_Date_rec + freeze_date + "\n"
			if(next_monday <= a_date and a_date <= next_friday):
				flag=1
				ind.Public_Announcement_Date_rec = ind.Public_Announcement_Date_rec + announce_date + "\n"
			if(next_monday <= cl_date and cl_date <= next_friday):
				flag=1
				ind.Client_Comm_Date_rec = ind.Client_Comm_Date_rec + client_comm_date + "\n"
			if(next_monday <= p_date and p_date <= next_friday):
				flag=1
				ind.Prelim_Comm_Date_rec = ind.Prelim_Comm_Date_rec + Prelim_comm_date + "\n"
			if(next_monday <= c_date and c_date <= next_friday):
				flag=1
				ind.Completion_Date_rec = ind.Completion_Date_rec + Completion_date + "\n"
			if(next_monday <= com_date and com_date <= next_friday):
				flag=1
				ind.Ind_Cmte_Comm_Date_rec = ind.Ind_Cmte_Comm_Date_rec + Committee_comm_date + "\n"
			if(next_monday <= sel_1_date and sel_1_date <= next_friday):
				flag=1
				ind.Selection_Date_Cycle_1_rec = ind.Selection_Date_Cycle_1_rec + selection_date1 + "\n"
		for i in range(0,num_month_rebal):
			year = y1
			if(month1_rebal>12):
				month1_rebal = month1_rebal%12;
			if(month1_rebal<cal_month_rebal):
				year = year+1

			if eff_rule_rebal:
				date1_rebal = EffectiveDate_Calculate(month1_rebal,year,int(eff_rule_rebal),holidays)
				eff_day_rebal = int(date1_rebal[3:5])
				eff_month_rebal = int(date1_rebal[0:2])
				eff_year_rebal = int(date1_rebal[6:8])
				dt_obj = datetime.strptime(date1_rebal,'%m/%d/%y')
				e_date_rebal = datetime.strftime(dt_obj, "%Y-%m-%d")
				e_y_rebal = int(e_date_rebal[:4])
				e_date_rebal = date(e_y_rebal,eff_month_rebal,eff_day_rebal)
				freeze_date_rebal = FreezeDate_Calculate(eff_day_rebal,eff_month_rebal,eff_year_rebal,int(fre_rule_rebal),holidays)
				freeze_day_rebal = int(freeze_date_rebal[3:5])
				freeze_month_rebal = int(freeze_date_rebal[0:2])
				freeze_year_rebal = int(freeze_date_rebal[6:8])
				dt_obj = datetime.strptime(freeze_date_rebal,'%m/%d/%y')
				f_date_rebal = datetime.strftime(dt_obj, "%Y-%m-%d")
				f_y_rebal = int(f_date_rebal[:4])
				f_date_rebal = date(f_y_rebal,freeze_month_rebal,freeze_day_rebal)


			if(int(ann_rule_rebal)==1):
				announce_date_rebal = AnnouncementDate_Calculate(eff_day_rebal,eff_month_rebal,eff_year_rebal,int(ann_rule_rebal),holidays)
			else:
				announce_date_rebal = AnnouncementDate_Calculate(freeze_day_rebal,freeze_month_rebal,freeze_year_rebal,int(ann_rule_rebal),holidays)
			announce_day_rebal = int(announce_date_rebal[3:5])
			announce_month_rebal = int(announce_date_rebal[0:2])
			announce_year_rebal = int(announce_date_rebal[6:8])
			dt_obj = datetime.strptime(announce_date_rebal,'%m/%d/%y')
			a_date_rebal = datetime.strftime(dt_obj, "%Y-%m-%d")
			a_y_rebal = int(a_date_rebal[:4])
			a_date_rebal = date(a_y_rebal,announce_month_rebal,announce_day_rebal)
			if(int(client_comm_rule_rebal)==1):
				client_comm_date_rebal = AnnouncementDate_Calculate(eff_day_rebal,eff_month_rebal,eff_year_rebal,int(client_comm_rule_rebal),holidays)
			else:
				client_comm_date_rebal = AnnouncementDate_Calculate(freeze_day_rebal,freeze_month_rebal,freeze_year_rebal,int(client_comm_rule_rebal),holidays)
			Client_comm_day_rebal = int(client_comm_date_rebal[3:5])
			Client_comm_month_rebal = int(client_comm_date_rebal[0:2])
			Client_comm_year_rebal = int(client_comm_date_rebal[6:8])
			dt_obj = datetime.strptime(client_comm_date_rebal,'%m/%d/%y')
			cl_date_rebal = datetime.strftime(dt_obj, "%Y-%m-%d")
			cl_y_rebal = int(cl_date_rebal[:4])
			cl_date_rebal = date(cl_y_rebal,Client_comm_month_rebal,Client_comm_day_rebal)


			cal_month_rebal = month1_rebal
			month1_rebal= month1_rebal+gap_rebal
			if(next_monday <= e_date_rebal and e_date_rebal <= next_friday):
				flag=1
				ind.Effective_Date_re = ind.Effective_Date_re + date1_rebal + "\n"
			if(next_monday <= f_date_rebal and f_date_rebal <= next_friday):
				flag=1
				ind.Weights_Share_Freeze_Date_re = ind.Weights_Share_Freeze_Date_re + freeze_date_rebal + "\n"
			if(next_monday <= cl_date_rebal and cl_date_rebal <= next_friday):
				flag=1
				ind.Client_Comm_Date_re = ind.Client_Comm_Date_re + client_comm_date_rebal + "\n"
			if(next_monday <= a_date_rebal and a_date_rebal <= next_friday):
				flag=1
				ind.Public_Announcement_Date_re = ind.Public_Announcement_Date_re + announce_date_rebal + "\n"
		for i in range(0,num_month_review):
			year = y1
			if(month1_review>12):
				month1_review = month1_review%12;
			if(month1_review<cal_month_review):
				year = year+1
			if eff_rule_review:
				date1_review = EffectiveDate_Calculate(month1_review,year,int(eff_rule_review),holidays)
				eff_day_review = int(date1_review[3:5])
				eff_month_review = int(date1_review[0:2])
				eff_year_review = int(date1_review[6:8])
				dt_obj = datetime.strptime(date1_review,'%m/%d/%y')
				e_date_review = datetime.strftime(dt_obj, "%Y-%m-%d")
				e_y_review = int(e_date_review[:4])
				e_date_review = date(e_y_review,eff_month_review,eff_day_review)

			if sel_rule2_review:
				sel_date_review = SelectionDate_Calculate(eff_day_review,eff_month_review,eff_year_review,int(sel_rule2_review),holidays)
				sel_day_review = int(sel_date_review[3:5])
				sel_month_review = int(sel_date_review[0:2])
				sel_year_review = int(sel_date_review[6:8])
				dt_obj = datetime.strptime(sel_date_review,'%m/%d/%y')
				s_date_review = datetime.strftime(dt_obj, "%Y-%m-%d")
				s_y_review = int(s_date_review[:4])
				s_date_review = date(s_y_review,sel_month_review,sel_day_review)
			if fre_rule_review:
				freeze_date_review = FreezeDate_Calculate(eff_day_review,eff_month_review,eff_year_review,int(fre_rule_review),holidays)
				freeze_day_review = int(freeze_date_review[3:5])
				freeze_month_review = int(freeze_date_review[0:2])
				freeze_year_review = int(freeze_date_review[6:8])
				dt_obj = datetime.strptime(freeze_date_review,'%m/%d/%y')
				f_date_review = datetime.strftime(dt_obj, "%Y-%m-%d")
				f_y_review = int(f_date_review[:4])
				f_date_review = date(f_y_review,freeze_month_review,freeze_day_review)

			if(int(ann_rule_review)==1):
				announce_date_review = AnnouncementDate_Calculate(eff_day_review,eff_month_review,eff_year_review,int(ann_rule_review),holidays)
			else:
				announce_date_review = AnnouncementDate_Calculate(freeze_day_review,freeze_month_review,freeze_year_review,int(ann_rule_review),holidays)
			announce_day_review = int(announce_date_review[3:5])
			announce_month_review = int(announce_date_review[0:2])
			announce_year_review = int(announce_date_review[6:8])
			dt_obj = datetime.strptime(announce_date_review,'%m/%d/%y')
			a_date_review = datetime.strftime(dt_obj, "%Y-%m-%d")
			a_y_review = int(a_date_review[:4])
			a_date_review = date(a_y_review,announce_month_review,announce_day_review)
			if(int(client_comm_rule_review)==1):
				client_comm_date_review = AnnouncementDate_Calculate(eff_day_review,eff_month_review,eff_year_review,int(client_comm_rule_review),holidays)
			else:
				client_comm_date_review = AnnouncementDate_Calculate(freeze_day_review,freeze_month_review,freeze_year_review,int(client_comm_rule_review),holidays)
			Client_comm_day_review = int(client_comm_date_review[3:5])
			Client_comm_month_review = int(client_comm_date_review[0:2])
			Client_comm_year_review = int(client_comm_date_review[6:8])
			dt_obj = datetime.strptime(client_comm_date_review,'%m/%d/%y')
			cl_date_review = datetime.strftime(dt_obj, "%Y-%m-%d")
			cl_y_review = int(cl_date_review[:4])
			cl_date_review = date(cl_y_review,Client_comm_month_review,Client_comm_day_review)
			Prelim_comm_date_review = PreliminaryCommDate_Calculate(announce_day_review,announce_month_review,announce_year_review,holidays)
			Prelim_comm_day_review = int(Prelim_comm_date_review[3:5])
			Prelim_comm_month_review = int(Prelim_comm_date_review[0:2])
			Prelim_comm_year_review = int(Prelim_comm_date_review[6:8])
			dt_obj = datetime.strptime(Prelim_comm_date_review,'%m/%d/%y')
			p_date_review = datetime.strftime(dt_obj, "%Y-%m-%d")
			p_y_review = int(p_date_review[:4])
			p_date_review = date(p_y_review,Prelim_comm_month_review,Prelim_comm_day_review)
			if(Prelim_comm_rule_review==""):
				Committee_comm_date_review = Committe_comm_date_Calculate(Client_comm_day_review,Client_comm_month_review,Client_comm_year_review,holidays)
			else:
				Committee_comm_date_review = Committe_comm_date_Calculate(Prelim_comm_day_review,Prelim_comm_month_review,Prelim_comm_year_review,holidays)

			Committee_comm_month_review = int(Committee_comm_date_review[0:2])
			Committee_comm_year_review = int(Committee_comm_date_review[6:8])
			Committee_comm_day_review = int(Committee_comm_date_review[3:5])
			dt_obj = datetime.strptime(Committee_comm_date_review,'%m/%d/%y')
			com_date_review = datetime.strftime(dt_obj, "%Y-%m-%d")
			com_y_review = int(com_date_review[:4])
			com_date_review = date(com_y_review,Committee_comm_month_review,Committee_comm_day_review)
			cal_month_review = month1_review
			month1_review= month1_review+gap_review
			if(next_monday <= e_date_review and e_date_review <= next_friday):
				flag=1
				ind.Effective_Date_rev = ind.Effective_Date_rev + date1_review + "\n"
			if(next_monday <= f_date_review and f_date_review <= next_friday):
				flag=1
				ind.Weights_Share_Freeze_Date_rev = ind.Weights_Share_Freeze_Date_rev + freeze_date_review + "\n"
			if(next_monday <= s_date_review and s_date_review <= next_friday):
				flag=1
				ind.Selection_Date_Cycle_2_rev = ind.Selection_Date_Cycle_2_rev + sel_date_review + "\n"
			if(next_monday <= a_date_review and a_date_review <= next_friday):
				flag=1
				ind.Public_Announcement_Date_rev = ind.Public_Announcement_Date_rev + announce_date_review + "\n"
			if(next_monday <= cl_date_review and cl_date_review <= next_friday):
				flag=1
				ind.Client_Comm_Date_rev = ind.Client_Comm_Date_rev + client_comm_date_review + "\n"
			if(next_monday <= p_date_review and p_date_review <= next_friday):
				flag=1
				ind.Prelim_Comm_Date_rev = ind.Prelim_Comm_Date_rev + Prelim_comm_date_review + "\n"
			if(next_monday <= com_date_review and com_date_review <= next_friday):
				flag=1
				ind.Ind_Cmte_Comm_Date_rev = ind.Ind_Cmte_Comm_Date_rev + Committee_comm_date_review + "\n"



		if(flag==1):
			informa.append(ind)
	context = {
				'info' : informa,
	            'client_name' : client_name,}
	'''templateName = "mail.html"
	return render(request, templateName, context)'''

	html_content = render_to_string('mail.html', context) # render with dynamic value
	text_content = strip_tags(html_content)

	body = 'Subject: Email testing'+'\n' + '\nHello, \n\n Email testing for calendar automation\n' + '\nHave a nice day!'
	send_mail(text_content)

