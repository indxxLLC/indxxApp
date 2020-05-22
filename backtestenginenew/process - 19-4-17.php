<?php
require_once("header.php");
$messgae 		= ""; 
$warrning 		= "";  
$buttonFlag 	= false;  
$securities 	= array();
$currency 		= 'USD'; 
$showPRD 		= 0; 


$securities 	= JSON_decode($_POST['securities']);
$currency 		= $_POST['currency'];
$period 		= $_POST['period'];
$StartDate 		= $_POST['StartDate'];
$EndDate 		= $_POST['EndDate'];
$Price			= array();	

$sqlsvr_details =   array(  'UID'   => 'sa',
							'PWD'           => 'f0r3z@786',
							'Database'      => 'FDS_Datafeeds',
							'CharacterSet'  => 'UTF-8'
						);

// try to connect                    
$connection = sqlsrv_connect("INDXX", $sqlsvr_details);

echo "<pre>";
print_r($_POST);
echo "</pre>";

?>
	<div class="container main-body">	
		<div class="row">
				<div class="col-lg-6 col-xs-6"><label></label></div>
				<div class="col-lg-6 col-xs-6"><a class="btn btn-primary" href="calculations.php">New Calculation </a></div>
			</div>
		<div class="row" id="resultDiv">
				
		</div>
		
		<?php
		
		
		
		
		for($prd = 0; $prd < $period; $prd++) { 
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
			$TmpSecuritiesISN = '';
			for($chkISN = 0; $chkISN < count($securities[$prd]); $chkISN++) {
				$TmpSecuritiesISN .="'".$securities[$prd][$chkISN]."',";
			}
			$TmpSecuritiesISN =  substr($TmpSecuritiesISN,0,strlen($TmpSecuritiesISN)-1);
			$StartDateDB 	= date( 'Y-m-d', strtotime( $_POST['StartDate'][$prd]) );
			$EndDateDB 		= date( 'Y-m-d', strtotime($_POST['EndDate'][$prd]) );
			
			//echo $TmpSecuritiesISN ; 
			//die;
			
			$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id,ISN.isin"; 
				$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
				$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
				$qry .= " ON PRC.fs_perm_sec_id = ISN.fs_primary_listing_id";
				$qry .= " WHERE ISN.isin in  (".$TmpSecuritiesISN.")  AND  PRC.date between '".$StartDateDB."' and '".$EndDateDB ."'";
				$qry .= " AND PRC.currency = '".$currency."'";
				//$qry .= " GROUP BY  PRC.date ";
				$qry .= " ORDER BY ISN.isin, PRC.date ";
				
				$a = sqlsrv_query( $connection, $qry );
				$TmpRecords = array();
				$count= 0;
				//$tmpArra  = array();		
				while( $record = sqlsrv_fetch_array( $a, SQLSRV_FETCH_ASSOC) ) {
					$DBdatArray = (array) $record['date'];
					if($count>0) {
						if($TmpRecords[$count-1]['p_price']==$record['p_price'] && $TmpRecords[$count-1]['date']==$record['date'] && $TmpRecords[$count-1]['isin']==$record['isin']) {
							continue;
						} else {
								$TmpRecords[$count] = array($record['p_price'],$DBdatArray['date'],$record['isin']);
						}							
					} else {
						$TmpRecords[$count] = array($record['p_price'],$DBdatArray['date'],$record['isin']);
					}
					$count++;
					
				}
				
				//$TmpRecords =  array_unique($TmpRecords); 
				echo "<pre>";
				print_r($TmpRecords);
				echo "</pre>";
				die;
				
			for($chkISN = 0; $chkISN < count($securities[$prd]); $chkISN++) {
				
				$securityISN 	= $securities[$prd][$chkISN];				
				$StartDateDB 	= date( 'Y-m-d', strtotime( $_POST['StartDate'][$prd]) );
				$EndDateDB 		= date( 'Y-m-d', strtotime($_POST['EndDate'][$prd]) );
				
										
				$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id,ISN.isin"; 
				$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
				$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
				$qry .= " ON PRC.fs_perm_sec_id = ISN.fs_primary_listing_id";
				$qry .= " WHERE ISN.isin = '".$securityISN."'  AND  PRC.date between '".$StartDateDB."' and '".$EndDateDB ."'";
				$qry .= " AND PRC.currency = '".$currency."'";
				$qry .= " GROUP BY  PRC.date ";
				$qry .= " ORDER BY  PRC.date ";
				echo $qry; 
				die;
				
				$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
				$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
				$qry .= " where  PRC.date between '".$StartDateDB."' and '".$EndDateDB ."'";
				$qry .= " AND PRC.currency = '".$currency."'";
				$qry .= " and  PRC.fs_perm_sec_id = ( select ISN.fs_primary_listing_id from FDS_DataFeeds.ids_v1.h_security_isin AS ISN  WHERE ISN.isin = '".$securityISN."' group by ISN.fs_primary_listing_id ) "; 	
				echo $qry .= " order by PRC.date ASC";
				die;
				$a = sqlsrv_query( $connection, $qry );
				$pcount = 0;
					
				while( $record = sqlsrv_fetch_array( $a, SQLSRV_FETCH_ASSOC) ) {
					$DBdatArray = (array) $record['date'];
					$dateToShow = date( 'm/d/Y', strtotime($DBdatArray['date']) );	
					
					$Price[$prd][$securityISN][$dateToShow]['price']	=	$record['p_price'];
					$Price[$prd][$securityISN][$dateToShow]['currency']	=	$currency;				
				?>
					<div class="row">
						<div class="col-lg-1 col-xs-1"><?php echo $sr;?></div>
						<div class="col-lg-3 col-xs-3"><?php echo $securityISN;?></div>
						<div class="col-lg-2 col-xs-2"><?php echo $currency?></div>
						<div class="col-lg-2 col-xs-2"><?php echo $dateToShow;?></div>
						<div class="col-lg-2 col-xs-2"><?php echo $record['p_price'];?></div>
						<div class="col-lg-2 col-xs-2">Excange Rate</div>
					</div>
				
				<?php
					$sr++;
					$pcount++;
					
					}
				//sqlsrv_free_stmt( $result);
				}
			}
			echo "<pre>";
			print_r($Price);
			echo "<pre>";			
		?>
	</div>


<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js"></script>
<script src="http://localhost/backtestengine/plugins/daterangepicker/daterangepicker.js"></script>
<!-- datepicker -->
<script src="http://localhost/backtestengine/plugins/datepicker/bootstrap-datepicker.js"></script>

<?php require_once("footer.php"); ?>
