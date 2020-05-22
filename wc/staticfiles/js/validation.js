/*!
 * Version : 1.0
 * Project: Calendar Automation
 * Copyright : Indxx Capital Management
 * Author: Pavan Rajput
 * Author: 08-04-2019
 * Licensed under : Self
 */
 
 
 // Wait for the DOM to be ready
$(function() {
  // Initialize form validation on the registration form.
  // It has the name attribute "registration"   /^[a-zA-Z, '']+$/ value == value.match(/^[a-zA-Z0-9, '']+$/); 
   $.validator.addMethod("alphanumeric", function(value, element){

        return this.optional(element) ||  value == value.match(/^([a-z])([0-9])+$/);

    }, "<br/>Alphabetic characters only please");
  $("form[name='RegForm']").validate({
    // Specify validation rules
    rules: {
      // The key name on the left side is the name attribute
      // of an input field. Validation rules are defined
      // on the right side
      index_name: "required",
	  /*
	  isin_id: { 
				
				required: true, 
				alphanumeric: true,
				minlength:12,	
				
				
	  },
	  bloomberg_id: { required: true, minlength:10},
	  thomson_id: "required",
	  ind_version: "required",
	  index_version_id: "required",
	  data_platform: "required",
	  data_vendors: "required",
	  */
	  client_name: "required",
	  index_Style: "required",
	  calculation: "required",
	  cal_agent: "required",
	  contract_Type: "required",
      type_index: "required",
	  prod_Status: "required",
	  etf_Launched: "required",
	  theme_Review: "required",
	  etf_date: "required",
	  live_date: "required",
	  backtest_date: "required",
    },
    // Specify validation error messages
    messages: {
      index_name: "<br/>Please enter index name.",
	  /*isin_id: {required: "<br/>Please enter isin id.",
				alphanumeric: "<br/>ISIN should be alpha numeric.",
	  			minlength: "<br/>ISIN should be 12 characters."
				},
	  
	  bloomberg_id: {required: "<br/>Please enter bloomberg id.",
				minlength: "<br/>Bloomberg id should be 10 characters."},
	  thomson_id: "<br/>Please enter thomson id.",
	  ind_version: "<br/>Please select index version.",
	  index_version_id: "<br/>Please enter index version id.",
	  data_platform: "<br/>Please select platform.",
	  data_vendors: "<br/>Please select data vendors.",
	  */
	  client_name: "<br/>Please select client name.",
	  index_Style: "<br/>Please select index style name.",
	  calculation: "<br/>Please select calculation type.",
	  cal_agent: "<br/>Please select calculation agent.",
	  contract_Type: "<br/>Please select contract type.",
	  type_index: "<br/>Please select index type.",
      prod_Status: "<br/>Please select product status.",
	  etf_Launched: "<br/>Please select etf launched.",
	  theme_Review: "<br/>Please select theme review.",
	  etf_date: "<br/>Please select etf date.",
	  live_date: "<br/>Please select live date.",
	  backtest_date: "<br/>Please select backtest date.",
    },
	
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
    submitHandler: function(form) {
      form.submit();
    }
  });
  
  $('#isin_id').keypress(function (e) {
    var regex = new RegExp("^[a-zA-Z0-9]+$");
    var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);
    if (regex.test(str)) {
        return true;
    }

    e.preventDefault();
    return false;
});
   $.validator.addMethod("alphaO", function(value, element, theRegEx){
        return value.match(new RegExp("^" + theRegEx + "$"));

    }, "Alphabetic characters only");
});



