<?php
require_once("header.php");
$messgae 	= ""; 
$warrning 	= "";  
$buttonFlag = false;  
$securities = array();
$currency 	= 'USD'; 
$showPRD 	= 0; 

echo "<pre>";
	print_r($_POST);
	die;    
?>
	<div class="container main-body">	
		<div class="row">
				<div class="col-lg-6 col-xs-6"><label>System is working Please wait...</label></div>
				<div class="col-lg-6 col-xs-6"><a class="btn btn-primary" href="calculations.php">New Calculation </a></div>
			</div>
		<div class="row" id="resultDiv">
				
		</div>
		<form name="frrmprocess" id="frrmprocess" action="" method="post" >
			<input type="hidden" id="filename" name ="filename" value="<?php echo $_POST['filename']?>" />	
			<input type="hidden" id="Proceed" name ="Proceed" value="<?php echo $_POST['Proceed']?>" />
			<input type="hidden" id="securities" name ="securities" value="<?php echo $_POST['securities']?>" />
			<input type="hidden" id="period" name ="period" value=""  />
			<input type="hidden" id="spinoff" name ="spinoff" value="<?php echo $_POST['spinoff']?>" />	
			<input type="hidden" id="dividend" name ="dividend" value="<?php echo $_POST['dividend']?>" />
			<input type="hidden" id="currency" name ="currency" value="<?php echo $_POST['currency']?>" />
			<input  type="hidden" name = "StartDate"  value="" />
			<input  type="hidden" name = "EndDate"  value="" />			
		</form>
		<?php foreach($prd = $_POST['StartDate'] as $ky => $val) { ?>
			<input  type="hidden" name = "tmpStartDate[]" id="<?php echo $ky?>" value="<?=$val?>" />
			<?php } ?>
			<?php foreach($prd = $_POST['EndDate'] as $ky => $val) { ?>
			<input  type="hidden" name = "tmpEndDate[]" id="tmpEndDate_<?php echo $ky?>"  value="<?=$val?>" />
			<?php } ?>
		
	</div>


<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js"></script>
<script src="http://localhost/backtestengine/plugins/daterangepicker/daterangepicker.js"></script>
<!-- datepicker -->
<script src="http://localhost/backtestengine/plugins/datepicker/bootstrap-datepicker.js"></script>
  <script> 
  $(document).ready(function() {
	  
	var time = 500; 
	var prd = 0;	
	$( "input[name='tmpStartDate[]']" ).each(function() {
	var id = $(this).attr("id");	
      setTimeout( function(){ SetData(id,prd); prd++; }, time);
      time += 500;
  });
  
	 
		
  });
  function SetData(id,prd) { alert(id);		
		$( "input[name='StartDate']" ).val($( "#"+id+"" ).val());
		$( "input[name='EndDate']" ).val($( "#tmpEndDate_"+id+"" ).val());
		$("#period").val(prd);		
		prd++;		
		var form = $('#frrmprocess')[0];
		var data = new FormData(form);
		console.log(data);		
		$.ajax({
			type: "POST",										
			url: "internalprocess.php",
			data: data,
			processData: false,
			contentType: false,
			cache: false,		
			async: false,			
			success: function (response) {	
			console.log(response);			
				$("#resultDiv").append(response);					
					
			},
			error: function (e) {
				alert("error");
			}
		});
  }
  </script>
<?php require_once("footer.php"); ?>
