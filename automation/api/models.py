# api/models.py
"""
 * Version : 1.0
 * Project: Calendar Automation
 * Copyright : Indxx Capital Management
 * Author: Pavan Rajput
 * Created Date: 08-04-2019
 * Modified Date: dd-mm-yyyy
 * Licensed under : Self
"""
from django.db import models
# Create your models here.
class Calendarlist(models.Model):
	"""This class represents the Calendarlist model."""
	id = models.AutoField(primary_key=True)
	category = models.CharField(max_length=100, blank=False)
	code = models.CharField(max_length=50, blank=False)
	description = models.CharField(max_length=500, blank=False)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		"""Return a human readable representation of the model instance."""
		return "{}".format(self.category)


class Registerindex(models.Model):
	"""This class represents the Registerindex model."""
	id = models.AutoField(primary_key=True)
	Ident_ISIN = models.CharField(max_length=255)
	Ident_Bloomberg = models.CharField(max_length=255)
	Ident_Reuters = models.CharField(max_length=255)
	Index_Name = models.CharField(max_length=255)
	Client_Name = models.ForeignKey('Calendarlist', on_delete=models.CASCADE)
	Ind_Sty = models.CharField(max_length=255)
	Ind_Ver = models.CharField(max_length=255)
	Ind_Ver_ID = models.CharField(max_length=255)
	Calc = models.CharField(max_length=255)
	Calc_Agent = models.CharField(max_length=255)
	Data_Platform = models.CharField(max_length=255)
	Data_Vendors = models.CharField(max_length=255)
	Contract_Type = models.CharField(max_length=255)
	Type_of_Ind = models.CharField(max_length=255)
	Product_Status = models.CharField(max_length=255)
	ETF_Launched = models.CharField(max_length=255)
	Reconstitution = models.CharField(max_length=255)
	reconst_month = models.CharField(max_length=255, blank=True)
	Rebalance = models.CharField(max_length=255)
	rebalance_month = models.CharField(max_length=255, blank=True)
	Review = models.CharField(max_length=255)
	review_month = models.CharField(max_length=20, blank=True)
	Theme_Review = models.CharField(max_length=255, null=True, blank=True)
	Comm_to_Calc_Agent = models.CharField(max_length=255, null=True, blank=True)
	Comm_to_Calc_Agent_rebal = models.CharField(max_length=255, null=True, blank=True)
	Comm_to_Calc_Agent_review = models.CharField(max_length=255, null=True, blank=True)
	Selection_Date_Cycle_1 = models.CharField(max_length=255, null=True, blank=True)
	Selection_Date_Cycle_1_rebal = models.CharField(max_length=255, null=True, blank=True)
	Selection_Date_Cycle_1_review = models.CharField(max_length=255, null=True, blank=True)
	Completion_Date = models.CharField(max_length=255, null=True, blank=True)
	Completion_Date_rebal = models.CharField(max_length=255, null=True, blank=True)
	Completion_Date_review = models.CharField(max_length=255, null=True, blank=True)
	Selection_Date_Cycle_2 = models.CharField(max_length=255, null=True, blank=True)
	Selection_Date_Cycle_2_rebal = models.CharField(max_length=255, null=True, blank=True)
	Selection_Date_Cycle_2_review = models.CharField(max_length=255, null=True, blank=True)
	Ind_Cmte_Comm_Date = models.CharField(max_length=255, null=True, blank=True)
	Ind_Cmte_Comm_Date_rebal = models.CharField(max_length=255, null=True, blank=True)
	Ind_Cmte_Comm_Date_review = models.CharField(max_length=255, null=True, blank=True)
	Prelim_Comm_Date = models.CharField(max_length=255, null=True, blank=True)
	Prelim_Comm_Date_rebal = models.CharField(max_length=255, null=True, blank=True)
	Prelim_Comm_Date_review = models.CharField(max_length=255, null=True, blank=True)
	Weights_Share_Freeze_Date = models.CharField(max_length=255, null=True, blank=True)
	Weights_Share_Freeze_Date_rebal = models.CharField(max_length=255, null=True, blank=True)
	QC_Date_rebal = models.CharField(max_length=255, null=True, blank=True)
	QC_Date = models.CharField(max_length=255, null=True, blank=True)
	QC_Date_review = models.CharField(max_length=255, null=True, blank=True)
	Weights_Share_Freeze_Date_review = models.CharField(max_length=255, null=True, blank=True)
	Public_Announcement_Date = models.CharField(max_length=255, null=True, blank=True)
	Public_Announcement_Date_rebal = models.CharField(max_length=255, null=True, blank=True)
	Public_Announcement_Date_review = models.CharField(max_length=255, null=True, blank=True)
	Client_Comm_Date = models.CharField(max_length=255, null=True, blank=True)
	Client_Comm_Date_rebal = models.CharField(max_length=255, null=True, blank=True)
	Client_Comm_Date_review = models.CharField(max_length=255, null=True, blank=True)
	Effective_Date = models.CharField(max_length=255, null=True, blank=True)
	Effective_Date_rebal = models.CharField(max_length=255, null=True, blank=True)
	Effective_Date_review = models.CharField(max_length=255, null=True, blank=True)
	etf_launch_date = models.CharField(max_length=255, null=True, blank=True)
	live_date = models.CharField(max_length=255, null=True, blank=True)
	backtest_comp_date = models.CharField(max_length=255, null=True, blank=True)
	color_code = models.IntegerField()

	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)


	def __str__(self):
		"""Return a human readable representation of the model instance."""
		return "{}".format(self.Index_Name)

		
