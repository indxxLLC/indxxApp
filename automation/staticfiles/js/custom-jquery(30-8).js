/*!
 * Version : 1.0
 * Project: Calendar Automation
 * Copyright : Indxx Capital Management
 * Author: Pavan Rajput
 * Author: 08-04-2019
 * Licensed under : Self
 */

function showDiv(divId, element)
{ 
    document.getElementById(divId).style.display = element.value == 'Thematic' ? 'block' : 'none';
}

function ISINvalidation(element)
{
	
	if(element.value.length!=12)
	{
		alert('ISIN must have 12 characters.');
		element.value="";
	}
	var ch = element.value.charAt(0);
	var ch1 = element.value.charAt(1);
	if((!((ch >= "A" && ch <= "Z") || (ch >= "a" && ch <= "z"))) || !(((ch1 >= "A" && ch1 <= "Z") || (ch1 >= "a" && ch1 <= "z"))))
	{
		alert('First two letters mush be alphabet.');
		element.value="";
	}
}
function BBGvalidation(element){
	if(element.value.length!=10)
	{
		alert('BBG Ticker must have 10 characters.');
		element.value="";
	}
}

function showEtfDate(lanched_date, prod_Status, element)
{  
    var prod_Status = document.getElementById(prod_Status).value;
	if(element.value == 'No' && prod_Status=='Licensed and Launched' )
	{
		alert('Please select ETF Launched "yes".');
		element.value="";
		
	}
	if(element.value == 'No' && prod_Status=='Launched' )
	{
		alert('Please select ETF Launched "yes".');
		element.value="";

	}
	document.getElementById(lanched_date).style.display = element.value == 'Yes' ? 'block' : 'none';
	
}

function showInput(inputId, element)
{ 
    document.getElementById(inputId).style.display = element.value != '' ? 'none' : 'block';

}
function showCalAgent(divId, element)
{
    document.getElementById(divId).style.display = element.value == 'Others' ? 'block' : 'none';
}
function Priordays(divId, element)
{
    document.getElementById(divId).style.display = element.value == '2' ? 'block' : 'none';

}
function Ann_Priordays(divId, element)
{
document.getElementById(divId).style.display = element.value == '3' ? 'block' : 'none';
}
function Sel2_Priordays(divId, element)
{
document.getElementById(divId).style.display = element.value == '7' ? 'block' : 'none';
}

function Freeze_Priordays(divId, element)
{
document.getElementById(divId).style.display = element.value == '6' ? 'block' : 'none';
}

function datevalidation(inputId,element)
{
  date1 = document.getElementById(inputId);
  if(date1.value=="" && element.value!=""){
   alert("Please enter the from date");
   element.value="";
  }
  if(date1.value > element.value){
   alert("To date can not be less than From date");
   element.value="";
  }
}
function datecheck(inputId,element)
{
  date1 = document.getElementById(inputId);
  if(date1.value < element.value){
   alert("Date should be less than effective date");
   element.value="";
  }
}
function daycheck(element)
{
 if(element.value<1){
  alert("Number of days should be positive");
  element.value="";
 }
}
function Colorchange(x,element)
{
  if(element.value=='2'){
  document.getElementById(x).style.backgroundColor = "#ff3333";
  }
  if(element.value=='3'){
  document.getElementById(x).style.backgroundColor = "#bfff80";
  }
  if(element.value=='1'){
  document.getElementById(x).style.backgroundColor = '';
  }

}
function showTab1()

{


                $("#bottom").removeClass("showDIV");

                $("#bottom1").removeClass("showDIV");

                $("#bottom2").removeClass("showDIV");

                $("#bottom").addClass("none");

                $("#bottom1").addClass("none");

                $("#bottom2").addClass("none");

                $("#top").removeClass("none");

                $("#btns").removeClass("showDIV");

                $("#btns").addClass("none");

                $("#top").addClass("showDIV");

 

}

function showTab2()

{           var check2 = document.getElementById('check2');
            var check3 = document.getElementById('check3');
            var check1 = document.getElementById('check1');
            var flag=0;
            if(check1.checked==false && check2.checked==false && check3.checked==false)
            {
            alert("Please select one of the checkbox");
            flag=1;
             $("#bottom").removeClass("showDIV");

                $("#bottom1").removeClass("showDIV");

                $("#bottom2").removeClass("showDIV");

                $("#bottom").addClass("none");

                $("#bottom1").addClass("none");

                $("#bottom2").addClass("none");

                $("#top").removeClass("none");

                $("#btns").removeClass("showDIV");

                $("#btns").addClass("none");

                $("#top").addClass("showDIV");
            }
            var idx_name = document.getElementById('index_name');
            var cl_name = document.getElementById('client_name');
            var idx_style = document.getElementById('index_Style');
            var cal = document.getElementById('calculation');
            var cal_ag = document.getElementById('cal_agent');
            var con_type = document.getElementById('contract_Type');
            var ty_idx = document.getElementById('type_index');
            var prd_status = document.getElementById('prod_Status');
            var etf = document.getElementById('etf_Launched');
            var the_rev = document.getElementById('theme_Review');
            var lv_date = document.getElementById('live_date');
            var back_date = document.getElementById('backtest_date');
            var etf_date = document.getElementById('lanched_date');
            var et_date = document.getElementById('etf_date');
            var cal_ag_dis = document.getElementById('cal_agent_name');
            var cal_ag_name = document.getElementById('cal_agent_des');
            if(lv_date.value < back_date.value)
            {
              alert("Index Live date can't be less than Backtest date");
              flag=1;
                      $("#bottom").removeClass("showDIV");

                $("#bottom1").removeClass("showDIV");

                $("#bottom2").removeClass("showDIV");

                $("#bottom").addClass("none");

                $("#bottom1").addClass("none");

                $("#bottom2").addClass("none");

                $("#top").removeClass("none");

                $("#btns").removeClass("showDIV");

                $("#btns").addClass("none");

                $("#top").addClass("showDIV");
            }
            if((etf_date.style.display == 'block') && (et_date.value < lv_date.value))
            {
              alert("ETF Launch date can't be less than Index Live date");
              flag=1;
                      $("#bottom").removeClass("showDIV");

                $("#bottom1").removeClass("showDIV");

                $("#bottom2").removeClass("showDIV");

                $("#bottom").addClass("none");

                $("#bottom1").addClass("none");

                $("#bottom2").addClass("none");

                $("#top").removeClass("none");

                $("#btns").removeClass("showDIV");

                $("#btns").addClass("none");

                $("#top").addClass("showDIV");
            }
            if((etf_date.style.display == 'block') && (et_date.value < back_date.value))
            {
              alert("ETF Launch date can't be less than Backtest date");
              flag=1;
                      $("#bottom").removeClass("showDIV");

                $("#bottom1").removeClass("showDIV");

                $("#bottom2").removeClass("showDIV");

                $("#bottom").addClass("none");

                $("#bottom1").addClass("none");

                $("#bottom2").addClass("none");

                $("#top").removeClass("none");

                $("#btns").removeClass("showDIV");

                $("#btns").addClass("none");

                $("#top").addClass("showDIV");
            }
			if((etf.value == "No") && (prd_status.value == 'Licensed and Launched'))
			{
				alert('Please select ETF Launched "yes".');
				flag=1;
			}
			if(element.value == 'No' && prd_status.value=='Launched' )
			{
				alert('Please select ETF Launched "yes".');
				flag=1;

			}
            if ((idx_name != null && idx_name.value == '') || (etf_date.style.display == 'block' && et_date.value == '')
            || (cl_name != null && cl_name.value == '') || (idx_style != null && idx_style.value == '') || (cal_ag_dis.style.display == 'block' && cal_ag_name.value == '')
            || (cal != null && cal.value == '') || (cal_ag != null && cal_ag.value == '') ||(con_type != null && con_type.value == '')
            ||(ty_idx != null && ty_idx.value == '') || (prd_status != null && prd_status.value == '') || (etf != null && etf.value == '')
            ||(the_rev != null && the_rev.value == '') || (back_date != null && back_date.value == '') || (lv_date != null && lv_date.value == '') ) {
                      alert("Please fill all the mandatory fields");
                      flag=1;
                      $("#bottom").removeClass("showDIV");

                $("#bottom1").removeClass("showDIV");

                $("#bottom2").removeClass("showDIV");

                $("#bottom").addClass("none");

                $("#bottom1").addClass("none");

                $("#bottom2").addClass("none");

                $("#top").removeClass("none");

                $("#btns").removeClass("showDIV");

                $("#btns").addClass("none");

                $("#top").addClass("showDIV");
          }
            if(flag==0){
                $("#top").removeClass("showDIV");

                $("#bottom1").removeClass("showDIV");

                $("#bottom2").removeClass("showDIV");

                $("#btns").removeClass("showDIV");

                $("#btns").addClass("none");

                $("#top").addClass("none");

                $("#bottom1").addClass("none");

                $("#bottom2").addClass("none");

                $("#bottom").removeClass("none");

                $("#bottom").addClass("showDIV");
                }

 

               

}

 

