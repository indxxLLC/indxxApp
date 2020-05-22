<?php
require_once("header.php");
$messgae = ""; 
$warrning = "";  
$buttonFlag = false;
$_SESSION['totalPages'] 			= 0;
$_SESSION['periodStartPoint'] 		= 0;
$_SESSION['securityISNStartPoint'] 	= 0;
$_SESSION['DateStartPoint'] 		= '';
$_SESSION['currency'] 				= '';
$_SESSION['securities'] 			= '';
$_SESSION['StartDate'] 				= '';
$_SESSION['EndDate'] 				= '';
$_SESSION['spinoff'] 				= '';
$_SESSION['dividend'] 				= '';
$_SESSION['period'] 				= '';	
$_SESSION['SRNO'] 					= 1;       
?>
	<div class="container main-body">
	<?php if(isset($_POST['period']) && isset($_POST['Step0']) ) { ?>
			
		<div class="row">
			<div class="col-lg-12 col-xs-12">
				<ul class="Notice" >
					<li style="font-size:15px;list-style:none; font-weight:bold;">Note : 1. CSV file should be Period , ISIN , and Weight format.</li>
					<li style="font-size:15px;list-style:none; font-weight:bold;">Note : 2. System will treat weight as in % only.</li>					
				</ul>
			</div>
		</div>
		
		<div class="row">
		<div class="col-lg-12 col-xs-12"><ul  id="result" class="Notice" style="color:rgb(202, 75, 75);"></ul></div>
		</div>
		
		
		
		
		<div class="row">
			<form name="frmStep1" id="frmStep1" action="process.php" method="post" enctype="multipart/form-data">		
				<div class="col-lg-3 col-xs-3">	
					<label >Period *</label> 	
					<input type="text" id="period" name ="period" class = "input-block-level period"  readonly  value="<?=$_POST['period']?>" placeholder="Period*" />		 
					<label class="error_period" style="display:none;color:#CA4B4B;">Period can not be empty.</label> 
				
					<br/><br/>
					<label >Portfolio*</label> 	
					<input type="file" id="CVSFile" name ="CVSFile" class = "input-block-level CVSFile" />	
					<input type="hidden" id="filename" name ="filename" />	
					<input type="hidden" id="Proceed" name ="Proceed" value="" />
					<input type="hidden" id="securities" name ="securities" value="" />	
					<input type="hidden" id="SecuritiesWeightJSON" name ="SecuritiesWeightJSON" value="" />						
					<label class="error_CVSFile" style="display:none;color:#CA4B4B;">Upload Portfolio.</label> 
					
					<br/><br/>
					<label >Treatment for spin off adjustment*</label> 	<br>
					<label style="margin-right:10px;"><input type="radio" class="input-block-level" name="spinoff" value="0" checked> Divisor </label >
					<label ><input type="radio" class="input-block-level" name="spinoff" value="1"> Stock </label >
										
					
					<br/><br/>
					<label >Treatment for dividend adjustment*</label> 	<br>
					<label style="margin-right:10px;"><input type="radio" class="input-block-level" name="dividend" value="0" checked> Divisor </label>
					<label ><input type="radio" class="input-block-level" name="dividend" value="1">  Stock</label>
					
					<br/><br/>
					<label style="margin-right:10px;">Currency*</label> 	
					<select class ="input-block-level" name = "currency" > 
					<option value ="USD" >USD</option>
					<option value ="GBP" >GBP</option>
					<option value ="EUR" >EUR</option>
					<option value ="HKD" >HKD</option>
					<option value ="INR" >INR</option>
					</select>
					
										
					
					
				</div>
				<div class="col-lg-6 col-xs-6" id="div_period_with_dates">	
						<div class="row">
								<div class="col-lg-2 col-xs-2"><label class="sr_period">Period</label></div>
								<div class="col-lg-5 col-xs-5">
									<label class="sr_period">Start Date (MM/DD/YYYY)</label>								
								</div>
								<div class="col-lg-5 col-xs-5"><label class="sr_period">End Date (MM/DD/YYYY)</label></div>
							</div>
							
						<?php 
						for($i=1;$i<=$_POST['period'];$i++) { 
						
						$startDate = $_POST['StartDate'][$i-1];
						$endDate = $_POST['EndDate'][$i-1];
						?>
							<div class="row">
								<div class="col-lg-2 col-xs-2"><label class="sr_period"><?=$i?></label></div>
								<div class="col-lg-5 col-xs-5">
									<input  type="text" class="input-block-level datepicker Startdatetxt" id = "StartDate_<?=$i?>" name = "StartDate[]"  value="<?=$startDate?>" placeholder="Start Date" readonly />
								
								</div>
								<div class="col-lg-5 col-xs-5"><input  type="text" class="input-block-level datepicker Enddatetxt" id = "EndDate_<?=$i?>" name = "EndDate[]"  value="<?=$endDate?>" placeholder="End Date" readonly /></div>
							</div>
					<?php } ?>
					<div class="row">
					<div class="col-lg-2 col-xs-2"> </div>
					<div class="col-lg-5 col-xs-5"><label class="error_StartDate" style="display:none;color:#CA4B4B;">All start dates are not fill.</label> </div>
					<div class="col-lg-5 col-xs-5"><label class="error_EndDate" style="display:none;color:#CA4B4B;">All end dates are not fill.</label> </div>
					</div>
				</div>	

				<div class="col-lg-3 col-xs-3">		
				<input  type="button" class="btn btn-primary" name = "back0" id="back0" value="Back" /> 
				<input  type="button" class="btn btn-primary" name = "Step1" id="Step1" value="Validate" /> 
				</div>
			</form>
		</div>
	<?php } else { ?>	
		<div class="row">
			<form name="frmStep0" id="frmStep0" action="" method="post" >		
				<div class="col-lg-3 col-xs-3">	
					<label >Period *</label> 	
					<input type="text" id="period" name ="period" class = "input-block-level period"  value="<?=$_POST['period']?>" placeholder="Period*" />		 
					<label class="error_period" style="display:none;color:#CA4B4B;">Period can not be empty.</label> 
				</div>
				<div class="col-lg-6 col-xs-6" id="div_period_with_dates">		
						

				</div>	

				<div class="col-lg-3 col-xs-3">		

				<input  type="submit" class="btn btn-primary" name = "Step0" id="Step0" value="Next" /> 
				</div>
			</form>
		</div>
	<?php } ?>
		<br/><br/><br/>
		<div class="row"><div class="col-lg-4 col-xs-4"></div>
		<div class="col-lg-4 col-xs-4"><label id="working" style="display:none;background-color:#222d32;border-color:#222d32; " class="btn btn-primary"> System is working... Please wait a while.</label></div>
		<div class="col-lg-4 col-xs-4"></div>
		</div>	
	</div>