class Ruleslist(models.Model):
	"""This class represents the Ruleslist model."""
	id = models.AutoField(primary_key=True)
	index = models.ForeignKey('Registerindex', on_delete=models.CASCADE)
	eff_rule = models.CharField(max_length=20, blank=False)
	eff_rule_rebal = models.CharField(max_length=20, blank=False)
	eff_rule_review = models.CharField(max_length=20, blank=False)
	sel_rule1 = models.CharField(max_length=20, blank=False)
	sel_rule1_rebal = models.CharField(max_length=20, blank=False)
	sel_rule1_review = models.CharField(max_length=20, blank=False)
	sel_rule2 = models.CharField(max_length=20, blank=False)
	sel_rule2_rebal = models.CharField(max_length=20, blank=False)
	sel_rule2_review = models.CharField(max_length=20, blank=False)
	announce_rule = models.CharField(max_length=20, blank=False)
	announce_rule_rebal = models.CharField(max_length=20, blank=False)
	announce_rule_review = models.CharField(max_length=20, blank=False)
	prelim_rule = models.CharField(max_length=20, blank=False)
	prelim_rule_rebal = models.CharField(max_length=20, blank=False)
	prelim_rule_review = models.CharField(max_length=20, blank=False)
	clientcomm_rule = models.CharField(max_length=20, blank=False)
	clientcomm_rule_rebal = models.CharField(max_length=20, blank=False)
	clientcomm_rule_review = models.CharField(max_length=20, blank=False)
	indcommittee_rule = models.CharField(max_length=20, blank=False)
	indcommittee_rule_rebal = models.CharField(max_length=20, blank=False)
	indcommittee_rule_review = models.CharField(max_length=20, blank=False)
	freeze_rule = models.CharField(max_length=20, blank=False)
	freeze_rule_rebal = models.CharField(max_length=20, blank=False)
	qc_rule = models.CharField(max_length=20, blank=True)
	qc_rule_review = models.CharField(max_length=20, blank=True)
	qc_rule_rebal = models.CharField(max_length=20, blank=True)
	freeze_rule_review = models.CharField(max_length=20, blank=False)
	comp_rule = models.CharField(max_length=20, blank=False)
	comp_rule_rebal = models.CharField(max_length=20, blank=False)
	comp_rule_review = models.CharField(max_length=20, blank=False)
	comm_cal_rule = models.CharField(max_length=20, blank=False)
	comm_cal_rule_rebal = models.CharField(max_length=20, blank=False)
	comm_cal_rule_review = models.CharField(max_length=20, blank=False)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		"""Return a human readable representation of the model instance."""
		return "{}".format(self.index)	


class Priordays(models.Model):
	"""This class represents the Priordays model."""
	id = models.AutoField(primary_key=True)
	index = models.ForeignKey('Registerindex', on_delete=models.CASCADE)
	sel_cycle_1_day_recon = models.CharField(max_length=20, blank=False)
	comp_cycle_1_day_recon = models.CharField(max_length=20, blank=False)
	sel_cycle_2_day_recon = models.CharField(max_length=20, blank=False)
	prelim_day_recon = models.CharField(max_length=20, blank=False)
	freeze_day_recon = models.CharField(max_length=20, blank=False)
	indcommittee_day_recon = models.CharField(max_length=20, blank=False)
	qc_day_recon = models.CharField(max_length=20, blank=False)
	announce_day_recon = models.CharField(max_length=20, blank=False)
	clientcomm_day_recon = models.CharField(max_length=20, blank=False)
	comm_cal_agent_day_recon = models.CharField(max_length=20, blank=False)
	freeze_day_rebal = models.CharField(max_length=20, blank=False)
	qc_day_rebal = models.CharField(max_length=20, blank=False)
	announce_day_rebal = models.CharField(max_length=20, blank=False)
	clientcomm_day_rebal = models.CharField(max_length=20, blank=False)
	comm_cal_agent_day_rebal = models.CharField(max_length=20, blank=False)
	sel_cycle_2_day_review = models.CharField(max_length=20, blank=False)
	indcommittee_day_review = models.CharField(max_length=20, blank=False)
	qc_day_review = models.CharField(max_length=20, blank=False)
	freeze_day_review = models.CharField(max_length=20, blank=False)
	announce_day_review = models.CharField(max_length=20, blank=False)
	clientcomm_day_review = models.CharField(max_length=20, blank=False)
	comm_cal_agent_day_review = models.CharField(max_length=20, blank=False)
