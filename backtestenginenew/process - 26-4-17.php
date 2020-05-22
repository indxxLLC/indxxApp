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



$TmpPriceRecords = array();
$TmpDividendRecords = array();
$TmpSplitsRecords = array();
$TmpExRates	 = array();
$DatabaseCurrency	 = array();
$DataTmpPrice = array();
$AllisinBasicCurrencey = array();
$SecuritiesWeightJSON  = array();

$TmpSecuritiesWeightJSON = (array) JSON_decode($_POST['SecuritiesWeightJSON']);
foreach($TmpSecuritiesWeightJSON as $tmpval) {
	$SecuritiesWeightJSON[] = (array) $tmpval;
}
unset($TmpSecuritiesWeightJSON);
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
			$qry .= " ORDER BY ISN.isin, PRC.date ";
			
			$a = sqlsrv_query( $connection, $qry );
			
			$count= 0;
				
			while( $record = sqlsrv_fetch_array( $a, SQLSRV_FETCH_ASSOC) ) {
				
				$DBdatArray = (array) $record['date'];
				if($count>0) {					
					if($TmpPriceRecords[$prd][$count-1]['p_price'] != $record['p_price'] || $TmpPriceRecords[$prd][$count-1]['date'] != $DBdatArray['date'] || $TmpPriceRecords[$prd][$count-1]['isin'] != $record['isin']) {
						
						$TmpPriceRecords[$prd][$count]['p_price'] 	= $record['p_price'];
						$TmpPriceRecords[$prd][$count]['date'] 		= date( 'Y-m-d', strtotime($DBdatArray['date']) );
						$TmpPriceRecords[$prd][$count]['isin'] 		= $record['isin'];
						$TmpPriceRecords[$prd][$count]['currency'] 	= $record['currency'];
						
						$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['price'] 		= $record['p_price'];
						$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['currency'] 	= $record['currency'];
						
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
						
						$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['dividend'] 	= $record['p_divs_pd'];
						$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['spinoff'] 	= $record['p_divs_s_spinoff'];
						$Divcount++;
					} 
					
				} else {				
					$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['dividend'] 	= $record['p_divs_pd'];
					$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['spinoff'] 	= $record['p_divs_s_spinoff'];
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
						
						$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['splitfactor'] 	= $record['p_split_factor'];
						$Sptcount++;
					} 
					
				} else {
					$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['splitfactor'] 	= $record['p_split_factor'];
					$Sptcount++;
				}
				
				
				
				
			}
			
		$StartDateDB 	= date( 'Y-m-d', strtotime( $_POST['StartDate'][0]) );
		$EndDateDB 		= date( 'Y-m-d', strtotime($_POST['EndDate'][count($_POST['EndDate'])-1]) );
		
		$DifferentCurrencies = '';
		for($sh = 0; $sh < count($AllisinBasicCurrencey); $sh++) {		
		$tmp = array_unique($AllisinBasicCurrencey[$sh]);
			foreach($tmp as $k => $vl) {
					$DifferentCurrencies .= "'".$vl."',";
			}		
		}
		
		$DifferentCurrencies =  substr($DifferentCurrencies,0,strlen($DifferentCurrencies)-1);
		
		//$DifferentCurrencies .= $DifferentCurrencies.",'USD'";
		
		$qry = "SELECT RTS.iso_currency, RTS.date, RTS.exch_rate_usd, RTS.exch_rate_per_usd"; 
		$qry .= " FROM FDS_DataFeeds.ref_v2.fx_rates_usd  AS RTS"; 			
		$qry .= " WHERE RTS.date between '".$StartDateDB."' and '".$EndDateDB ."'";	
		$qry .= " and RTS.iso_currency in ( ".$DifferentCurrencies.")";			
		$qry .= " ORDER BY RTS.date ";
		
		$d = sqlsrv_query( $connection, $qry );			
		while( $record = sqlsrv_fetch_array( $d, SQLSRV_FETCH_ASSOC) ) {
			
			$DBdatArray = (array) $record['date'];
			$TmpExRates[date( 'Y-m-d', strtotime($DBdatArray['date']) )][$record['iso_currency']]['exch_rate_usd'] 				= $record['exch_rate_usd'];
			
			if($record['exch_rate_per_usd']>0)
				$TmpExRates[date( 'Y-m-d', strtotime($DBdatArray['date']) )][$record['iso_currency']]['exch_rate_per_usd'] 			= $record['exch_rate_per_usd'];
			else
				$TmpExRates[date( 'Y-m-d', strtotime($DBdatArray['date']) )][$record['iso_currency']]['exch_rate_per_usd'] 			=  1.00;
			
			
		}
		
			
			
		}
		
		//echo "<pre>";
		//print_r($TmpExRates);
		//echo "</pre>";	
		//die;
		
		$FinalPriceData = array();
		for($i=0;$i<count( $DataTmpPrice);$i++) {
			foreach($DataTmpPrice[$i] as $IsnKey =>$data) {
				
				$Startdate =  date( 'Y-m-d', strtotime( $_POST['StartDate'][$i] ) );				
				$EndDate   =  date( 'Y-m-d', strtotime( $_POST['EndDate'][$i] ) );
				while($Startdate!=$EndDate) {
					if (array_key_exists($Startdate,$DataTmpPrice[$i][$IsnKey])) {
						
						
						
						
						if($DataTmpPrice[$i][$IsnKey][$Startdate]['price']) {  //echo "<br/>a=>".$DataTmpPrice[$i][$IsnKey][$Startdate]['price'];
							$FinalPriceData[$i][$IsnKey][$Startdate]['price']	=  $DataTmpPrice[$i][$IsnKey][$Startdate]['price'];
						} else  {
							
							
							$dayBefore  =  date( 'Y-m-d', strtotime( $Startdate . ' -1 day' ) );
							$FinalPriceData[$i][$IsnKey][$Startdate]['price'] =$FinalPriceData[$i][$IsnKey][$dayBefore]['price'];
						}
					
						
						
						
						$FinalPriceData[$i][$IsnKey][$Startdate]['currency']= $DataTmpPrice[$i][$IsnKey][$Startdate]['currency'];
						
						if (!array_key_exists('splitfactor',$FinalPriceData[$i][$IsnKey][$Startdate])) {
							$FinalPriceData[$i][$IsnKey][$Startdate]['splitfactor'] = 1;
						}
						if (!array_key_exists('dividend',$FinalPriceData[$i][$IsnKey][$Startdate])) {
							$FinalPriceData[$i][$IsnKey][$Startdate]['dividend'] = 0;							
						}
						if (!array_key_exists('spinoff',$FinalPriceData[$i][$IsnKey][$Startdate])) {
							$FinalPriceData[$i][$IsnKey][$Startdate]['spinoff'] = 0;
						}
						if($TmpExRates[$Startdate][$FinalPriceData[$i][$IsnKey][$Startdate]['currency']]['exch_rate_per_usd']>0.0)
							$FinalPriceData[$i][$IsnKey][$Startdate]['exchangeRate'] = $TmpExRates[$Startdate][$FinalPriceData[$i][$IsnKey][$Startdate]['currency']]['exch_rate_per_usd'];
						else
							$FinalPriceData[$i][$IsnKey][$Startdate]['exchangeRate'] = 1.0;
					
						
						$FinalPriceData[$i][$IsnKey][$Startdate]['isin'] = $IsnKey;
						
						
						
					} else {
							
							$dayBefore  =  date( 'Y-m-d', strtotime( $Startdate . ' -1 day' ) );
							$daybeforePrice  = $FinalPriceData[$i][$IsnKey][$dayBefore]['price'];
							$FinalPriceData[$i][$IsnKey][$Startdate]['price'] = $daybeforePrice;
							$FinalPriceData[$i][$IsnKey][$Startdate]['currency'] = $FinalPriceData[$i][$IsnKey][$dayBefore]['currency'];
							
							
							$FinalPriceData[$i][$IsnKey][$Startdate]['splitfactor'] = 1;
							$FinalPriceData[$i][$IsnKey][$Startdate]['dividend'] 	= 0;							
							$FinalPriceData[$i][$IsnKey][$Startdate]['spinoff'] 	= 0;
											
												
							
							if($TmpExRates[$Startdate][$FinalPriceData[$i][$IsnKey][$Startdate]['currency']]['exch_rate_per_usd']>0.0)
								$FinalPriceData[$i][$IsnKey][$Startdate]['exchangeRate'] = $TmpExRates[$Startdate][$FinalPriceData[$i][$IsnKey][$Startdate]['currency']]['exch_rate_per_usd'];
							else 
								$FinalPriceData[$i][$IsnKey][$Startdate]['exchangeRate'] = 1.0;
							
							$FinalPriceData[$i][$IsnKey][$Startdate]['isin'] = $IsnKey;
							
							
					}
						$FinalPriceData[$i][$IsnKey][$Startdate]['dividendUSD'] = $FinalPriceData[$i][$IsnKey][$Startdate]['dividend'] / $FinalPriceData[$i][$IsnKey][$Startdate]['exchangeRate'];
						$FinalPriceData[$i][$IsnKey][$Startdate]['DivSpinOfUSD'] = $FinalPriceData[$i][$IsnKey][$Startdate]['dividendUSD'] * $FinalPriceData[$i][$IsnKey][$Startdate]['spinoff'];
						$FinalPriceData[$i][$IsnKey][$Startdate]['DivExSpinOfUSD'] = $FinalPriceData[$i][$IsnKey][$Startdate]['dividendUSD'] -  $FinalPriceData[$i][$IsnKey][$Startdate]['DivSpinOfUSD'];
						
						$FinalPriceData[$i][$IsnKey][$Startdate]['newChangedPriceUSD'] = round( $FinalPriceData[$i][$IsnKey][$Startdate]['price'] /  $FinalPriceData[$i][$IsnKey][$Startdate]['exchangeRate'],7, PHP_ROUND_HALF_UP);
							
					$Startdate = date( 'Y-m-d', strtotime( $Startdate . ' +1 day' ) );
				}
				
			}			
			
		}
		
		unset($TmpDividendRecords);
		unset($TmpSplitsRecords);
		unset($TmpExRates);
		unset($DataTmpPrice);
					
		
		//echo "Price Data : <pre>";
		//print_r($FinalPriceData); 
		//echo "</pre>";
		//die;
		$NoOfShares = array();
		for($prd = 0; $prd < $period; $prd++) { 
			
			$prdStartDate = date( 'Y-m-d', strtotime( $_POST['StartDate'][$prd]));			
			
			for($chkISN = 0; $chkISN < count($securities[$prd]); $chkISN++) {
				$TmpSecuritiesISN = $securities[$prd][$chkISN];
				$weight = $SecuritiesWeightJSON[$prd][$TmpSecuritiesISN];
		
				$priceOfPrdFirstDay = $FinalPriceData[$prd][$TmpSecuritiesISN][$prdStartDate]['newChangedPriceUSD'];
				
				if($priceOfPrdFirstDay	>	0)
					$Shares	= ( 100000 * ( $weight / 100 ) ) / $priceOfPrdFirstDay;
				else {
					$Shares	= 0 ; 						
				}					
				
				$NoOfShares[$prd][$prdStartDate][$TmpSecuritiesISN] 		= round( $Shares,7,PHP_ROUND_HALF_UP);
							
			}	
		}
		
		echo "Securities with their Weight : <pre>";
		print_r($SecuritiesWeightJSON); 
		echo "</pre>";
		
		
		echo "No Of Shares  Data : <pre>";
		print_r($NoOfShares); 
		echo "</pre>";
		die;
		
		
		$srNo = 0;
		
		for($i=0;$i<count( $FinalPriceData);$i++) {
			$showPRD = $i + 1; 
			?>
			<div class="row">
				<div class="col-lg-12 col-xs-12"><label><?php echo "###########################Data of period $showPRD###########################"; ?></label></div>
			</div>
			<div class="row">					
					<div class="col-lg-2 col-xs-2"><label>Security ISN</label></div>
					<div class="col-lg-1 col-xs-1"><label>Currency</label></div>
					<div class="col-lg-2 col-xs-2"><label>Date (MM/DD/YYYY)</label></div>
					<div class="col-lg-1 col-xs-1"><label>Price</label></div>
					<div class="col-lg-2 col-xs-2"><label>Dividend</label></div>
					<div class="col-lg-1 col-xs-1"><label>Spin Off</label></div>
					<div class="col-lg-1 col-xs-1"><label>Split Factor</label></div>
					<div class="col-lg-2 col-xs-2"><label>Excange Rate</label></div>					
			</div>
			<?php
			foreach($FinalPriceData[$i] as $IsnKey =>$data) {
				
				echo '<div class="row"><div class="col-lg-12 col-xs-12"><label>*************************Data of '.$IsnKey.' Start**************************</label></div></div>';
				
				foreach($FinalPriceData[$i][$IsnKey] as $dateKey =>$Record) {
				
			 
				$securityISN 		= $IsnKey;
				$dateToShow 		= date( 'm/d/Y', strtotime( $dateKey) );
				$price 				= $Record['price'];
				$currency 			= $Record['currency'];
				$dividend 			= $Record['dividend'];
				$splitfactor 		= $Record['splitfactor'];
				$spinoff 			= $Record['spinoff'];
				$exchangeRate 		= $Record['exchangeRate'];
				$srNo++;
			
				echo '<div class="row">';
				echo '<div class="col-lg-1 col-xs-1">'.$srNo.'</div>';					
				echo '<div class="col-lg-2 col-xs-2">'.$securityISN.'</div>';
				echo '<div class="col-lg-1 col-xs-1">'.$currency.'</div>';
				echo '<div class="col-lg-2 col-xs-2">'.$dateToShow.'</div>';
				echo '<div class="col-lg-1 col-xs-1">'.number_format($price, 3).'</div>';
				echo '<div class="col-lg-1 col-xs-1">'.$dividend.'</div>';
				echo '<div class="col-lg-1 col-xs-1">'.$spinoff.'</div>';
				echo '<div class="col-lg-1 col-xs-1">'.$splitfactor.'</div>';
				echo '<div class="col-lg-2 col-xs-2">'.number_format($exchangeRate,3).'</div>';			
				echo '</div>';
				}
				
				echo '<div class="row"><div class="col-lg-12 col-xs-12"><label>*************************Data of '.$IsnKey.' End**************************"</label></div></div>';
				
			}
		}	
		?>
	</div>


<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js"></script>
<script src="http://localhost/backtestengine/plugins/daterangepicker/daterangepicker.js"></script>
<!-- datepicker -->
<script src="http://localhost/backtestengine/plugins/datepicker/bootstrap-datepicker.js"></script>

<?php require_once("footer.php"); ?>
