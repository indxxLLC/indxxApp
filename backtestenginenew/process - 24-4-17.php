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

$TmpPriceRecords = array();
$TmpDividendRecords = array();
$TmpSplitsRecords = array();
$TmpExRates	 = array();
$DatabaseCurrency	 = array();
$DataTmpPrice = array();
$AllisinBasicCurrencey = array();
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
			
			//DatabaseCurrency
			
			
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
			
			
			
			$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id,ISN.isin"; 
			$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
			$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
			$qry .= " ON PRC.fs_perm_sec_id = ISN.fs_primary_listing_id";
			$qry .= " WHERE ISN.isin in  (".$TmpSecuritiesISN.")  AND  PRC.date between '".$StartDateDB."' and '".$EndDateDB ."'";
			//$qry .= " AND PRC.currency = '".$currency."'";				
			$qry .= " ORDER BY ISN.isin, PRC.date ";
			
			$a = sqlsrv_query( $connection, $qry );
			
			$count= 0;
				
			while( $record = sqlsrv_fetch_array( $a, SQLSRV_FETCH_ASSOC) ) {
				
				$DBdatArray = (array) $record['date'];
				
				$divqry = "SELECT DIV.p_divs_pd , DIV.currency,DIV.date , DIV.p_divs_s_spinoff, DIV.fs_perm_sec_id,ISN.isin"; 
				$divqry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_dividends  AS DIV"; 
				$divqry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
				$divqry .= " ON DIV.fs_perm_sec_id = ISN.fs_primary_listing_id";
				$divqry .= " WHERE ISN.isin = '".$record['isin'].")  AND  DIV.date = '".$DBdatArray['date']."'";							
				$divqry .= " ORDER BY ISN.isin, DIV.date ";

				$b = sqlsrv_query( $connection, $divqry );

				$Divcount= 0;

				$TmpDividendRecords = sqlsrv_fetch_array( $b, SQLSRV_FETCH_ASSOC) ) ;
				
				if($count>0) {					
					if($TmpPriceRecords[$prd][$count-1]['p_price'] != $record['p_price'] || $TmpPriceRecords[$prd][$count-1]['date'] != $DBdatArray['date'] || $TmpPriceRecords[$prd][$count-1]['isin'] != $record['isin']) {
						
						$TmpPriceRecords[$prd][$count]['p_price'] 	= $record['p_price'];
						$TmpPriceRecords[$prd][$count]['date'] 		= date( 'Y-m-d', strtotime($DBdatArray['date']) );
						$TmpPriceRecords[$prd][$count]['isin'] 		= $record['isin'];
						$TmpPriceRecords[$prd][$count]['currency'] 	= $record['currency'];
						
						$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['price'] 		= $record['p_price'];
						$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['currency'] 	= $record['currency'];
						$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['dividend'] 	= $TmpDividendRecords['dividend'];
						$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['spinoff'] 	= $TmpDividendRecords['p_divs_s_spinoff'];
						$AllisinBasicCurrencey[$prd][$count] = $record['currency'];
						
						$count++;
					} 
					
				} else {				
					$TmpPriceRecords[$prd][$count]['p_price'] 	= $record['p_price'];
					$TmpPriceRecords[$prd][$count]['date'] 		= date( 'Y-m-d', strtotime($DBdatArray['date']) );
					$TmpPriceRecords[$prd][$count]['isin'] 		= $record['isin'];
					$TmpPriceRecords[$prd][$count]['currency'] 	= $record['currency'];
					
					$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['price'] = $record['p_price'];
					$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['currency'] =	$record['currency'];
					$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['dividend'] 	= $TmpDividendRecords['dividend'];
					$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['spinoff'] 	= $TmpDividendRecords['p_divs_s_spinoff'];
					$AllisinBasicCurrencey[$prd][$count] = $record['currency'];	
					$count++;
				}
				
				
				
				
			}
			
			
			$qry = "SELECT DIV.p_divs_pd , DIV.currency,DIV.date , DIV.p_divs_s_spinoff, DIV.fs_perm_sec_id,ISN.isin"; 
			$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_dividends  AS DIV"; 
			$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
			$qry .= " ON DIV.fs_perm_sec_id = ISN.fs_primary_listing_id";
			$qry .= " WHERE ISN.isin in  (".$TmpSecuritiesISN.")  AND  DIV.date between '".$StartDateDB."' and '".$EndDateDB ."'";							
			$qry .= " ORDER BY ISN.isin, DIV.date ";
			
			$b = sqlsrv_query( $connection, $qry );
			
			$Divcount= 0;
				
			while( $record = sqlsrv_fetch_array( $b, SQLSRV_FETCH_ASSOC) ) {
				
				$DBdatArray = (array) $record['date'];
				
				if($Divcount>0) {	
				
					if($TmpDividendRecords[$prd][$Divcount-1]['dividend'] != $record['p_divs_pd'] || $TmpDividendRecords[$prd][$Divcount-1]['date'] !=  date( 'Y-m-d', strtotime($DBdatArray['date']) )|| $TmpDividendRecords[$prd][$Divcount-1]['isin'] != $record['isin']) {						
						
						$TmpDividendRecords[$prd][$Divcount]['dividend'] 			= $record['p_divs_pd'];
						$TmpDividendRecords[$prd][$Divcount]['spinoff'] 			= $record['p_divs_s_spinoff'];
						$TmpDividendRecords[$prd][$Divcount]['date'] 				=  date( 'Y-m-d', strtotime($DBdatArray['date']) );
						$TmpDividendRecords[$prd][$Divcount]['isin'] 				= $record['isin'];
						$Divcount++;
					} 
					
				} else {				
					$TmpDividendRecords[$prd][$Divcount]['dividend'] 			= $record['p_divs_pd'];
					$TmpDividendRecords[$prd][$Divcount]['spinoff'] 			= $record['p_divs_s_spinoff'];
					$TmpDividendRecords[$prd][$Divcount]['date'] 				= date( 'Y-m-d', strtotime($DBdatArray['date']) );
					$TmpDividendRecords[$prd][$Divcount]['isin'] 				= $record['isin'];
					$Divcount++;
				}
				
				
				
				
			}
			
			
			$qry = "SELECT SPT.p_split_factor, SPT.date, SPT.fs_perm_sec_id, ISN.isin"; 
			$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_splits  AS SPT"; 
			$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
			$qry .= " ON SPT.fs_perm_sec_id = ISN.fs_primary_listing_id";
			$qry .= " WHERE ISN.isin in  (".$TmpSecuritiesISN.")  AND  SPT.date between '".$StartDateDB."' and '".$EndDateDB ."'";							
			$qry .= " ORDER BY ISN.isin, SPT.date ";
			
			$c = sqlsrv_query( $connection, $qry );
			
			$Sptcount= 0;
				
			while( $record = sqlsrv_fetch_array( $c, SQLSRV_FETCH_ASSOC) ) {
				
				$DBdatArray = (array) $record['date'];
				
				if($Sptcount>0) {					
					if($TmpSplitsRecords[$prd][$Sptcount-1]['split'] != $record['p_split_factor'] || $TmpSplitsRecords[$prd][$Sptcount-1]['date'] != date( 'Y-m-d', strtotime($DBdatArray['date']) ) || $TmpSplitsRecords[$prd][$Sptcount-1]['isin'] != $record['isin']) {
						
						$TmpSplitsRecords[$prd][$Sptcount]['split'] 			= $record['p_split_factor'];						
						$TmpSplitsRecords[$prd][$Sptcount]['date'] 			= date( 'Y-m-d', strtotime($DBdatArray['date']) );
						$TmpSplitsRecords[$prd][$Sptcount]['isin'] 			= $record['isin'];
						$Sptcount++;
					} 
					
				} else {				
					$TmpSplitsRecords[$prd][$Sptcount]['split'] 				= $record['p_split_factor'];					
					$TmpSplitsRecords[$prd][$Sptcount]['date'] 				= date( 'Y-m-d', strtotime($DBdatArray['date']) );
					$TmpSplitsRecords[$prd][$Sptcount]['isin'] 				= $record['isin'];
					$Sptcount++;
				}
				
				
				
				
			}
			
			
			
			$count = 1;
			for($abc = 0 ; $abc < $count; $abc++){
			 $sr = $abc + 1;  
			$securityISN 	= $TmpPriceRecords[$prd][$abc]['isin'];
			$dateToShow 	= date( 'm/d/Y', strtotime( $TmpPriceRecords[$prd][$abc]['date']) );
			$price 			= $TmpPriceRecords[$prd][$abc]['p_price'];
			
				echo '<div class="row">';
				echo '<div class="col-lg-1 col-xs-1">'. $sr.'</div>';
				echo '<div class="col-lg-3 col-xs-3">'.$securityISN.'</div>';
				echo '<div class="col-lg-2 col-xs-2">'.$currency.'</div>';
				echo '<div class="col-lg-2 col-xs-2">'.$dateToShow.'</div>';
				echo '<div class="col-lg-2 col-xs-2">'.$price.'</div>';
				echo '<div class="col-lg-2 col-xs-2">Excange Rate</div>';
				echo '</div>';
			}
			
			
		}
		
		$StartDateDB 	= date( 'Y-m-d', strtotime( $_POST['StartDate'][0]) );
		$EndDateDB 		= date( 'Y-m-d', strtotime($_POST['EndDate'][count($_POST['EndDate'])-1]) );
		
		$DifferentCurrencies = '';
		for($sh = 0; $sh < count($AllisinBasicCurrencey); $sh++) {		
		$tmp = array_unique($AllisinBasicCurrencey[0]);
			foreach($tmp as $k => $vl) {
					$DifferentCurrencies .= "'".$vl."',";
			}		
		}
		
		$DifferentCurrencies =  substr($DifferentCurrencies,0,strlen($DifferentCurrencies)-1);
		
		$qry = "SELECT RTS.iso_currency, RTS.date, RTS.exch_rate_usd, RTS.exch_rate_per_usd"; 
		$qry .= " FROM FDS_DataFeeds.ref_v2.fx_rates_usd  AS RTS"; 			
		$qry .= " WHERE RTS.date between '".$StartDateDB."' and '".$EndDateDB ."'";	
		$qry .= " and RTS.iso_currency in ( ".$DifferentCurrencies.")";			
		$qry .= " ORDER BY RTS.date ";
		
		$d = sqlsrv_query( $connection, $qry );
		
		$EXcount= 0;
			
		while( $record = sqlsrv_fetch_array( $d, SQLSRV_FETCH_ASSOC) ) {
			
			$DBdatArray = (array) $record['date'];
			$TmpExRates[$prd][$EXcount]['iso_currency'] 				= $record['iso_currency'];					
			$TmpExRates[$prd][$EXcount]['date'] 						= date( 'Y-m-d', strtotime($DBdatArray['date']) );
			$TmpExRates[$prd][$EXcount]['exch_rate_usd'] 				= $record['exch_rate_usd'];
			$TmpExRates[$prd][$EXcount]['exch_rate_per_usd'] 			= $record['exch_rate_per_usd'];
			$EXcount++;
		}
		echo "Price Data : <pre>";
		print_r($DataTmpPrice); 
		echo "</pre>";
		
		echo "Dividends Data : <pre>";
		print_r($TmpDividendRecords); 
		echo "</pre>";

		echo "Splits  Data : <pre>";
		print_r($TmpSplitsRecords); 
		echo "</pre>";	
		
		echo "Excange Rates : <pre>";
		print_r($TmpExRates); 
		echo "</pre>";					
		?>
	</div>


<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js"></script>
<script src="http://localhost/backtestengine/plugins/daterangepicker/daterangepicker.js"></script>
<!-- datepicker -->
<script src="http://localhost/backtestengine/plugins/datepicker/bootstrap-datepicker.js"></script>

<?php require_once("footer.php"); ?>