function showTab3()
{

	var check1 = document.getElementById('check1');
	var choice1 = document.getElementById('choice1');
	var choice2 = document.getElementById('choice2');
	
	var reconstitution = document.getElementById('dd1');
	var reconst_month = document.getElementById('dd12');
	var cmp_date = document.getElementById('cmp_Date');
	var eff_date = document.getElementById('effective_date');
	var sel_date = document.getElementById('selec_Date_Cyc_2');

	var fre_date = document.getElementById('weights_Share_Freeze');
	//var ind_date = document.getElementById('ind_Comm_Date');
	var ann_date = document.getElementById('public_Announcement');
	var cl_date = document.getElementById('client_Comm');
	var qc_date = document.getElementById('qc_date');
	var com_cal = document.getElementById('comm_to_Calc_Agent');
	var sel_1_display = document.getElementById('Cycle_11');
	var sel_1_date = document.getElementById('selec_Date_Cyc_1');
	var sel_1 = document.getElementById('sel1_prior_days');
	var sel_2 = document.getElementById('sel2_prior_days');
	var cmp = document.getElementById('cmp_prior_days');
	var pre = document.getElementById('pre_prior_days');
	//var icom = document.getElementById('icom_prior_days');
	var fre = document.getElementById('fre_prior_days');
	var qc = document.getElementById('qc_prior_days');
	var ann = document.getElementById('ann_prior_days')
	var cl = document.getElementById('cl_prior_days')
	var cal_ag = document.getElementById('cal_ag_prior_days')
	if(choice1.checked){
	  if (check1.checked ==true){
	  if ((reconstitution!= null && reconstitution.value == '') || (reconst_month!= null && reconst_month.value == '')
	   || (sel_1_display.style.display == 'block' && sel_1_date.value == '') ||(qc_date!= null && qc_date.value == '')
	  ||(cmp_date!= null && cmp_date.value == '') || (eff_date!= null && eff_date.value == '') ||(sel_date!= null && sel_date.value == '')
	  || (fre_date!= null && fre_date.value == '') 
	   ||(ann_date!= null && ann_date.value == '') || (cl_date!= null && cl_date.value == '') || (com_cal!= null && com_cal.value == '')
	   || (qc.style.display == 'block' && qc.value == '')||(ann.style.display == 'block' && ann.value == '') || (cl.style.display == 'block' && cl.value == '') || (cal_ag.style.display == 'block' && cal_ag.value == '')
	  || (fre.style.display == 'block' && fre.value == '') 
	  //|| (icom.style.display == 'block' && icom.value == '')
	   ||(pre.style.display == 'block' && pre.value == '') || (cmp.style.display == 'block' && cmp.value == '') || (sel_1.style.display == 'block' && sel_1.value == '')
	   ||(sel_2.style.display == 'block' && sel_2.value == ''))
	   {
		 alert("Please fill all the fields for reconstitution info");
	   }
	   else{
		$("#top").removeClass("showDIV");

		$("#bottom").removeClass("showDIV");

		$("#bottom2").removeClass("showDIV");

		$("#btns").removeClass("showDIV");

		$("#btns").addClass("none");

		$("#top").addClass("none");

		$("#bottom").addClass("none");

		$("#bottom2").addClass("none");

		$("#bottom1").removeClass("none");

		$("#bottom1").addClass("showDIV");
	   }


	  }
	  else
	  {
		$("#top").removeClass("showDIV");

		$("#bottom").removeClass("showDIV");

		$("#bottom2").removeClass("showDIV");

		$("#btns").removeClass("showDIV");

		$("#btns").addClass("none");

		$("#top").addClass("none");

		$("#bottom").addClass("none");

		$("#bottom2").addClass("none");

		$("#bottom1").removeClass("none");

		$("#bottom1").addClass("showDIV");
		}


	}
	else{
		var cmp_date = document.getElementById('mnl_cmp_Date');
		var eff_date = document.getElementById('mnl_eff_date');
		var sel_date = document.getElementById('mnl_sel2_date');
		var fre_date = document.getElementById('mnl_freeze_date');
		//var ind_date = document.getElementById('mnl_ind_Comm_date');
		var ann_date = document.getElementById('mnl_pb_announce_date');
		var cl_date = document.getElementById('mnl_client_comm_date');
		var qc_date = document.getElementById('mnl_qc_date');
		var com_cal = document.getElementById('mnl_comm_cal_date');
		var sel_1_display = document.getElementById('Cycle_11');
		var sel_1_date = document.getElementById('mnl_sel1_date')

	 if (check1.checked ==true){
		  if ((reconstitution!= null && reconstitution.value == '') || (reconst_month!= null && reconst_month.value == '')
		   || (sel_1_display.style.display == 'block' && sel_1_date.value == '') ||(qc_date!= null && qc_date.value == '')
		  ||(cmp_date!= null && cmp_date.value == '') || (eff_date!= null && eff_date.value == '') ||(sel_date!= null && sel_date.value == '')
		 || (fre_date!= null && fre_date.value == '') 
		   ||(ann_date!= null && ann_date.value == '') || (cl_date!= null && cl_date.value == '') || (com_cal!= null && com_cal.value == ''))
		   {
			 alert("Please fill all the fields for reconstitution info");
		   }
		   else{
			$("#top").removeClass("showDIV");

			$("#bottom").removeClass("showDIV");

			$("#bottom2").removeClass("showDIV");

			$("#btns").removeClass("showDIV");

			$("#btns").addClass("none");

			$("#top").addClass("none");

			$("#bottom").addClass("none");

			$("#bottom2").addClass("none");

			$("#bottom1").removeClass("none");

			$("#bottom1").addClass("showDIV");
		   }


		  }
		  else
		  {
			$("#top").removeClass("showDIV");

			$("#bottom").removeClass("showDIV");

			$("#bottom2").removeClass("showDIV");

			$("#btns").removeClass("showDIV");

			$("#btns").addClass("none");

			$("#top").addClass("none");

			$("#bottom").addClass("none");

			$("#bottom2").addClass("none");

			$("#bottom1").removeClass("none");

			$("#bottom1").addClass("showDIV");
			}
	}
}

