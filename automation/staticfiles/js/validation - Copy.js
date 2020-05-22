/*!
 * Version : 1.0
 * Project: Calendar Automation
 * Copyright : Indxx Capital Management
 * Author: Pavan Rajput
 * Author: 08-04-2019
 * Licensed under : Self
 */
 
 
 $(document).ready(function() {
 
  $('#RegForm').submit(function(e) {
    e.preventDefault();
    var index_name = $('#index_name').val();
	var thomson_id = $('#thomson_id').val();
	var ind_version = $('#ind_version').val();
	
	var cal_agent = $('#cal_agent').val();
	var contract_Type = $('#contract_Type').val();
	var etf_Launched = $('#etf_Launched').val();
	var live_date = $('#live_date').val();
	var isin_id = $('#isin_id').val();
	var client_name = $('#client_name').val();
	var index_version_id = $('#index_version_id').val();
	var data_platform = $('#data_platform').val();
	var type_index = $('#type_index').val();
	var theme_Review = $('#theme_Review').val();
	var backtest_date = $('#backtest_date').val();
	var bloomberg_id = $('#bloomberg_id').val();
	var index_Style = $('#index_Style').val();
	var calculation = $('#calculation').val();
	var data_vendors = $('#data_vendors').val();
	var prod_Status = $('#prod_Status').val();
	var etf_date = $('#etf_date').val();
	
   
 
    $(".error").remove();
 
    if (index_name.length < 1) {
      $('#index_name').after('<br/><span class="error">Index Name is required</span>');
    }
	if (thomson_id.length < 1) {
      $('#thomson_id').after('<br/><span class="error">Thomson Id is required</span>');
    }
	if (ind_version.length < 1) {
      $('#ind_version').after('<br/><span class="error">Index Version is required</span>');
    }
	
	
	
	if (cal_agent.length < 1) {
      $('#cal_agent').after('<br/><span class="error">This field is required</span>');
    }
	if (contract_Type.length < 1) {
      $('#contract_Type').after('<br/><span class="error">This field is required</span>');
    }
	if (etf_Launched.length < 1) {
      $('#etf_Launched').after('<br/><span class="error">This field is required</span>');
    }
	if (live_date.length < 1) {
      $('#live_date').after('<br/><span class="error">This field is required</span>');
    }
	if (isin_id.length < 1) {
      $('#isin_id').after('<br/><span class="error">This field is required</span>');
    }
	if (client_name.length < 1) {
      $('#client_name').after('<br/><span class="error">This field is required</span>');
    }
	if (index_version_id.length < 1) {
      $('#index_version_id').after('<br/><span class="error">This field is required</span>');
    }
	if (data_platform.length < 1) {
      $('#data_platform').after('<br/><span class="error">This field is required</span>');
    }
	if (type_index.length < 1) {
      $('#type_index').after('<br/><span class="error">This field is required</span>');
    }
	if (theme_Review.length < 1) {
      $('#theme_Review').after('<br/><span class="error">This field is required</span>');
    }
	if (backtest_date.length < 1) {
      $('#backtest_date').after('<br/><span class="error">This field is required</span>');
    }
	if (bloomberg_id.length < 1) {
      $('#bloomberg_id').after('<br/><span class="error">This field is required</span>');
    }
	if (index_Style.length < 1) {
      $('#index_Style').after('<br/><span class="error">This field is required</span>');
    }
	if (calculation.length < 1) {
      $('#calculation').after('<br/><span class="error">This field is required</span>');
    }
	if (data_vendors.length < 1) {
      $('#data_vendors').after('<br/><span class="error">This field is required</span>');
    }
	if (prod_Status.length < 1) {
      $('#prod_Status').after('<br/><span class="error">This field is required</span>');
    }
	if (etf_date.length < 1) {
      $('#etf_date').after('<br/><span class="error">This field is required</span>');
    }
	else{
		alert('ff');
		return true;
		
	}
	

  });
 
});




