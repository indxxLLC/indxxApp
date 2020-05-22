<?php
require_once("header.php");
$messgae 		= ""; 
$warrning 		= "";  
$buttonFlag 	= false;  
$securities 	= array();
$currency 		= 'USD'; 
$showPRD 		= 0; 

echo "<pre>";
print_r($_POST);
echo "</pre>";
$securities 	= JSON_decode($_POST['securities']);
$currency 		= $_POST['currency'];
$period 		= $_POST['period'];
$StartDate 		= $_POST['StartDate'];
$EndDate 		= $_POST['EndDate'];

$totaldaysCount = 0;
for($i=0;$i<count($StartDate);$i++) {
	$tmpStartDate 	= strtotime($StartDate[$i]);
	$tmpEndDate		= strtotime($EndDate[$i]);
	$datediff = $tmpEndDate - $tmpStartDate;
	$totaldaysCount +=  floor($datediff / (60 * 60 * 24));	
}

echo $TotalRecords 	= $period * count($securities) * $totaldaysCount; 

die;   
?>
	<div class="container main-body">	
		<div class="row">
				<div class="col-lg-6 col-xs-6"><label>System is working Please wait...</label></div>
				<div class="col-lg-6 col-xs-6"><a class="btn btn-primary" href="calculations.php">New Calculation </a></div>
			</div>
		<div class="row" id="resultDiv">
				
		</div>
		<form name="process" id="process" action="" method="post" >
			<input type="hidden" id="filename" name ="filename" value="<?php echo $_POST['filename']?>" />	
			<input type="hidden" id="Proceed" name ="Proceed" value="<?php echo $_POST['Proceed']?>" />
			<input type="hidden" id="securities" name ="securities" value="<?php echo $_POST['securities']?>" />
			<input type="hidden" id="period" name ="period" value="<?=$_POST['period']?>"  />
			<input type="hidden" id="spinoff" name ="spinoff" value="<?php echo $_POST['spinoff']?>" />	
			<input type="hidden" id="dividend" name ="dividend" value="<?php echo $_POST['dividend']?>" />
			<input type="hidden" id="currency" name ="currency" value="<?php echo $_POST['currency']?>" />
			<?php foreach($prd = $_POST['StartDate'] as $ky => $val) { ?>
			<input  type="hidden" name = "StartDate[]"  value="<?=$val?>" />
			<?php } ?>
			<?php foreach($prd = $_POST[''] as $ky => $val) { ?>
			<input  type="hidden" name = "EndDate[]"  value="<?=$val?>" />
			<?php } ?>			
		</form>
		<?php
		
		
		
		
		for($prd = 0; $prd < count($period); $prd++) {
			$showPRD = $prd + 1 ; 
			?>
			<div class="row">
				<div class="col-lg-12 col-xs-12"><label><?php echo "Data of period $showPRD"; ?></label></div>
			</div>
			<div class="row">
					<div class="col-lg-1 col-xs-1"><label>SR</label></div>
					<div class="col-lg-3 col-xs-3"><label>Security ISN</label></div>
					<div class="col-lg-2 col-xs-2"><label>Currency</label></div>
					<div class="col-lg-2 col-xs-2"><label>Date (MM/DD/YYYY)</label></div>
					<div class="col-lg-2 col-xs-2"><label>Price</label></div>
					<div class="col-lg-2 col-xs-2"><label>Excange Rate</label></div>
			</div>
			<?php	
			$sr = 1 ;
			$SecurityISN = '';
			$price = 0.0;
			$exRate = 0.0;
			
			for($chkISN = 0; $chkISN < count($securities[$prd]); $chkISN++) {
				
				$securityISN 	= $securities[$prd][$chkISN];
				$StartDate 		= $_POST['StartDate'][$prd];
				$EndDate 		= $_POST['EndDate'][$prd];
				
				$date 			=  $StartDate ;
				
				while( $date != $EndDate ) { 
					$dateforDB 	= date( 'Y-m-d', strtotime( $date) );					
					$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
					$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
					$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
					$qry .= " ON PRC.fs_perm_sec_id = ISN.fs_primary_listing_id";
					$qry .= " WHERE ISN.isin = '".$securityISN."'  AND  PRC.date = '".$dateforDB."'";
					$qry .= " AND PRC.currency = '".$currency."'";
					
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
						<div class="col-lg-1 col-xs-1"><?php echo $sr;?></div>
						<div class="col-lg-3 col-xs-3"><?php echo $securityISN;?></div>
						<div class="col-lg-2 col-xs-2"><?php echo $currency?></div>
						<div class="col-lg-2 col-xs-2"><?php echo $date;?></div>
						<div class="col-lg-2 col-xs-2"><?php echo $price;?></div>
						<div class="col-lg-2 col-xs-2">Excange Rate</div>
				</div>
				
				<?php
				$sr++;
				$date 		= date( 'm/d/Y', strtotime( $date . ' +1 day' ) );
				}
			}
								
		}
		?>
	</div>


<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js"></script>
<script src="http://localhost/backtestengine/plugins/daterangepicker/daterangepicker.js"></script>
<!-- datepicker -->
<script src="http://localhost/backtestengine/plugins/datepicker/bootstrap-datepicker.js"></script>

<?php require_once("footer.php"); ?>