function showTab4()
{
            var check1 = document.getElementById('check1');
            var choice1 = document.getElementById('choice1');
            var choice2 = document.getElementById('choice2');
            var reconstitution = document.getElementById('dd1');
            var reconst_month = document.getElementById('dd12');
            var cmp_date = document.getElementById('cmp_Date');
            var eff_date = document.getElementById('effective_date');
            var sel_date = document.getElementById('selec_Date_Cyc_2');
            //var pre_date = document.getElementById('pre_comm_date');
            var fre_date = document.getElementById('weights_Share_Freeze');
            //var ind_date = document.getElementById('ind_Comm_Date');
            var ann_date = document.getElementById('public_Announcement');
            var qc_date = document.getElementById('qc_date');
            var cl_date = document.getElementById('client_Comm');
			var com_cal = document.getElementById('comm_to_Calc_Agent');
			var sel_1_display = document.getElementById('Cycle_11');
            var sel_1_date = document.getElementById('selec_Date_Cyc_1')
            var sel_1 = document.getElementById('sel1_prior_days');
             var sel_2 = document.getElementById('sel2_prior_days');
            var cmp = document.getElementById('cmp_prior_days');
            var pre = document.getElementById('pre_prior_days');
            //var icom = document.getElementById('icom_prior_days');
            var fre = document.getElementById('fre_prior_days');
            var qc = document.getElementById('qc_prior_days');
            var ann = document.getElementById('ann_prior_days')
            var cl = document.getElementById('cl_prior_days')
            var cal_ag = document.getElementById('cal_ag_prior_days')

			var check2 = document.getElementById('check2');
			var rebalance = document.getElementById('dd2');
            var rebalance_month = document.getElementById('dd22');
            var eff_date_rebal = document.getElementById('effective_date_rebal');
            var pre_date_rebal = document.getElementById('qc_Date_rebal');
            var fre_date_rebal = document.getElementById('weights_Share_Freeze_rebal');
            var ann_date_rebal = document.getElementById('public_Announcement_rebal');
            var cl_date_rebal = document.getElementById('client_Comm_rebal');
			var com_cal_rebal = document.getElementById('comm_to_Calc_Agent_rebal');
            var fre_rebal = document.getElementById('fre_prior_days_rebal');
            var qc_rebal = document.getElementById('qc_prior_days_rebal');
            var ann_rebal = document.getElementById('ann_prior_days_rebal')
            var cl_rebal = document.getElementById('cl_prior_days_rebal')
            var cal_ag_rebal = document.getElementById('cal_ag_prior_days_rebal')
			
            
			var flag=0;
			if(choice1.checked){
			if (check1.checked==true){
              if ((reconstitution!= null && reconstitution.value == '') || (reconst_month!= null && reconst_month.value == '')
              || (sel_1_display.style.display == 'block' && sel_1_date.value == '')
              ||(cmp_date!= null && cmp_date.value == '') || (eff_date!= null && eff_date.value == '') ||(sel_date!= null && sel_date.value == '')
              || (fre_date!= null && fre_date.value == '') 
               ||(ann_date!= null && ann_date.value == '') || (cl_date!= null && cl_date.value == '') || (com_cal!= null && com_cal.value == '')
               || (qc.style.display == 'block' && qc.value == '')||(ann.style.display == 'block' && ann.value == '') || (cl.style.display == 'block' && cl.value == '') || (cal_ag.style.display == 'block' && cal_ag.value == '')
              || (fre.style.display == 'block' && fre.value == '') 
			  //|| (icom.style.display == 'block' && icom.value == '')
               ||(pre.style.display == 'block' && pre.value == '') || (cmp.style.display == 'block' && cmp.value == '') || (sel_1.style.display == 'block' && sel_1.value == '')
               ||(sel_2.style.display == 'block' && sel_2.value == ''))
               {
                 alert("Please fill all the fields for reconstitution info");
                 flag=1;
               }
               }
            if (check2.checked==true){
              if ((rebalance!= null && rebalance.value == '') || (rebalance_month!= null && rebalance_month.value == '')
              || (eff_date_rebal!= null && eff_date_rebal.value == '')
              ||(pre_date_rebal!= null && pre_date_rebal.value == '') || (fre_date_rebal!= null && fre_date_rebal.value == '')

               ||(ann_date_rebal!= null && ann_date_rebal.value == '') || (cl_date_rebal!= null && cl_date_rebal.value == '')
                || (com_cal_rebal!= null && com_cal_rebal.value == '')
                || (qc_rebal.style.display == 'block' && qc_rebal.value == '')
				||(ann_rebal.style.display == 'block' && ann_rebal.value == '') 
				|| (cl_rebal.style.display == 'block' && cl_rebal.value == '') ||
                (cal_ag_rebal.style.display == 'block' && cal_ag_rebal.value == '')
              || (fre_rebal.style.display == 'block' && fre_rebal.value == ''))
               {
                 alert("Please fill all the fields for rebalancing info");
                 flag=1;
               }
               }
			   
			 
			   }
            else{
            var cmp_date = document.getElementById('mnl_cmp_Date');
            var eff_date = document.getElementById('mnl_eff_date');
            var sel_date = document.getElementById('mnl_sel2_date');
            //var pre_date = document.getElementById('mnl_prelim_date');
            var fre_date = document.getElementById('mnl_freeze_date');
            //var ind_date = document.getElementById('mnl_ind_Comm_date');
            var ann_date = document.getElementById('mnl_pb_announce_date');
            var cl_date = document.getElementById('mnl_client_comm_date');
            var qc_date = document.getElementById('mnl_qc_date');
			var com_cal = document.getElementById('mnl_comm_cal_date');
			var sel_1_display = document.getElementById('Cycle_11');
            var sel_1_date = document.getElementById('mnl_sel1_date')
            var eff_date_rebal = document.getElementById('mnl_eff_date_rebal');
            var pre_date_rebal = document.getElementById('mnl_qc_date_rebal');
            var fre_date_rebal = document.getElementById('mnl_freeze_date_rebal');
            var ann_date_rebal = document.getElementById('mnl_pb_announce_date_rebal');
            var cl_date_rebal = document.getElementById('mnl_client_comm_date_rebal');
			var com_cal_rebal = document.getElementById('mnl_comm_cal_date_rebal');
			
             
			 if (check1.checked==true){
              if ((reconstitution!= null && reconstitution.value == '') || (reconst_month!= null && reconst_month.value == '')
              || (sel_1_display.style.display == 'block' && sel_1_date.value == '')
              ||(cmp_date!= null && cmp_date.value == '') || (eff_date!= null && eff_date.value == '') ||(sel_date!= null && sel_date.value == '')
              || (fre_date!= null && fre_date.value == '') 
               ||(ann_date!= null && ann_date.value == '') || (cl_date!= null && cl_date.value == '') || (com_cal!= null && com_cal.value == ''))
               {
                 alert("Please fill all the fields for reconstitution info");
                 flag=1;
               }
               }
            if (check2.checked==true){
              if ((rebalance!= null && rebalance.value == '') || (rebalance_month!= null && rebalance_month.value == '')
              || (eff_date_rebal!= null && eff_date_rebal.value == '')
              ||(pre_date_rebal!= null && pre_date_rebal.value == '') || (fre_date_rebal!= null && fre_date_rebal.value == '')

               ||(ann_date_rebal!= null && ann_date_rebal.value == '') || (cl_date_rebal!= null && cl_date_rebal.value == '')
                || (com_cal_rebal!= null && com_cal_rebal.value == ''))
               {
                 alert("Please fill all the fields for rebalancing info");
                 flag=1;
               }
               }
			 
               }
            if(flag==0){
                $("#top").removeClass("showDIV");

                $("#bottom").removeClass("showDIV");

                $("#bottom1").removeClass("showDIV");

                $("#btns").removeClass("none");

                $("#btns").addClass("showDIV");

                $("#top").addClass("none");

                $("#bottom").addClass("none")

                $("#bottom1").addClass("none");

                $("#bottom2").removeClass("none");

                $("#bottom2").addClass("showDIV");
                }


}

