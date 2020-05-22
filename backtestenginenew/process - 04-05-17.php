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


$Adj0 = 0; 
$Adj1 = 0;

if($_POST['spinoff']) {
	$Adj0 = 1;
}

if($_POST['dividend']) {
	$Adj1 = 1;
} 

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

$InvestmentValueP	= array();
$InvestmentValueT	= array();
$IndexValueP 		= array();
$IndexValueT 		= array();
$DivisorP 			= array();
$DivisorT 			= array();
$cnt = 0; 
foreach($_POST['StartDate']  as $date) {	
	$Startdate 						= date( 'Y-m-d', strtotime( $date) );
	$InvestmentValueP[$cnt][$Startdate]	= 100000;
	$InvestmentValueT[$cnt][$Startdate]	= 100000;
	$IndexValueP[$cnt][$Startdate] 		= 1000;
	$IndexValueT[$cnt][$Startdate] 		= 1000;
	$DivisorP[$cnt][$Startdate] 		= 100;
	$DivisorT[$cnt][$Startdate] 		= 100;
	$cnt++;
}
?>
	<div class="container main-body">	
		<div class="row">
				<div class="col-lg-6 col-xs-6"><label></label></div>
				<div class="col-lg-6 col-xs-6"><a class="btn btn-primary" href="calculations.php">New Calculation </a></div>
			</div>
		<div class="row" id="resultDiv"> &nbsp </div>
		
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
						
						$TmpDividendRecords[$prd][$Divcount]['dividend'] 	= $record['p_divs_pd'];
						$TmpDividendRecords[$prd][$Divcount]['date'] 		= date( 'Y-m-d', strtotime($DBdatArray['date']) );
						$TmpDividendRecords[$prd][$Divcount]['isin'] 		= $record['isin'];
						
						
						$Divcount++;
					} 
					
				} else {				
					$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['dividend'] 	= $record['p_divs_pd'];
					$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['spinoff'] 	= $record['p_divs_s_spinoff'];
					
					$TmpDividendRecords[$prd][$Divcount]['dividend'] 	= $record['p_divs_pd'];
					$TmpDividendRecords[$prd][$Divcount]['date'] 		= date( 'Y-m-d', strtotime($DBdatArray['date']) );
					$TmpDividendRecords[$prd][$Divcount]['isin'] 		= $record['isin'];
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
						
						$TmpSplitsRecords[$prd][$Sptcount]['split'] 	= $record['p_split_factor'];
						$TmpSplitsRecords[$prd][$Sptcount]['date'] 		= date( 'Y-m-d', strtotime($DBdatArray['date']) );
						$TmpSplitsRecords[$prd][$Sptcount]['isin'] 		= $record['isin'];
						$Sptcount++;
					} 
					
				} else {
					$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['splitfactor'] 	= $record['p_split_factor'];
					$TmpSplitsRecords[$prd][$Sptcount]['split'] 	= $record['p_split_factor'];
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
		
		
		$NoOfShares 			= array();
		$NoOfSharesOnDate 		= array();
		$FinalPriceData 		= array();
		$TmpInvestmentValuesPk 	= array();
		$TmpDivisorPk 			= array();
		$TmpInvestmentValuesTk 	= array();
		$TmpDivisorTk 			= array();
		
		for($i=0;$i<count( $DataTmpPrice);$i++) {
			foreach($DataTmpPrice[$i] as $IsnKey =>$data) {
				
				$Startdate =  date( 'Y-m-d', strtotime( $_POST['StartDate'][$i] ) );				
				$EndDate   =  date( 'Y-m-d', strtotime( $_POST['EndDate'][$i] ) );
				
				$dateCounter = 0;
				$NoOfSharesOnDate[$Startdate] = 0;
				
				
				
				while($Startdate <= $EndDate) {
					if (array_key_exists($Startdate,$DataTmpPrice[$i][$IsnKey])) {
						
						
						
						
						if($DataTmpPrice[$i][$IsnKey][$Startdate]['price']) {  
							$FinalPriceData[$i][$IsnKey][$Startdate]['price']	=  $DataTmpPrice[$i][$IsnKey][$Startdate]['price'];
						} else  {
							$dayBefore  =  date( 'Y-m-d', strtotime( $Startdate . ' -1 day' ) );
							$FinalPriceData[$i][$IsnKey][$Startdate]['price'] = $FinalPriceData[$i][$IsnKey][$dayBefore]['price'];
						}
					
						
						
						
						$FinalPriceData[$i][$IsnKey][$Startdate]['currency']= $DataTmpPrice[$i][$IsnKey][$Startdate]['currency'];
						
						if (!array_key_exists('splitfactor',$DataTmpPrice[$i][$IsnKey][$Startdate])) {
							$FinalPriceData[$i][$IsnKey][$Startdate]['splitfactor'] = 1;
						} else {
							$FinalPriceData[$i][$IsnKey][$Startdate]['splitfactor'] = $DataTmpPrice[$i][$IsnKey][$Startdate]['splitfactor'];
						}
						
						if (!array_key_exists('dividend',$DataTmpPrice[$i][$IsnKey][$Startdate])) {
							$FinalPriceData[$i][$IsnKey][$Startdate]['dividend'] = 0;							
						} else {
							$FinalPriceData[$i][$IsnKey][$Startdate]['dividend'] = $DataTmpPrice[$i][$IsnKey][$Startdate]['dividend'];
						}
						
						if (!array_key_exists('spinoff',$DataTmpPrice[$i][$IsnKey][$Startdate])) {
							$FinalPriceData[$i][$IsnKey][$Startdate]['spinoff'] = 0;
						} else {
							$FinalPriceData[$i][$IsnKey][$Startdate]['spinoff'] = $DataTmpPrice[$i][$IsnKey][$Startdate]['spinoff'];
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
							
							 if($FinalPriceData[$i][$IsnKey][$Startdate]['price']==0 || $FinalPriceData[$i][$IsnKey][$Startdate]['price']=="") {
							$dayBefore  =  date( 'Y-m-d', strtotime( $Startdate . ' -2 day' ) );
							$daybeforePrice  = $FinalPriceData[$i][$IsnKey][$dayBefore]['price'];
							$FinalPriceData[$i][$IsnKey][$Startdate]['price'] = $daybeforePrice;
							$FinalPriceData[$i][$IsnKey][$Startdate]['currency'] = $FinalPriceData[$i][$IsnKey][$dayBefore]['currency'];
						 }
						
							
							$FinalPriceData[$i][$IsnKey][$Startdate]['splitfactor'] = 1;
							$FinalPriceData[$i][$IsnKey][$Startdate]['dividend'] 	= 0;							
							$FinalPriceData[$i][$IsnKey][$Startdate]['spinoff'] 	= 0;
											
											
							
							if($TmpExRates[$Startdate][$FinalPriceData[$i][$IsnKey][$Startdate]['currency']]['exch_rate_per_usd']) {  
								$FinalPriceData[$i][$IsnKey][$Startdate]['exchangeRate']	=  $TmpExRates[$Startdate][$FinalPriceData[$i][$IsnKey][$Startdate]['currency']]['exch_rate_per_usd'];
							} else  {
								$dayBefore  =  date( 'Y-m-d', strtotime( $Startdate . ' -1 day' ) );
								$FinalPriceData[$i][$IsnKey][$Startdate]['exchangeRate'] =$TmpExRates[$Startdate][$FinalPriceData[$i][$IsnKey][$dayBefore]['currency']]['exch_rate_per_usd'];
							}
							
							
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
						
						
						
						/* Start  Calculation to get No Of Shares each ISIN of Every Date */ 
						if($dateCounter	==	0) {
							$weight = $SecuritiesWeightJSON[$i][$IsnKey];

							$priceOfPrdFirstDay = $FinalPriceData[$i][$IsnKey][$Startdate]['newChangedPriceUSD'];

							if($priceOfPrdFirstDay	>	0)
								$Shares	= ( 100000 * ( $weight / 100 ) ) / $priceOfPrdFirstDay;
							else {
								$Shares	= 0 ; 						
							}					

							$NoOfShares[$i][$Startdate][$IsnKey] 		= round( $Shares,13,PHP_ROUND_HALF_UP);
							$FinalPriceData[$i][$IsnKey][$Startdate]['NoOfShares'] =  round( $Shares,13,PHP_ROUND_HALF_UP);

						} else 	{
								
							
							$date1DayBefore = date( 'Y-m-d', strtotime( $Startdate . ' -1 day' ) );
						$NoOfShares[$i][$Startdate][$IsnKey] = round( ( ( $NoOfShares[$i][$date1DayBefore][$IsnKey] + ($Adj0 * $FinalPriceData[$i][$IsnKey][$Startdate]['DivSpinOfUSD'] *  $NoOfShares[$i][$date1DayBefore][$IsnKey] / $FinalPriceData[$i][$IsnKey][$Startdate]['newChangedPriceUSD'] ) + ($Adj1 * $FinalPriceData[$i][$IsnKey][$Startdate]['DivExSpinOfUSD'] *  $NoOfShares[$i][$date1DayBefore][$IsnKey] / $FinalPriceData[$i][$IsnKey][$Startdate]['newChangedPriceUSD'] ) ) / $FinalPriceData[$i][$IsnKey][$Startdate]['splitfactor'] ) , 13,PHP_ROUND_HALF_UP);
							
							$FinalPriceData[$i][$IsnKey][$Startdate]['NoOfShares'] = $NoOfShares[$i][$Startdate][$IsnKey]; 
							
							
							
						}
						$dateCounter++;
						
						/*  End Calculation to get No Of Shares each ISIN of Every Date */ 
						
						/* Start Calculation for InvestmentValuesPk */ 
						
						$TmpInvestmentValuesPk[$i][$Startdate][$IsnKey]['PK']	= $FinalPriceData[$i][$IsnKey][$Startdate]['newChangedPriceUSD'];
						$TmpInvestmentValuesPk[$i][$Startdate][$IsnKey]['NK'] 	= $NoOfShares[$i][$Startdate][$IsnKey];
						
						
						$TmpDivisorPk[$i][$Startdate][$IsnKey]['Spin'] 			= $FinalPriceData[$i][$IsnKey][$Startdate]['DivSpinOfUSD'];
						$TmpDivisorPk[$i][$Startdate][$IsnKey]['NK'] 			= $NoOfShares[$i][$Startdate][$IsnKey];
						$TmpDivisorPk[$i][$Startdate][$IsnKey]['price'] 		= $FinalPriceData[$i][$IsnKey][$Startdate]['newChangedPriceUSD'];
						$TmpDivisorPk[$i][$Startdate][$IsnKey]['split'] 		= $FinalPriceData[$i][$IsnKey][$Startdate]['splitfactor'];
						$TmpDivisorPk[$i][$Startdate][$IsnKey]['dividendUSD'] 	= $FinalPriceData[$i][$IsnKey][$Startdate]['dividendUSD'];
						
											
						/* End Calculation for InvestmentValuesPk */ 
						
						$NoOfSharesOnDate[$Startdate] = $NoOfSharesOnDate[$Startdate] + $NoOfShares[$i][$Startdate][$IsnKey];							
						$Startdate = date( 'Y-m-d', strtotime( $Startdate . ' +1 day' ) );
				}
				
			}			
			
		}
		
		echo "<pre>";
		print_r($FinalPriceData);
		die;
		unset($TmpDividendRecords);
		unset($TmpSplitsRecords);
		unset($TmpExRates);
		unset($DataTmpPrice);
		
	
		
		/* Start Calculation for InvestmentValuesPk */ 
		$InvestmentValuesPk = array();
		for($p=0;$p < count($TmpInvestmentValuesPk);$p++) {
			foreach($TmpInvestmentValuesPk[$p] as $keydts => $DateValue) {
				$sum = 0.0;
				foreach($DateValue as $keyISIN => $DataISIN) {
					$sum = $sum + ( $DataISIN['PK'] * $DataISIN['NK'] );
				}
				$InvestmentValuesPk[$p][$keydts] = round($sum,13,PHP_ROUND_HALF_UP); 
			}
			
		}
		
		$InvestmentValuesTk = $InvestmentValuesPk;
		unset($TmpInvestmentValuesPk);
		/* End Calculation for InvestmentValuesPk */ 
		
		
		$tmpSumOfSharesDividend = array();
		$tmpSumOfSharesPrice 	= array();
		$tmpSumOfSharesDividendUSD 	= array();
		
		
		for($p=0;$p < count($TmpDivisorPk);$p++) {
			$ctn = 0 ;
			foreach($TmpDivisorPk[$p] as $keydts => $DateValue) {
				$sum1 = 0.0;	
				$sum2 = 0.0;
				$sum3 = 0.0;				
				$ctn++;
				$daybefore = date( 'Y-m-d', strtotime( $keydts . ' -1 day' ) );
				
				if($ctn > 1) { 				
					foreach($DateValue as $keyISIN => $DataISIN) { 
						$sum1 = $sum1 + ( $DataISIN['Spin'] * $DataISIN['NK'] ) ;
							
						if($DataISIN['split'] > 0) {
							if($TmpDivisorPk[$p][$daybefore][$keyISIN]['price']>0) {
								$sum2 = $sum2 + ( ( $TmpDivisorPk[$p][$daybefore][$keyISIN]['price'] * $DataISIN['NK'] ) * $DataISIN['split'] ) ;
							}							
						} 
						$sum3 = $sum3 + ( $DataISIN['dividendUSD'] * $DataISIN['NK'] ) ;
					} 					
					
				}
				
				$tmpSumOfSharesDividend[$p][$keydts] 	= round($sum1,13,PHP_ROUND_HALF_UP); 
				$tmpSumOfSharesPrice[$p][$keydts] 		= round($sum2,13,PHP_ROUND_HALF_UP);
				$tmpSumOfSharesDividendUSD[$p][$keydts] = round($sum3,13,PHP_ROUND_HALF_UP);
				
				
			}
			
		}
	
		
		unset($TmpDivisorPk);
		
		for($p=0;$p < count($tmpSumOfSharesPrice);$p++) {
			$count = 0;
			foreach($tmpSumOfSharesPrice[$p] as $keydts => $DateValue) {							 
				$count++;
				if($count>=2) { 
					$daybefore = date( 'Y-m-d', strtotime( $keydts . ' -1 day' ) );
					if($IndexValueP[$p][$daybefore]>0) {
						
					$a 	= $tmpSumOfSharesDividend[$p][$keydts] / $IndexValueP[$p][$daybefore];
					$b	= $InvestmentValuesPk[$p][$daybefore] -  $tmpSumOfSharesPrice[$p][$keydts];
			
					$c 	= $b / $IndexValueP[$p][$daybefore] ;
					$cc = $b / $IndexValueT[$p][$daybefore]; 
					
					$dd 	= $tmpSumOfSharesDividendUSD[$p][$keydts] / $IndexValueT[$p][$daybefore];				
					
					$DivisorP[$p][$keydts] = $DivisorP[$p][$daybefore] - $a - $c ;
					$DivisorT[$p][$keydts] = $DivisorT[$p][$daybefore] - $dd - $cc ;					
					
					} else { 
						$DivisorP[$p][$keydts]  = $DivisorP[$p][$daybefore];
						$DivisorT[$p][$keydts]  = $DivisorT[$p][$daybefore];
					}
					
					$DivisorP[$p][$keydts] 		= round($DivisorP[$p][$keydts],13,PHP_ROUND_HALF_UP);
					$DivisorT[$p][$keydts] 		= round($DivisorT[$p][$keydts],13,PHP_ROUND_HALF_UP);					
					
					
					
					if($DivisorP[$p][$keydts]>0) {
						
						$d = $InvestmentValuesPk[$p][$keydts] / $DivisorP[$p][$keydts] ; 						
						$IndexValueP[$p][$keydts]  	= round( $d ,13,PHP_ROUND_HALF_UP);
						
					} else {
							$IndexValueP[$p][$keydts] = 0.00;
					}
					
					if($DivisorT[$p][$keydts]>0) {
						
						$ddd = $InvestmentValuesPk[$p][$keydts] / $DivisorT[$p][$keydts] ; 						
						$IndexValueT[$p][$keydts]  	= round( $ddd ,13,PHP_ROUND_HALF_UP);
						
					} else {
							$IndexValueT[$p][$keydts] = 0.00;
					}
					
					//echo $keydts."=>"; 
					//echo $IndexValueP[$p][$daybefore]; echo "<br/>";
					
					if($p >= 1) {
							
							// $EndDateofPrdPrevious 		= date( 'Y-m-d', strtotime( $_POST['EndDate'][$p-1] ) );	
							
							// $IndexValueP[$p][$keydts] 	= $IndexValueP[$p][$keydts] * $IndexValueP[$p-1][$EndDateofPrdPrevious] / 1000;
							// $IndexValueT[$p][$keydts] 	= $IndexValueT[$p][$keydts] * $IndexValueT[$p-1][$EndDateofPrdPrevious] / 1000;
							// $IndexValueT[$p][$keydts]  	= round( $IndexValueP[$p][$keydts] ,13,PHP_ROUND_HALF_UP);
							// $IndexValueT[$p][$keydts]  	= round( $IndexValueT[$p][$keydts] ,13,PHP_ROUND_HALF_UP);
					}
					
				} else if($count == 1 && $p >= 1) {					
					
					// $EndDateofPrdPrevious 						= date( 'Y-m-d', strtotime( $_POST['EndDate'][$p-1] ) );
					// $IndexValueP[$p][$keydts] 					= $IndexValueP[$p-1][$EndDateofPrdPrevious];
					// $IndexValueP[$p][$keydts] 					= $IndexValueP[$p-1][$EndDateofPrdPrevious];					
					// $DivisorP[$p][$keydts] 						= $DivisorP[$p-1][$EndDateofPrdPrevious];
					// $DivisorT[$p][$keydts]						= $DivisorT[$p-1][$EndDateofPrdPrevious];
					
									
					// $IndexValueP[$p][$keydts] 	= $IndexValueP[$p][$keydts] * $IndexValueP[$p-1][$EndDateofPrdPrevious] / 1000;
					// $IndexValueT[$p][$keydts] 	= $IndexValueT[$p][$keydts] * $IndexValueT[$p-1][$EndDateofPrdPrevious] / 1000;
					// $IndexValueP[$p][$keydts]  	= round( $IndexValueP[$p][$keydts] ,13,PHP_ROUND_HALF_UP);
					// $IndexValueT[$p][$keydts]  	= round( $IndexValueT[$p][$keydts] ,13,PHP_ROUND_HALF_UP);
					
				}
			}
			
		}
		
		
		/*
		echo "DivisorP Data : <pre>";
		print_r($DivisorP); 
		echo "</pre>";
		die;
		
		echo "IndexValueT Data : <pre>";
		print_r($IndexValueP); 
		echo "</pre>"; die;
		

		$fp = fopen("php://output", "w");
		fputcsv ($fp, $header, "\t");
		foreach($array as $row){
		fputcsv($fp, $row, "\t");
		}
		fclose($fp);
		*/
		$title = date('Y-m-d-').time().".csv";
		$filename =dirname(__FILE__)."/csvfiles/".$title;		
		$srNo = 0;	
		$file =  fopen($filename, 'w');
		$header = array("Date","Index PR","Index TR");
		ob_start();
		fputcsv ($file, $header, "\t");		
		
		for($i=0;$i<count( $IndexValueP);$i++) {
				
			?>
			
			<div class="row">
					<div class="col-lg-1 col-xs-1"><label>SR No.</label></div>			
					<div class="col-lg-3 col-xs-3"><label>Date</label></div>
					<div class="col-lg-4 col-xs-4"><label>Index PR</label></div>
					<div class="col-lg-4 col-xs-4"><label>Index TR</label></div>
										
			</div>
			<?php
			foreach($IndexValueP[$i] as $Date =>$indexValue) {
				
				$indexValueTR =$IndexValueT[$i][$Date] ;
				$srNo++;
				
				$fields = array($Date,$indexValue,$indexValueTR);
				fputcsv($file,$fields);
			
				echo '<div class="row">';
				echo '<div class="col-lg-1 col-xs-1">'.$srNo.'</div>';					
				echo '<div class="col-lg-3 col-xs-3">'.$Date.'</div>';
				echo '<div class="col-lg-4 col-xs-4">'.$indexValue.'</div>';
				echo '<div class="col-lg-4 col-xs-4">'.$indexValueTR.'</div>';				
				echo '</div>';
				}
		}
		fclose($file);

		if($srNo) {						
		?>
		<div class="row">
					<a target="_blank" class="btn btn-primary" href="http://localhost/backtestengine/download.php?file=<?php echo $title?>" title="<?php echo $title?>">Download file</a>
										
			</div>
		<?php } ?>	
	</div>


<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js"></script>
<script src="http://localhost/backtestengine/plugins/daterangepicker/daterangepicker.js"></script>
<!-- datepicker -->
<script src="http://localhost/backtestengine/plugins/datepicker/bootstrap-datepicker.js"></script>

<?php require_once("footer.php"); ?>
