<?php
require_once("header.php");
$messgae 		= ""; 
$warrning 		= "";  
$buttonFlag 	= false;  
$securities 	= array();
$currency 		= 'USD'; 
$showPRD 		= 0; 
$StartDate 		= array();
$EndDate 		= array();



if($_POST['Proceed']=="Proceed") {
	$securities 	= JSON_decode($_POST['securities']);
	$currency 		= $_POST['currency'];
	$period 		= $_POST['period'];
	$StartDate 		= $_POST['StartDate'];
	$EndDate 		= $_POST['EndDate'];
	$totaldaysCount = 0;
	$totalsecuritiesCount = 0;	
	$_SESSION['post'] = $_POST; 
	
	
}  

if(isset($_GET['date']))
	$currentDate 			= date( 'Y-m-d',strtotime($_GET['date']));
else 
	$currentDate 			= date( 'Y-m-d',strtotime($StartDate[0]));

if(isset($_GET['pd']))
	$currentpd 			= $_GET['pd'];
else 
	$currentpd 			= 0;

$date = '';

 

?>
	<div class="container main-body">	
		<div class="row">
				<div class="col-lg-6 col-xs-6"><label></label></div>
				<div class="col-lg-6 col-xs-6"><a class="btn btn-primary" href="calculations.php">New Calculation </a></div>
			</div>
			<div class="row"> &nbsp </div><div class="row"> &nbsp </div>
			<div class="row">
				<div class="col-lg-12 col-xs-12"><label><?php echo "Data of period ".( $currentpd + 1 )." and Date (MM/DD/YYYY) - $currentDate" ; ?></label></div>
			</div>
			
			<div class="row"> &nbsp </div><div class="row"> &nbsp </div>
			
		<div class="row">								
					<div class="col-lg-3 col-xs-3"><label>Security ISN</label></div>
					<div class="col-lg-3 col-xs-3"><label>Currency</label></div>
					
					<div class="col-lg-3 col-xs-3"><label>Price</label></div>
					<div class="col-lg-3 col-xs-3"><label>Excange Rate</label></div>
			</div>
			
			<?php
 
		$securities 	= JSON_decode($_SESSION['post']['securities']);
		$currency 		= $_SESSION['post']['currency'];
	
			for($chkISN = 0; $chkISN < count($securities[$currentpd]); $chkISN++) {
				$securityISN 	= $securities[$currentpd][$chkISN];
				$price = 0.0;
				$exRate = 0.0;
								
				$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
				$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
				$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
				$qry .= " ON PRC.fs_perm_sec_id = ISN.fs_primary_listing_id";
				$qry .= " WHERE ISN.isin = '".$securityISN."'  AND  PRC.date = '".$currentDate."'";
				$qry .= " AND PRC.currency = '".$currency."'";
				
				//echo $qry; 
				$records =  array();			
				$records =  (array) $db->query($qry);
									
				if(count($records)<=0) {									
					$price  = 0.0;		
				} else {
					if($records['p_price'])						
						$price  = $records['p_price'];
					else
						$price  = 0.0;	
				}
			
			?>
			
			<div class="row">				
				<div class="col-lg-3 col-xs-3"><?php echo $securityISN;?></div>
				<div class="col-lg-3 col-xs-3"><?php echo $currency?></div>				
				<div class="col-lg-3 col-xs-3"><?php echo $price;?></div>
				<div class="col-lg-3 col-xs-3">Excange Rate</div>
			</div>
				
			<?php } ?>
			
		<div class="row"> &nbsp </div><div class="row"> &nbsp </div>
		<div class="row pagging">
				<div class="col-lg-12 col-xs-12">
				<?php 	 for($di=0 ; $di < count($_SESSION['post']['StartDate'] ); $di++) {	
				
					$date = date( 'Y-m-d', strtotime( $_SESSION['post']['StartDate'][$di] ) );	
					$endDateFormate = date( 'Y-m-d', strtotime( $_SESSION['post']['EndDate'][$di]. ' +1 day' ) );
				?>	
				<div class="row pagging"><div class="col-lg-2 col-xs-2">Dates of Period -  <?php echo $di + 1 ?> </div>
				<div class="col-lg-10 col-xs-10">
				<?php
				while($date	!=	$endDateFormate){
						
					$DateFormateToshow = date( 'm/d/Y', strtotime( $date ) );		
				?>
					<?php if($currentDate==$date) { ?>
						<label><a href="process.php?pd=<?php echo $di?>&date=<?php echo $date;?>" style="padding-left:5px;"><?php echo $DateFormateToshow;?></a></label>
					<?php } else { ?> 
						<a href="process.php?pd=<?php echo $di?>&date=<?php echo $date;?>" style="padding-left:5px;"><?php echo $DateFormateToshow;?></a>
					<?php } ?>					
				<?php $date = date( 'Y-m-d', strtotime( $date . ' +1 day' ) ); } ?>
				</div>				
			</div>	
				<?php } ?>
					
	</div>


<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js"></script>
<script src="http://localhost/backtestengine/plugins/daterangepicker/daterangepicker.js"></script>
<!-- datepicker -->
<script src="http://localhost/backtestengine/plugins/datepicker/bootstrap-datepicker.js"></script>

<?php require_once("footer.php"); ?>