function showTab5()
{
            var check1 = document.getElementById('check1');
            var choice1 = document.getElementById('choice1');
            var choice2 = document.getElementById('choice2');
            var reconstitution = document.getElementById('dd1');
            var reconst_month = document.getElementById('dd12');
            var cmp_date = document.getElementById('cmp_Date');
            var eff_date = document.getElementById('effective_date');
            var sel_date = document.getElementById('selec_Date_Cyc_2');
            //var pre_date = document.getElementById('pre_comm_date');
            var fre_date = document.getElementById('weights_Share_Freeze');
            //var ind_date = document.getElementById('ind_Comm_Date');
            var ann_date = document.getElementById('public_Announcement');
            var qc_date = document.getElementById('qc_date');
            var cl_date = document.getElementById('client_Comm');
			var com_cal = document.getElementById('comm_to_Calc_Agent');
			var sel_1_display = document.getElementById('Cycle_11');
            var sel_1_date = document.getElementById('selec_Date_Cyc_1')
            var sel_1 = document.getElementById('sel1_prior_days');
             var sel_2 = document.getElementById('sel2_prior_days');
            var cmp = document.getElementById('cmp_prior_days');
            var pre = document.getElementById('pre_prior_days');
            //var icom = document.getElementById('icom_prior_days');
            var fre = document.getElementById('fre_prior_days');
            var qc = document.getElementById('qc_prior_days');
            var ann = document.getElementById('ann_prior_days')
            var cl = document.getElementById('cl_prior_days')
            var cal_ag = document.getElementById('cal_ag_prior_days')

			var check2 = document.getElementById('check2');
			var rebalance = document.getElementById('dd2');
            var rebalance_month = document.getElementById('dd22');
            var eff_date_rebal = document.getElementById('effective_date_rebal');
            var pre_date_rebal = document.getElementById('qc_Date_rebal');
            var fre_date_rebal = document.getElementById('weights_Share_Freeze_rebal');
            var ann_date_rebal = document.getElementById('public_Announcement_rebal');
            var cl_date_rebal = document.getElementById('client_Comm_rebal');
			var com_cal_rebal = document.getElementById('comm_to_Calc_Agent_rebal');
            var fre_rebal = document.getElementById('fre_prior_days_rebal');
            var qc_rebal = document.getElementById('qc_prior_days_rebal');
            var ann_rebal = document.getElementById('ann_prior_days_rebal')
            var cl_rebal = document.getElementById('cl_prior_days_rebal')
            var cal_ag_rebal = document.getElementById('cal_ag_prior_days_rebal')
			
			
			var check3 = document.getElementById('check3');
			var review = document.getElementById('dd3');
            var review_month = document.getElementById('dd32');
            var eff_date_review = document.getElementById('effective_date_review');
            var sel_date_cycl2_review = document.getElementById('selec_Date_Cyc_2_review');
			var fre_review = document.getElementById('weights_Share_Freeze_review');
			var qc_review = document.getElementById('ind_qc_date_review');
			var ann_review = document.getElementById('public_Announcement_review');
            var client_comm_review = document.getElementById('client_Comm_review');
			var com_cal_ag_review = document.getElementById('comm_to_Calc_Agent_review');
            
            
			var flag=0;
			if(choice1.checked){
			if (check1.checked==true){
              if ((reconstitution!= null && reconstitution.value == '') || (reconst_month!= null && reconst_month.value == '')
              || (sel_1_display.style.display == 'block' && sel_1_date.value == '')
              ||(cmp_date!= null && cmp_date.value == '') || (eff_date!= null && eff_date.value == '') ||(sel_date!= null && sel_date.value == '')
              || (fre_date!= null && fre_date.value == '') 
               ||(ann_date!= null && ann_date.value == '') || (cl_date!= null && cl_date.value == '') || (com_cal!= null && com_cal.value == '')
               || (qc.style.display == 'block' && qc.value == '')||(ann.style.display == 'block' && ann.value == '') || (cl.style.display == 'block' && cl.value == '') || (cal_ag.style.display == 'block' && cal_ag.value == '')
              || (fre.style.display == 'block' && fre.value == '') 
			  //|| (icom.style.display == 'block' && icom.value == '')
               ||(pre.style.display == 'block' && pre.value == '') || (cmp.style.display == 'block' && cmp.value == '') || (sel_1.style.display == 'block' && sel_1.value == '')
               ||(sel_2.style.display == 'block' && sel_2.value == ''))
               {
                 alert("Please fill all the fields for reconstitution info");
                 flag=1;
               }
               }
            if (check2.checked==true){
              if ((rebalance!= null && rebalance.value == '') || (rebalance_month!= null && rebalance_month.value == '')
              || (eff_date_rebal!= null && eff_date_rebal.value == '')
              ||(pre_date_rebal!= null && pre_date_rebal.value == '') || (fre_date_rebal!= null && fre_date_rebal.value == '')

               ||(ann_date_rebal!= null && ann_date_rebal.value == '') || (cl_date_rebal!= null && cl_date_rebal.value == '')
                || (com_cal_rebal!= null && com_cal_rebal.value == '')
                || (qc_rebal.style.display == 'block' && qc_rebal.value == '')
				||(ann_rebal.style.display == 'block' && ann_rebal.value == '') 
				|| (cl_rebal.style.display == 'block' && cl_rebal.value == '') ||
                (cal_ag_rebal.style.display == 'block' && cal_ag_rebal.value == '')
              || (fre_rebal.style.display == 'block' && fre_rebal.value == ''))
               {
                 alert("Please fill all the fields for rebalancing info");
                 flag=1;
               }
               }
			   
			  
			  if (check3.checked==true){
              if ((review!= null && review.value == '') || (review_month!= null && review_month.value == '')
              || (eff_date_review!= null && eff_date_review.value == '')
              ||(sel_date_cycl2_review!= null && sel_date_cycl2_review.value == '') || (fre_review!= null && fre_review.value == '')

               ||(qc_review!= null && qc_review.value == '') || (ann_review!= null && ann_review.value == '')
                || (client_comm_review!= null && client_comm_review.value == '') || (com_cal_ag_review!= null && com_cal_ag_review.value == '')
                )
               {
                 alert("Please fill all the fields for review info");
                 flag=1;
               }
               }
			   
			   }
            else{
				var cmp_date = document.getElementById('mnl_cmp_Date');
				var eff_date = document.getElementById('mnl_eff_date');
				var sel_date = document.getElementById('mnl_sel2_date');
				//var pre_date = document.getElementById('mnl_prelim_date');
				var fre_date = document.getElementById('mnl_freeze_date');
				//var ind_date = document.getElementById('mnl_ind_Comm_date');
				var ann_date = document.getElementById('mnl_pb_announce_date');
				var cl_date = document.getElementById('mnl_client_comm_date');
				var qc_date = document.getElementById('mnl_qc_date');
				var com_cal = document.getElementById('mnl_comm_cal_date');
				var sel_1_display = document.getElementById('Cycle_11');
				var sel_1_date = document.getElementById('mnl_sel1_date')
				var eff_date_rebal = document.getElementById('mnl_eff_date_rebal');
				var pre_date_rebal = document.getElementById('mnl_qc_date_rebal');
				var fre_date_rebal = document.getElementById('mnl_freeze_date_rebal');
				var ann_date_rebal = document.getElementById('mnl_pb_announce_date_rebal');
				var cl_date_rebal = document.getElementById('mnl_client_comm_date_rebal');
				var com_cal_rebal = document.getElementById('mnl_comm_cal_date_rebal');
				
				var eff_date_review = document.getElementById('mnl_eff_date_review');
				var sel2_date_review = document.getElementById('mnl_sel2_date_review');
				//var ind_Comm_date_review = document.getElementById('mnl_ind_Comm_date_review');
				var qc_date_review = document.getElementById('mnl_qc_date_review');
				var fre_date_review = document.getElementById('mnl_freeze_date_review');
				var ann_date_review = document.getElementById('mnl_pb_announce_date_review');
				var cl_com_date_review = document.getElementById('mnl_client_comm_date_review');
				var com_cal_date_review = document.getElementById('mnl_comm_cal_date_review');
				
             
			 if (check1.checked==true){
              if ((reconstitution!= null && reconstitution.value == '') || (reconst_month!= null && reconst_month.value == '')
              || (sel_1_display.style.display == 'block' && sel_1_date.value == '')
              ||(cmp_date!= null && cmp_date.value == '') || (eff_date!= null && eff_date.value == '') ||(sel_date!= null && sel_date.value == '')
              || (fre_date!= null && fre_date.value == '') 
               ||(ann_date!= null && ann_date.value == '') || (cl_date!= null && cl_date.value == '') || (com_cal!= null && com_cal.value == ''))
               {
                 alert("Please fill all the fields for reconstitution info");
                 flag=1;
               }
               }
            if (check2.checked==true){
              if ((rebalance!= null && rebalance.value == '') || (rebalance_month!= null && rebalance_month.value == '')
              || (eff_date_rebal!= null && eff_date_rebal.value == '')
              ||(pre_date_rebal!= null && pre_date_rebal.value == '') || (fre_date_rebal!= null && fre_date_rebal.value == '')
               ||(ann_date_rebal!= null && ann_date_rebal.value == '') || (cl_date_rebal!= null && cl_date_rebal.value == '')
                || (com_cal_rebal!= null && com_cal_rebal.value == ''))
               {
                 alert("Please fill all the fields for rebalancing info");
                 flag=1;
               }
               }
			  
			  if (check3.checked==true){
              if ((review!= null && review.value == '') || (review_month!= null && review_month.value == '')
              || (eff_date_review!= null && eff_date_review.value == '')
              ||(sel2_date_review!= null && sel2_date_review.value == '') 
			  //|| (ind_Comm_date_review!= null && ind_Comm_date_review.value == '')
               ||(qc_date_review!= null && qc_date_review.value == '') || (fre_date_review!= null && fre_date_review.value == '')
                || (ann_date_review!= null && ann_date_review.value == '') || (cl_com_date_review!= null && cl_com_date_review.value == '')
				|| (com_cal_date_review!= null && com_cal_date_review.value == ''))
               {
                 alert("Please fill all the fields for review info");
                 flag=1;
               }
               }
			   
               }
			   if(flag==0){
				   document.getElementById("RegForm").submit();
			   }
            


}
function showRules()
{
	$("#selec_Date_Cyc_1").removeClass("none");
	$("#selec_Date_Cyc_1").addClass("showDIV");

	//Make sure showDates is not visible
	$("#mnl_sel1_date").removeClass("showDIV");
	$("#mnl_sel1_date").addClass("none");
	/*
	$('#dd1').css("float", "left");
	$('#dd2').css("float", "left");
	$('#dd3').css("float", "left");
	
	$("#dd12").removeClass("none");
	$("#dd12").addClass("showDIV");
	$('#dd12').css("float", "left");
	
	$("#dd22").removeClass("none");
	$("#dd22").addClass("showDIV");
	$('#dd22').css("float", "left");
	
	$("#dd32").removeClass("none");
	$("#dd32").addClass("showDIV");
	$('#dd32').css("float", "left");
	*/
	$("#cmp_Date").removeClass("none");
	$("#cmp_Date").addClass("showDIV");

    $('#cmp_prior_days').removeClass("none");
    $('#cmp_prior_days').addClass("showDIV");

	$("#mnl_cmp_date").removeClass("showDIV");
	$("#mnl_cmp_date").addClass("none");

	$("#qc_date").removeClass("none");
	$("#qc_date").addClass("showDIV");

	$("#mnl_qc_date").removeClass("showDIV");
	$("#mnl_qc_date").addClass("none");

	$("#effective_date").removeClass("none");
	$("#effective_date").addClass("showDIV");

	$("#mnl_eff_date").removeClass("showDIV");
	$("#mnl_eff_date").addClass("none");


	$("#selec_Date_Cyc_2").removeClass("none");
	$("#selec_Date_Cyc_2").addClass("showDIV");

	$("#mnl_sel2_date").removeClass("showDIV");
	$("#mnl_sel2_date").addClass("none");

	$("#ind_Comm_Date").removeClass("none");
	$("#ind_Comm_Date").addClass("showDIV");

	//$("#mnl_ind_Comm_date").removeClass("showDIV");
	//$("#mnl_ind_Comm_date").addClass("none");

	$("#pre_comm_date").removeClass("none");
	$("#pre_comm_date").addClass("showDIV");

	$("#mnl_prelim_date").removeClass("showDIV");
	$("#mnl_prelim_date").addClass("none");

	$("#weights_Share_Freeze").removeClass("none");
	$("#weights_Share_Freeze").addClass("showDIV");

	$("#mnl_freeze_date").removeClass("showDIV");
	$("#mnl_freeze_date").addClass("none");

	$("#public_Announcement").removeClass("none");
	$("#public_Announcement").addClass("showDIV");

	$("#mnl_pb_announce_date").removeClass("showDIV");
	$("#mnl_pb_announce_date").addClass("none");

	$("#client_Comm").removeClass("none");
	$("#client_Comm").addClass("showDIV");

	$("#mnl_client_comm_date").removeClass("showDIV");
	$("#mnl_client_comm_date").addClass("none");

	$("#comm_to_Calc_Agent").removeClass("none");
	$("#comm_to_Calc_Agent").addClass("showDIV");

	$("#mnl_comm_cal_date").removeClass("showDIV");
	$("#mnl_comm_cal_date").addClass("none");

	$("#selec_Date_Cyc_1_rebal").removeClass("none");
	$("#selec_Date_Cyc_1_rebal").addClass("showDIV");

	$("#mnl_sel1_date_rebal").removeClass("showDIV");
	$("#mnl_sel1_date_rebal").addClass("none");
	
	$("#cmp_Date_rebal").removeClass("none");
	$("#cmp_Date_rebal").addClass("showDIV");

	$("#mnl_cmp_date_rebal").removeClass("showDIV");
	$("#mnl_cmp_date_rebal").addClass("none");

	$("#qc_Date_rebal").removeClass("none");
	$("#qc_Date_rebal").addClass("showDIV");

	$("#mnl_qc_date_rebal").removeClass("showDIV");
	$("#mnl_qc_date_rebal").addClass("none");

	$("#effective_date_rebal").removeClass("none");
	$("#effective_date_rebal").addClass("showDIV");

	$("#mnl_eff_date_rebal").removeClass("showDIV");
	$("#mnl_eff_date_rebal").addClass("none");

	$("#selec_Date_Cyc_2_rebal").removeClass("none");
	$("#selec_Date_Cyc_2_rebal").addClass("showDIV");

	$("#mnl_sel2_date_rebal").removeClass("showDIV");
	$("#mnl_sel2_date_rebal").addClass("none");

	$("#ind_Comm_Date_rebal").removeClass("none");
	$("#ind_Comm_Date_rebal").addClass("showDIV");

	$("#mnl_ind_Comm_date_rebal").removeClass("showDIV");
	$("#mnl_ind_Comm_date_rebal").addClass("none");

	$("#pre_comm_date_rebal").removeClass("none");
	$("#pre_comm_date_rebal").addClass("showDIV");

	$("#mnl_prelim_date_rebal").removeClass("showDIV");
	$("#mnl_prelim_date_rebal").addClass("none");

	$("#weights_Share_Freeze_rebal").removeClass("none");
	$("#weights_Share_Freeze_rebal").addClass("showDIV");

	$("#mnl_freeze_date_rebal").removeClass("showDIV");
	$("#mnl_freeze_date_rebal").addClass("none");

	$("#public_Announcement_rebal").removeClass("none");
	$("#public_Announcement_rebal").addClass("showDIV");

	$("#mnl_pb_announce_date_rebal").removeClass("showDIV");
	$("#mnl_pb_announce_date_rebal").addClass("none");

	$("#client_Comm_rebal").removeClass("none");
	$("#client_Comm_rebal").addClass("showDIV");

	$("#mnl_client_comm_date_rebal").removeClass("showDIV");
	$("#mnl_client_comm_date_rebal").addClass("none");

	$("#comm_to_Calc_Agent_rebal").removeClass("none");
	$("#comm_to_Calc_Agent_rebal").addClass("showDIV");

	$("#mnl_comm_cal_date_rebal").removeClass("showDIV");
	$("#mnl_comm_cal_date_rebal").addClass("none");

	$("#selec_Date_Cyc_1_review").removeClass("none");
	$("#selec_Date_Cyc_1_review").addClass("showDIV");

	$("#mnl_sel1_date_review").removeClass("showDIV");
	$("#mnl_sel1_date_review").addClass("none");

	$("#cmp_Date_review").removeClass("none");
	$("#cmp_Date_review").addClass("showDIV");

	$("#mnl_cmp_date_review").removeClass("showDIV");
	$("#mnl_cmp_date_review").addClass("none");

	$("#ind_qc_date_review").removeClass("none");
	$("#ind_qc_date_review").addClass("showDIV");

	$("#mnl_qc_date_review").removeClass("showDIV");
	$("#mnl_qc_date_review").addClass("none");

	$("#effective_date_review").removeClass("none");
	$("#effective_date_review").addClass("showDIV");

	$("#mnl_eff_date_review").removeClass("showDIV");
	$("#mnl_eff_date_review").addClass("none");

	$("#selec_Date_Cyc_2_review").removeClass("none");
	$("#selec_Date_Cyc_2_review").addClass("showDIV");

	$("#mnl_sel2_date_review").removeClass("showDIV");
	$("#mnl_sel2_date_review").addClass("none");

	$("#ind_Comm_Date_review").removeClass("none");
	$("#ind_Comm_Date_review").addClass("showDIV");
	/*
	$("#mnl_ind_Comm_date_review").removeClass("showDIV");
	$("#mnl_ind_Comm_date_review").addClass("none");
	*/
	$("#pre_comm_date_review").removeClass("none");
	$("#pre_comm_date_review").addClass("showDIV");

	$("#mnl_prelim_date_review").removeClass("showDIV");
	$("#mnl_prelim_date_review").addClass("none");

	$("#weights_Share_Freeze_review").removeClass("none");
	$("#weights_Share_Freeze_review").addClass("showDIV");

	$("#mnl_freeze_date_review").removeClass("showDIV");
	$("#mnl_freeze_date_review").addClass("none");

	$("#public_Announcement_review").removeClass("none");
	$("#public_Announcement_review").addClass("showDIV");

	$("#mnl_pb_announce_date_review").removeClass("showDIV");
	$("#mnl_pb_announce_date_review").addClass("none");

	$("#client_Comm_review").removeClass("none");
	$("#client_Comm_review").addClass("showDIV");

	$("#mnl_client_comm_date_review").removeClass("showDIV");
	$("#mnl_client_comm_date_review").addClass("none");

	$("#comm_to_Calc_Agent_review").removeClass("none");
	$("#comm_to_Calc_Agent_review").addClass("showDIV");

	$("#mnl_comm_cal_date_review").removeClass("showDIV");
	$("#mnl_comm_cal_date_review").addClass("none");

	$('#fre_prior_days_rebal').removeClass("none");
    $('#fre_prior_days_rebal').addClass("showDIV");

    $('#qc_prior_days_rebal').removeClass("none");
    $('#qc_prior_days_rebal').addClass("showDIV");

    $('#ann_prior_days_rebal').removeClass("none");
    $('#ann_prior_days_rebal').addClass("showDIV");

    $('#cl_prior_days_rebal').removeClass("none");
    $('#cl_prior_days_rebal').addClass("showDIV");

    $('#cal_ag_prior_days_rebal').removeClass("none");
    $('#cal_ag_prior_days_rebal').addClass("showDIV");

    //$('#cmp_prior_days').removeClass("none");
    //$('#cmp_prior_days').addClass("showDIV");

    //$('#sel1_prior_days').removeClass("none");
    //$('#sel1_prior_days').addClass("showDIV");

    //$('#sel2_prior_days').removeClass("none");
    //$('#sel2_prior_days').addClass("showDIV");

    //$('#icom_prior_days').removeClass("none");
    //$('#icom_prior_days').addClass("showDIV");

    //$('#qc_prior_days').removeClass("none");
    //$('#qc_prior_days').addClass("showDIV");

    //$('#pre_prior_days').removeClass("none");
    //$('#pre_prior_days').addClass("showDIV");

    //$('#fre_prior_days').removeClass("none");
    //$('#fre_prior_days').addClass("showDIV");

    //$('#ann_prior_days').removeClass("none");
    //$('#ann_prior_days').addClass("showDIV");

    //$('#cl_prior_days').removeClass("none");
    //$('#cl_prior_days').addClass("showDIV");

    //$('#cal_ag_prior_days').removeClass("none");
    //$('#cal_ag_prior_days').addClass("showDIV");

    //$('#sel2_prior_days_review').removeClass("none");
    //$('#sel2_prior_days_review').addClass("showDIV");

    //$('#icom_prior_days_review').removeClass("none");
    //$('#icom_prior_days_review').addClass("showDIV");

    //$('#qc_prior_days_review').removeClass("none");
    //$('#qc_prior_days_review').addClass("showDIV");

    //$('#fre_prior_days_review').removeClass("none");
    //$('#fre_prior_days_review').addClass("showDIV");

    //$('#ann_prior_days_review').removeClass("none");
    //$('#ann_prior_days_review').addClass("showDIV");

    //$('#cl_prior_days_review').removeClass("none");
    //$('#cl_prior_days_review').addClass("showDIV");

    //$('#cal_ag_prior_days_review').removeClass("none");
    //$('#cal_ag_prior_days_review').addClass("showDIV");
	// 16-08-2019
	
	if(document.getElementById('selec_Date_Cyc_1').value == 2){
		$("#sel1_prior_days").removeClass("none");
		$("#sel1_prior_days").addClass("showDIV");
		$('#sel1_prior_days').css("display", "block");
	}
	else{
		$("#sel1_prior_days").removeClass("showDIV");
		$("#sel1_prior_days").addClass("none");
	}
	
	
	if(document.getElementById('cmp_Date').value == 2){
		$("#cmp_prior_days").removeClass("none");
		$("#cmp_prior_days").addClass("showDIV");
		$('#cmp_prior_days').css("display", "block");
	}
	else{
		$("#cmp_prior_days").removeClass("showDIV");
		$("#cmp_prior_days").addClass("none");
	}
	
	if(document.getElementById('selec_Date_Cyc_2').value == 7){
		$("#sel2_prior_days").removeClass("none");
		$("#sel2_prior_days").addClass("showDIV");
		$('#sel2_prior_days').css("display", "block");
	}
	else{
		$("#sel2_prior_days").removeClass("showDIV");
		$("#sel2_prior_days").addClass("none");
	}
	
	if(document.getElementById('ind_Comm_Date').value == 3){
		$("#icom_prior_days").removeClass("none");
		$("#icom_prior_days").addClass("showDIV");
		$('#icom_prior_days').css("display", "block");
	}
	else{
		$("#icom_prior_days").removeClass("showDIV");
		$("#icom_prior_days").addClass("none");
	}
	
	if(document.getElementById('qc_date').value == 3){
		$("#qc_prior_days").removeClass("none");
		$("#qc_prior_days").addClass("showDIV");
		$('#qc_prior_days').css("display", "block");
	}
	else{
		$("#qc_prior_days").removeClass("showDIV");
		$("#qc_prior_days").addClass("none");
	}
	
	if(document.getElementById('pre_comm_date').value == 2){
		$("#pre_prior_days").removeClass("none");
		$("#pre_prior_days").addClass("showDIV");
		$('#pre_prior_days').css("display", "block");
	}
	else{
		$("#pre_prior_days").removeClass("showDIV");
		$("#pre_prior_days").addClass("none");
	}
	
	if(document.getElementById('weights_Share_Freeze').value == 6){
		$("#fre_prior_days").removeClass("none");
		$("#fre_prior_days").addClass("showDIV");
		$('#fre_prior_days').css("display", "block");
	}
	else{
		$("#fre_prior_days").removeClass("showDIV");
		$("#fre_prior_days").addClass("none");
	}
	
	if(document.getElementById('public_Announcement').value == 3){
		$("#ann_prior_days").removeClass("none");
		$("#ann_prior_days").addClass("showDIV");
		$('#ann_prior_days').css("display", "block");
	}
	else{
		$("#ann_prior_days").removeClass("showDIV");
		$("#ann_prior_days").addClass("none");
	}
	
	if(document.getElementById('client_Comm').value == 3){
		$("#cl_prior_days").removeClass("none");
		$("#cl_prior_days").addClass("showDIV");
		$('#cl_prior_days').css("display", "block");
	}
	else{
		$("#cl_prior_days").removeClass("showDIV");
		$("#cl_prior_days").addClass("none");
	}
	
	if(document.getElementById('comm_to_Calc_Agent').value == 2){
		$("#cal_ag_prior_days").removeClass("none");
		$("#cal_ag_prior_days").addClass("showDIV");
		$('#cal_ag_prior_days').css("display", "block");
	}
	else{
		$("#cal_ag_prior_days").removeClass("showDIV");
		$("#cal_ag_prior_days").addClass("none");
	}
	

	//Rebal
	if(document.getElementById('weights_Share_Freeze_rebal').value == 6){
		$("#fre_prior_days_rebal").removeClass("none");
		$("#fre_prior_days_rebal").addClass("showDIV");
		$('#fre_prior_days_rebal').css("display", "block");
	}
	else{
		$("#fre_prior_days_rebal").removeClass("showDIV");
		$("#fre_prior_days_rebal").addClass("none");
	}
	
	if(document.getElementById('qc_Date_rebal').value == 3){
		$("#qc_prior_days_rebal").removeClass("none");
		$("#qc_prior_days_rebal").addClass("showDIV");
		$('#qc_prior_days_rebal').css("display", "block");
	}
	else{
		$("#qc_prior_days_rebal").removeClass("showDIV");
		$("#qc_prior_days_rebal").addClass("none");
	}
	
	if(document.getElementById('public_Announcement_rebal').value == 3){
		$("#ann_prior_days_rebal").removeClass("none");
		$("#ann_prior_days_rebal").addClass("showDIV");
		$('#ann_prior_days_rebal').css("display", "block");
	}
	else{
		$("#ann_prior_days_rebal").removeClass("showDIV");
		$("#ann_prior_days_rebal").addClass("none");
	}
	
	if(document.getElementById('client_Comm_rebal').value == 3){
		$("#cl_prior_days_rebal").removeClass("none");
		$("#cl_prior_days_rebal").addClass("showDIV");
		$('#cl_prior_days_rebal').css("display", "block");
	}
	else{
		$("#cl_prior_days_rebal").removeClass("showDIV");
		$("#cl_prior_days_rebal").addClass("none");
	}
	
	if(document.getElementById('comm_to_Calc_Agent_rebal').value == 2){
		$("#cal_ag_prior_days_rebal").removeClass("none");
		$("#cal_ag_prior_days_rebal").addClass("showDIV");
		$('#cal_ag_prior_days_rebal').css("display", "block");
	}
	else{
		$("#cal_ag_prior_days_rebal").removeClass("showDIV");
		$("#cal_ag_prior_days_rebal").addClass("none");
	}
	
	//Review
	if(document.getElementById('selec_Date_Cyc_2_review').value == 7){
		$("#sel2_prior_days_review").removeClass("none");
		$("#sel2_prior_days_review").addClass("showDIV");
		$('#sel2_prior_days_review').css("display", "block");
	}else{
		$("#sel2_prior_days_review").removeClass("showDIV");
		$("#sel2_prior_days_review").addClass("none");
	}
	/*
	if(document.getElementById('ind_Comm_Date_review').value == 3){
		$("#icom_prior_days_review").removeClass("none");
		$("#icom_prior_days_review").addClass("showDIV");
		$('#icom_prior_days_review').css("display", "block");
	}else{
		$("#icom_prior_days_review").removeClass("showDIV");
		$("#icom_prior_days_review").addClass("none");
	}
	*/
	if(document.getElementById('ind_qc_date_review').value == 3){
		$("#qc_prior_days_review").removeClass("none");
		$("#qc_prior_days_review").addClass("showDIV");
		$('#qc_prior_days_review').css("display", "block");
	}else{
		$("#qc_prior_days_review").removeClass("showDIV");
		$("#qc_prior_days_review").addClass("none");
	}
	
	if(document.getElementById('weights_Share_Freeze_review').value == 6){
		$("#fre_prior_days_review").removeClass("none");
		$("#fre_prior_days_review").addClass("showDIV");
		$('#fre_prior_days_review').css("display", "block");
	}else{
		$("#fre_prior_days_review").removeClass("showDIV");
		$("#fre_prior_days_review").addClass("none");
	}
	
	if(document.getElementById('public_Announcement_review').value == 3){
		$("#ann_prior_days_review").removeClass("none");
		$("#ann_prior_days_review").addClass("showDIV");
		$('#ann_prior_days_review').css("display", "block");
	}else{
		$("#ann_prior_days_review").removeClass("showDIV");
		$("#ann_prior_days_review").addClass("none");
	}
	
	if(document.getElementById('client_Comm_review').value == 3){
		$("#cl_prior_days_review").removeClass("none");
		$("#cl_prior_days_review").addClass("showDIV");
		$('#cl_prior_days_review').css("display", "block");
	}else{
		$("#cl_prior_days_review").removeClass("showDIV");
		$("#cl_prior_days_review").addClass("none");
	}
	
	if(document.getElementById('comm_to_Calc_Agent_review').value == 2){
		$("#cal_ag_prior_days_review").removeClass("none");
		$("#cal_ag_prior_days_review").addClass("showDIV");
		$('#cal_ag_prior_days_review').css("display", "block");
	}else{
		$("#cal_ag_prior_days_review").removeClass("showDIV");
		$("#cal_ag_prior_days_review").addClass("none");
		
	}
	
	
	

}