<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js"></script>
<script src="http://localhost/backtestengine/plugins/daterangepicker/daterangepicker.js"></script>
<!-- datepicker -->
<script src="http://localhost/backtestengine/plugins/datepicker/bootstrap-datepicker.js"></script>
  <script> 
  $(document).ready(function() {
	$("#frmStep0").submit(function() {	
		var period = $("#period").val();
		var flag = true;			
		//period  = period.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, ' ');	
		period = $.trim(period);			
		$("#period").val(period);
		
		if(!period) {
			$("#period").focus();
			$(".error_period").html("Period can not be empty.");
			$(".error_period").show();				
			flag = false;
		} else if(/^[a-zA-Z0-9- ]*$/.test(period) == false) {			
			$("#period").focus();
			$(".error_period").html("Period contains illegal characters.");
			$(".error_period").show();
			flag = false;
		} else if(!$.isNumeric( period)) {
			$("#period").focus();
			$(".error_period").html("Period must be numeric.");
			$(".error_period").show();				
			flag = false;
		}  else {
			$(".error_period").hide();
			
		} 
		
		return flag;
		//$("#frmlist").submit();
	});
	

	$( "#Step1" ).click(function() {
						
		var period = $("#period").val();
		$("#result").html("");
		var flag = true;			
		period  = period.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, ' ');			
		period = $.trim(period);			
		$("#period").val(period);
		var Nperiod = parseInt(period, 10) * 1;	
		
		if(!period) {
			$("#period").focus();
			$(".error_period").html("Period can not be empty.");
			$(".error_period").show();				
			flag = false;
		} else if(!Nperiod) {
			$("#period").focus();
			$(".error_period").html("Period must be numeric.");
			$(".error_period").show();				
			flag = false;
		}  else {
			$(".error_period").hide();
			
		} 
		var StartDateFlag 	= false;
		var EndDateFlag 	= false;
		
		var totalStartDates = $( "input[name='StartDate[]']" ).length;		
		var totalStartDatesCount = 0;
		
		$( "input[name='StartDate[]']" ).each(function( index ) {
		  if($( this ).val()) {
			  totalStartDatesCount++;
		  }
		});
		
		if(totalStartDates!=totalStartDatesCount) {			
			$(".error_StartDate").html("All start dates are not fill.");
			$(".error_StartDate").show();
			flag = false;
		}
		var totalEndDates = $( "input[name='EndDate[]']" ).length;		
		var totalEndDateCount = 0;
		
		$( "input[name='EndDate[]']" ).each(function( index ) {
		  if($( this ).val()) {
			  totalEndDateCount++;
		  }
		});
		
		if(totalEndDates!=totalEndDateCount) {			
			$(".error_EndDate").html("All end dates are not fill.");
			$(".error_EndDate").show();
			flag = false;
		}
		
		if( (totalStartDates == totalEndDateCount) && ( totalEndDateCount == totalStartDatesCount) ) {			
			for(var i = 2; i <=totalStartDates; i++ ) {
				var StartDate = $( "#StartDate_" + i ).val();
				var previousID = i-1;
				var EndDate = $( "#EndDate_" + previousID ).val();				
				if(StartDate	!=	EndDate) {					
					$(".error_StartDate").html(	"Period - " + i + " start date does not match with period - "+ previousID + " end date.");
					$(".error_StartDate").show();
					flag = false;
					break;
				}
			}
			
			if(flag) {
				for(var i = 1; i <= totalStartDates; i++ ) {
					var StartDate = $( "#StartDate_" + i ).val();				
					var EndDate = $( "#EndDate_" + i ).val();
					if(Date.parse(StartDate) > Date.parse(EndDate)) {						
						$(".error_StartDate").html(	"Period - " + i + " start date should be less than  period - "+ i + " end date.");
						$(".error_StartDate").show();
						flag = false;
						break;
					}
				}
			}
			
			if(flag) {
				if(!$('#CVSFile').val()) {
					$(".error_CVSFile").html("Please upload Portfolio.");
					$(".error_CVSFile").show();		
					$("#result").html("");	
					flag = false;
				} else {					
					var fileExtension = ['csv', 'CSV'];
					if ($.inArray($('#CVSFile').val().split('.').pop().toLowerCase(), fileExtension) == -1) {			
						$(".error_CVSFile").html("Only 'csv' format is allowed.");
						$(".error_CVSFile").show();	
						$("#result").html("");						
						flag = false;
					}		
				}	
			}
			
			
			
		}				
		
		// on fornt end validation sucess
		if(flag) {
			// Get form
			var form = $('#frmStep1')[0];

			// Create an FormData object
			var data = new FormData(form);

			// disabled the submit button
			$("#Step1").prop("disabled", true);
			$("#CVSFile").hide();
			$("#working").show();
			
			$.ajax({
				type: "POST",
				enctype: 'multipart/form-data',
				url: "filevalidations.php",
				data: data,
				processData: false,
				contentType: false,
				cache: false,				
				success: function (data) {					
					console.log(data);				
					var obj = jQuery.parseJSON(data);
					if(obj.success) {
						var varconfirm = false;	
						if(obj.message)  {
							$("#result").html(obj.message + obj.warrning);	
							$("#Step1").prop("disabled", false);
							$("#CVSFile").show();
							$("#working").hide();							
						} else {							
							$("#filename").val(obj.file);							
							$("#Proceed").val("Proceed");
							$("#Step1").prop("disabled", false);
							$("#CVSFile").show();
							$("#working").hide();
							$("#securities").val(obj.Securities);
							
							//var SecuritiesWeightJSON = jQuery.parseJSON(obj.SecuritiesWeightJSON);
							$("#SecuritiesWeightJSON").val(obj.SecuritiesWeightJSON);							
							
							var Thedates = jQuery.parseJSON(obj.thedates);
							
							var i;
							for (i = 0; i < Thedates.length; i++) {
								var x = i+1; 
								$( "#StartDate_"+x).val(Thedates[i]);
							}
							
							
							// code to reset all dates 
							if(obj.warrning){							
								$("#result").html(obj.warrning);
								var txt = obj.warrningNoHTML;																
								setTimeout( function(){
									varconfirm = confirm("Warning : " + txt + " Do you want proceed?");
								}, 100);
							} else {
								$("#result").html("");
								setTimeout( function(){
									varconfirm = confirm("There is no error. do you want proceed?");
								}, 100);
							
							}
							setTimeout( function(){							
								if (varconfirm) {								
									$("#frmStep1").submit();									
								} else { alert("no");								
									$("#Step1").prop("disabled", false);
									$("#CVSFile").show();
									$("#filename").val(obj.file);							
									$("#Proceed").val("delete");	
									var form = $('#frmStep1')[0];
									// Create an FormData object
									var data = new FormData(form);
									$.ajax({
											type: "POST",										
											url: "deletefile.php",
											data: data,
											processData: false,
											contentType: false,
											cache: false,										
											success: function (data) {											
											}										

										});
										$("#Proceed").val("");
									
								}

							
							}, 150);	
							
						}					
					} else {
						$("#result").html("<li style='list-style:none;'>something gone wrong, Please try again</li>");					
						$("#Step1").prop("disabled", false);
						$("#CVSFile").show();
						$("#working").hide();
					}					
					
				
					
					
				},
				error: function (e) {

					$("#result").html("<li style='list-style:none;'>something gone wrong, Please try again</li>");					
					$("#Step1").prop("disabled", false);
					$("#CVSFile").show();
					$("#working").hide();

				}

			});

		}
		
	});
	
	$('#CVSFile').change(function() {
		$("#result").html("");
		var fileExtension = ['csv', 'CSV'];
		if ($.inArray($(this).val().split('.').pop().toLowerCase(), fileExtension) == -1) {
			$(".error_CVSFile").html("Only 'csv' format is allowed.");
			$(".error_CVSFile").show();				
			flag = false;
		} else  {
			$(".error_CVSFile").hide();	
		}
		
	});
	
	$( ".datepicker").on('click',function(e){
		$(".error_StartDate").hide();	
		$(".error_EndDate").hide();				
	});
	
	var totalEndDates = $( "input[name='EndDate[]']" ).length;	
	
	$( ".datepicker").on('change',function(e){
		
		setTimeout( function(){
			// nothing to do 
		}, 100);
		
		if($(this).hasClass("Enddatetxt")) {
			var ID = $(this).attr("id");			
			var n = ID.indexOf("totalEndDates");			
			if(n==-1){
				var TmpStID = ID.split("_"); StartDate_1
				var StID = parseInt(TmpStID[1]) ;
				var NextStartID = StID + 1;
				$("#StartDate_"+NextStartID).val($(this).val());
				//alert($(this).val());
			}
		}
		
	});
		
		
   $(".datepicker").datepicker({
		autoclose: true,		
		endDate: '0d'
	});
   
	$( "#back0").on('click',function(e){		
		window.history.back();		
	});
		
	
  });
  
  </script>
<?php require_once("footer.php"); ?>
