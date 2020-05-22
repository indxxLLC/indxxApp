<?php
session_start();
$flag=false;

if(!empty($_SESSION) && $_SESSION['userDisplayNamne'] !="")
{
	$flag=true;
	//echo 1;
	//header("location:calculations.php");
}
elseif(isset($_GET['Email']) && isset($_GET['usname'])){
	
$_SESSION['userDisplayNamne'] = $_GET['usname']; 
	
$_SESSION['userDisplayPic'] = $_GET['usname'];
$flag=true;
//echo 2;

}
//exit;
if($flag){

//$_SESSION['userDisplayNamne'] = $_GET['usname']; 
	header("location:calculations.php");
	
}
else{
	header("location: https://www.gathan.in/");
	
}




require_once("header.php");
?>


   <div class="row">
    <div class="col-lg-4 col-xs-4">
	</div>
        <div class="col-lg-4 col-xs-4">
 
   
      <form class="form-signin" id="form-signin" name="form-signin" action="" method="post">
	 <?php if(isset($msg)) { ?>
	  <div class="div_message">        
		<label class="error_message" style="color:#CA4B4B;"><?=$msg?></label> 
		</div>
	 <?php } ?>
        <div class="div_username">
        <input name="username" type="text" class="form-control username"  value="" placeholder="Email address">
		<label class="error_username" style="display:none;color:#CA4B4B;">Email address not valid!</label> 
		</div>
		<div class="div_username">
        <input name="password" type="password" class="form-control password" value="" placeholder="Password">
		<label class="error_password" style="display:none;color:#CA4B4B;">Password can not be empty!</label> 
		</div>  
		<div class="div_username">      
         <input class="form-control btn  btn-primary " type="submit" name="login" id="btnlogin"  value="Log in" />
		 </div>
      </form>
	</div>
	 <div class="col-lg-4 col-xs-4"> </div>
	
    </div>
 
 
    
	<script>
	$( document ).ready(function() {
		$(".username").on('input',function(e){
			$(".error_username").hide();		
		});
		$(".password").on('input',function(e){
			$(".error_password").hide();		
		});
				
		$( "#form-signin" ).submit(function(event) {			
			var flag = true;			
			var username = $(".username").val();
			var password = $(".password").val();
			if(!username) {
				$(".username").focus();
				$(".error_username").html("Email address can not empty.");
				$(".error_username").show();
				flag = false;
			} else if(!isValidEmailAddress(username)) {
				$(".username").focus();
				$(".error_username").html("Email address not valid!");				
				$(".username").val(username);
				$(".error_username").show();
				flag = false;
			} else {
				$(".error_username").hide();
			}
			if(!password) {
				$(".password").focus();
				$(".error_password").html("Password can not empty.");
				$(".error_password").show();
				flag = false;
			} else {
				$(".error_password").hide();
			}	
			
			return flag;
		});
		function isValidEmailAddress(emailAddress) {
			var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
			return pattern.test(emailAddress);
		};
	});
	</script>
	
 
  <?php require_once("footer.php"); ?>


 