function showDates()
{

	$("#selec_Date_Cyc_1").removeClass("showDIV");
	$("#selec_Date_Cyc_1").addClass("none");
	/*
	$("#dd12").removeClass("showDIV");
	$("#dd12").addClass("none");
	
	$("#dd22").removeClass("showDIV");
	$("#dd22").addClass("none");
	
	$("#dd32").removeClass("showDIV");
	$("#dd32").addClass("none");
	*/
	//Make sure showDates is not visible
	$("#mnl_sel1_date").removeClass("none");
	$("#mnl_sel1_date").addClass("showDIV");

	$('#fre_prior_days_rebal').removeClass("showDIV");
    $('#fre_prior_days_rebal').addClass("none");
	$('#fre_prior_days_rebal').css("display", "none");

    $('#qc_prior_days_rebal').removeClass("showDIV");
    $('#qc_prior_days_rebal').addClass("none");
	$('#qc_prior_days_rebal').css("display", "none");

    $('#ann_prior_days_rebal').removeClass("showDIV");
    $('#ann_prior_days_rebal').addClass("none");
	$('#ann_prior_days_rebal').css("display", "none");

    $('#cl_prior_days_rebal').removeClass("showDIV");
    $('#cl_prior_days_rebal').addClass("none");
	$('#cl_prior_days_rebal').css("display", "none");

    $('#cal_ag_prior_days_rebal').removeClass("showDIV");
    $('#cal_ag_prior_days_rebal').addClass("none");
	$('#cal_ag_prior_days_rebal').css("display", "none");

    $('#cmp_prior_days').removeClass("showDIV");
    $('#cmp_prior_days').addClass("none");
	$('#cmp_prior_days').css("display", "none");

    $('#sel1_prior_days').removeClass("showDIV");
    $('#sel1_prior_days').addClass("none");
	$('#sel1_prior_days').css("display", "none");

    $('#sel2_prior_days').removeClass("showDIV");
    $('#sel2_prior_days').addClass("none");
	$('#sel2_prior_days').css("display", "none");

    $('#icom_prior_days').removeClass("showDIV");
    $('#icom_prior_days').addClass("none");
	$('#icom_prior_days').css("display", "none");

    $('#qc_prior_days').removeClass("showDIV");
    $('#qc_prior_days').addClass("none");
	$('#qc_prior_days').css("display", "none");

    $('#pre_prior_days').removeClass("showDIV");
    $('#pre_prior_days').addClass("none");
	$('#pre_prior_days').css("display", "none");

    $('#fre_prior_days').removeClass("showDIV");
    $('#fre_prior_days').addClass("none");
	$('#fre_prior_days').css("display", "none");

    $('#ann_prior_days').removeClass("showDIV");
    $('#ann_prior_days').addClass("none");
	$('#ann_prior_days').css("display", "none");

    $('#cl_prior_days').removeClass("showDIV");
    $('#cl_prior_days').addClass("none");
	$('#cl_prior_days').css("display", "none");

    $('#cal_ag_prior_days').removeClass("showDIV");
    $('#cal_ag_prior_days').addClass("none");
	$('#cal_ag_prior_days').css("display", "none");

    $('#sel2_prior_days_review').removeClass("showDIV");
    $('#sel2_prior_days_review').addClass("none");
	$('#sel2_prior_days_review').css("display", "none");
	/*
    $('#icom_prior_days_review').removeClass("showDIV");
    $('#icom_prior_days_review').addClass("none");
	$('#icom_prior_days_review').css("display", "none");
	*/
    $('#qc_prior_days_review').removeClass("showDIV");
    $('#qc_prior_days_review').addClass("none");
	$('#qc_prior_days_review').css("display", "none");

    $('#fre_prior_days_review').removeClass("showDIV");
    $('#fre_prior_days_review').addClass("none");
	$('#fre_prior_days_review').css("display", "none");

    $('#ann_prior_days_review').removeClass("showDIV");
    $('#ann_prior_days_review').addClass("none");
	$('#ann_prior_days_review').css("display", "none");

    $('#cl_prior_days_review').removeClass("showDIV");
    $('#cl_prior_days_review').addClass("none");
	$('#cl_prior_days_review').css("display", "none");

    $('#cal_ag_prior_days_review').removeClass("showDIV");
    $('#cal_ag_prior_days_review').addClass("none");
	$('#cal_ag_prior_days_review').css("display", "none");

	$("#cmp_Date").removeClass("showDIV");
	$("#cmp_Date").addClass("none");



	$("#mnl_cmp_date").removeClass("none");
	$("#mnl_cmp_date").addClass("showDIV");

	$("#effective_date").removeClass("showDIV");
	$("#effective_date").addClass("none");

	$("#mnl_eff_date").removeClass("none");
	$("#mnl_eff_date").addClass("showDIV");

    $("#qc_date").removeClass("showDIV");
    $("#qc_date").addClass("none");

    $("#mnl_qc_date").removeClass("none");
    $("#mnl_qc_date").addClass("showDIV");

	$("#selec_Date_Cyc_2").removeClass("showDIV");
	$("#selec_Date_Cyc_2").addClass("none");

	$("#mnl_sel2_date").removeClass("none");
	$("#mnl_sel2_date").addClass("showDIV");

	$("#ind_Comm_Date").removeClass("showDIV");
	$("#ind_Comm_Date").addClass("none");

	//$("#mnl_ind_Comm_date").removeClass("none");
	//$("#mnl_ind_Comm_date").addClass("showDIV");

	$("#pre_comm_date").removeClass("showDIV");
	$("#pre_comm_date").addClass("none");

	$("#mnl_prelim_date").removeClass("none");
	$("#mnl_prelim_date").addClass("showDIV");


	$("#weights_Share_Freeze").removeClass("showDIV");
	$("#weights_Share_Freeze").addClass("none");

	$("#mnl_freeze_date").removeClass("none");
	$("#mnl_freeze_date").addClass("showDIV");

	$("#public_Announcement").removeClass("showDIV");
	$("#public_Announcement").addClass("none");

	$("#mnl_pb_announce_date").removeClass("none");
	$("#mnl_pb_announce_date").addClass("showDIV");

	$("#client_Comm").removeClass("showDIV");
	$("#client_Comm").addClass("none");

	$("#mnl_client_comm_date").removeClass("none");
	$("#mnl_client_comm_date").addClass("showDIV");

	$("#comm_to_Calc_Agent").removeClass("showDIV");
	$("#comm_to_Calc_Agent").addClass("none");

	$("#mnl_comm_cal_date").removeClass("none");
	$("#mnl_comm_cal_date").addClass("showDIV");

	$("#selec_Date_Cyc_1_rebal").removeClass("showDIV");
	$("#selec_Date_Cyc_1_rebal").addClass("none");

	$("#mnl_sel1_date_rebal").removeClass("none");
	$("#mnl_sel1_date_rebal").addClass("showDIV");
	
	$("#cmp_Date_rebal").removeClass("showDIV");
	$("#cmp_Date_rebal").addClass("none");

	$("#mnl_cmp_date_rebal").removeClass("none");
	$("#mnl_cmp_date_rebal").addClass("showDIV");

	$("#effective_date_rebal").removeClass("showDIV");
	$("#effective_date_rebal").addClass("none");

	$("#mnl_eff_date_rebal").removeClass("none");
	$("#mnl_eff_date_rebal").addClass("showDIV");

	$("#selec_Date_Cyc_2_rebal").removeClass("showDIV");
	$("#selec_Date_Cyc_2_rebal").addClass("none");

	$("#mnl_sel2_date_rebal").removeClass("none");
	$("#mnl_sel2_date_rebal").addClass("showDIV");

	$("#qc_Date_rebal").removeClass("showDIV");
	$("#qc_Date_rebal").addClass("none");

	$("#mnl_qc_date_rebal").removeClass("none");
	$("#mnl_qc_date_rebal").addClass("showDIV");

	$("#pre_comm_date_rebal").removeClass("showDIV");
	$("#pre_comm_date_rebal").addClass("none");

	$("#mnl_prelim_date_rebal").removeClass("none");
	$("#mnl_prelim_date_rebal").addClass("showDIV");

	$("#weights_Share_Freeze_rebal").removeClass("showDIV");
	$("#weights_Share_Freeze_rebal").addClass("none");

	$("#mnl_freeze_date_rebal").removeClass("none");
	$("#mnl_freeze_date_rebal").addClass("noneshowDIV");

	$("#public_Announcement_rebal").removeClass("showDIV");
	$("#public_Announcement_rebal").addClass("none");

	$("#mnl_pb_announce_date_rebal").removeClass("none");
	$("#mnl_pb_announce_date_rebal").addClass("showDIV");

	$("#client_Comm_rebal").removeClass("showDIV");
	$("#client_Comm_rebal").addClass("none");

	$("#mnl_client_comm_date_rebal").removeClass("none");
	$("#mnl_client_comm_date_rebal").addClass("showDIV");

	$("#comm_to_Calc_Agent_rebal").removeClass("showDIV");
	$("#comm_to_Calc_Agent_rebal").addClass("none");

	$("#mnl_comm_cal_date_rebal").removeClass("none");
	$("#mnl_comm_cal_date_rebal").addClass("showDIV");

	$("#selec_Date_Cyc_1_review").removeClass("showDIV");
	$("#selec_Date_Cyc_1_review").addClass("none");

	$("#mnl_sel1_date_review").removeClass("none");
	$("#mnl_sel1_date_review").addClass("showDIV");

	$("#cmp_Date_review").removeClass("showDIV");
	$("#cmp_Date_review").addClass("none");

	$("#mnl_cmp_date_review").removeClass("none");
	$("#mnl_cmp_date_review").addClass("showDIV");

	$("#effective_date_review").removeClass("showDIV");
	$("#effective_date_review").addClass("none");

	$("#mnl_eff_date_review").removeClass("none");
	$("#mnl_eff_date_review").addClass("showDIV");

	$("#selec_Date_Cyc_2_review").removeClass("showDIV");
	$("#selec_Date_Cyc_2_review").addClass("none");

	$("#mnl_sel2_date_review").removeClass("none");
	$("#mnl_sel2_date_review").addClass("showDIV");

	$("#ind_Comm_Date_review").removeClass("showDIV");
	$("#ind_Comm_Date_review").addClass("none");
	/*
	$("#mnl_ind_Comm_date_review").removeClass("none");
	$("#mnl_ind_Comm_date_review").addClass("showDIV");
	*/
	$("#pre_comm_date_review").removeClass("showDIV");
	$("#pre_comm_date_review").addClass("none");

	$("#mnl_prelim_date_review").removeClass("none");
	$("#mnl_prelim_date_review").addClass("showDIV");

	$("#weights_Share_Freeze_review").removeClass("showDIV");
	$("#weights_Share_Freeze_review").addClass("none");

	$("#mnl_freeze_date_review").removeClass("none");
	$("#mnl_freeze_date_review").addClass("showDIV");

	$("#public_Announcement_review").removeClass("showDIV");
	$("#public_Announcement_review").addClass("none");

	$("#mnl_pb_announce_date_review").removeClass("none");
	$("#mnl_pb_announce_date_review").addClass("showDIV");

	$("#client_Comm_review").removeClass("showDIV");
	$("#client_Comm_review").addClass("none");

	$("#mnl_client_comm_date_review").removeClass("none");
	$("#mnl_client_comm_date_review").addClass("showDIV");

	$("#ind_qc_date_review").removeClass("showDIV");
	$("#ind_qc_date_review").addClass("none");

	$("#mnl_qc_date_review").removeClass("none");
	$("#mnl_qc_date_review").addClass("showDIV");

	$("#comm_to_Calc_Agent_review").removeClass("showDIV");
	$("#comm_to_Calc_Agent_review").addClass("none");

	$("#mnl_comm_cal_date_review").removeClass("none");
	$("#mnl_comm_cal_date_review").addClass("showDIV");
	
	$("#comCalAgent").removeClass("showDIV");
	$("#comCalAgent").addClass("none");
	
	
}




