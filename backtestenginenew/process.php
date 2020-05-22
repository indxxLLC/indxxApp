<?php

require_once("header.php");




$messgae 		= ""; 
$warrning 		= "";  
$buttonFlag 	= false;  
$securities 	= array();
$currency 		= 'USD'; 
$showPRD 		= 0; 
$url 			= '';
$title 			= '';

if($_POST['SecuritiesWeightJSON'] && $_POST['StartDate'] && $_POST['EndDate'] && $_POST['currency']) {
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
$NotTrading  = array(); 
$NottradContiDays = array();

$TmpSecuritiesWeightJSON = (array) JSON_decode($_POST['SecuritiesWeightJSON']);
foreach($TmpSecuritiesWeightJSON as $tmpval) {
	$SecuritiesWeightJSON[] = (array) $tmpval;
}
unset($TmpSecuritiesWeightJSON);

$InvestmentValueP	= array();
$InvestmentValueT	= array();
$InvestmentValueN	= array();
$IndexValueP 		= array();
$IndexValueT 		= array();
$IndexValueN 		= array();
$DivisorP 			= array();
$DivisorT 			= array();
$DivisorN 			= array();
$V1			        = array();
$V2			        = array();
$V3			        = array();
$cnt = 0; 
$TAXDATA	= array();
	$taxqry = " SELECT ba.tax ,ca.iso_country from FDS_DataFeeds.dbo.tax_rate ba left join FDS_DataFeeds.ref_v2.country_map ca on ba.Country=ca.country_desc ";
				
				//echo $qry;
				//exit;
				
				$taxres = sqlsrv_query( $connection, $taxqry );
				
				
					
				while( $record = sqlsrv_fetch_array( $taxres, SQLSRV_FETCH_ASSOC) ) {
					$TAXDATA[$record['iso_country']]=$record['tax'];
				}

//print_r($TAXDATA);
//exit;


foreach($_POST['StartDate']  as $date) {	
	$Startdate 						= date( 'Y-m-d', strtotime( $date) );
	$InvestmentValueP[$cnt][$Startdate]	= 100000;
	$InvestmentValueT[$cnt][$Startdate]	= 100000;
	$InvestmentValueN[$cnt][$Startdate]	= 100000;
	$IndexValueP[$cnt][$Startdate] 		= 1000;
	$IndexValueT[$cnt][$Startdate] 		= 1000;
	$IndexValueN[$cnt][$Startdate] 		= 1000;
	$newindexP[$cnt][$Startdate] 		= 1000;
	$newindexT[$cnt][$Startdate] 		= 1000;
	$newindexN[$cnt][$Startdate] 		= 1000;
	$DivisorP[$cnt][$Startdate] 		= 100;
	$DivisorT[$cnt][$Startdate] 		= 100;
	$DivisorN[$cnt][$Startdate] 		= 100;
	$cnt++;
}
?>
	<div class="container main-body">	
		<div class="row">
				<div class="col-lg-6 col-xs-6"><a target="_blank" class="btn btn-primary" id="downloadhref" href="#" title="">Download Index Values file</a></div>
				<div class="col-lg-6 col-xs-6"><a target="_blank" class="btn btn-primary" id="downloadhref2" href="#" title="">Download Portfolio Output file</a></div>
				<div class="col-lg-6 col-xs-6"><a class="btn btn-primary" href="calculations.php">New Calculation </a></div>
			</div>
		
		
		<div class="row" id="resultDiv"> </div>
		
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
			$qry .= " ON PRC.fs_perm_sec_id =CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
			$qry .= " WHERE ISN.isin in  (".$TmpSecuritiesISN.")  AND  PRC.date between '".$StartDateDB."' and '".$EndDateDB ."'";						
			$qry .= " ORDER BY ISN.isin, PRC.date ";
			
			//echo $qry;
			//exit;
			
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
						$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['country']=explode("-",$record['fs_perm_sec_id'])[2];
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
					$DataTmpPrice[$prd][$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['country']=explode("-",$record['fs_perm_sec_id'])[2];
				
					$AllisinBasicCurrencey[$prd][$count] = $record['currency'];	
					$count++;
				}
				
				
				
				
			}
			//print_r($DataTmpPrice);
			//exit;
			$qry = "SELECT DIV.p_divs_pd , DIV.currency,DIV.date , DIV.p_divs_s_spinoff, DIV.fs_perm_sec_id,ISN.isin"; 
			$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_dividends  AS DIV"; 
			$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
			$qry .= " ON DIV.fs_perm_sec_id = CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
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
			$qry .= " ON SPT.fs_perm_sec_id = CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
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
							$NotTrading[$IsnKey][$Startdate] = 1;
						}
					
						
						
						
						$FinalPriceData[$i][$IsnKey][$Startdate]['currency']= $DataTmpPrice[$i][$IsnKey][$Startdate]['currency'];
						$FinalPriceData[$i][$IsnKey][$Startdate]['country']= $DataTmpPrice[$i][$IsnKey][$Startdate]['country'];
							$FinalPriceData[$i][$IsnKey][$Startdate]['tax']= $TAXDATA[$DataTmpPrice[$i][$IsnKey][$Startdate]['country']];
						
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
							$FinalPriceData[$i][$IsnKey][$Startdate]['country']= $FinalPriceData[$i][$IsnKey][$dayBefore]['country'];
							$FinalPriceData[$i][$IsnKey][$Startdate]['tax']= $TAXDATA[$FinalPriceData[$i][$IsnKey][$dayBefore]['country']];
							$NotTrading[$IsnKey][$Startdate] = 1;
							
							if($FinalPriceData[$i][$IsnKey][$Startdate]['price']==0 || $FinalPriceData[$i][$IsnKey][$Startdate]['price']=="") {
								$NotTrading[$IsnKey][$dayBefore] = 1;								
								
							$dayBefore  =  date( 'Y-m-d', strtotime( $Startdate . ' -2 day' ) );
							$daybeforePrice  = $FinalPriceData[$i][$IsnKey][$dayBefore]['price'];
							$EnddateOfpreviousPrd  =  date( 'Y-m-d', strtotime( $EndDate[$i-1]) );
							if($daybeforePrice) {
								$FinalPriceData[$i][$IsnKey][$Startdate]['price'] = $daybeforePrice;
								$FinalPriceData[$i][$IsnKey][$Startdate]['currency'] = $FinalPriceData[$i][$IsnKey][$dayBefore]['currency'];								
							} else if($dayBefore==$EnddateOfpreviousPrd) {
								$FinalPriceData[$i][$IsnKey][$Startdate]['price'] = $FinalPriceData[$i-1][$IsnKey][$EnddateOfpreviousPrd]['price'];
								$FinalPriceData[$i][$IsnKey][$Startdate]['currency'] = $FinalPriceData[$i-1][$IsnKey][$EnddateOfpreviousPrd]['currency'];
								$NotTrading[$IsnKey][date( 'Y-m-d', strtotime( $Startdate . ' -2 day' ) )] = 1;
							}
							
							
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
						$EnddateOfpreviousPrd  =  date( 'Y-m-d', strtotime( $_POST['EndDate'][$i-1]) );
						
						 if($FinalPriceData[$i][$IsnKey][$Startdate]['price'] == 0) {
						    $dateForDB = date('Y-m-d',strtotime($EnddateOfpreviousPrd));
							 $flagSecuritiesNotTradingOnFirDay = 0;
							$flagSecuritiesNotTradingOnThuDay = 0 ;
							$flagSecuritiesNotTradingOnMonDay = 0 ;
							$flagSecuritiesNotTradingOnTuesDay = 0 ;
							$Day = date('D',strtotime($dateForDB));
							$NotTrading[$IsnKey][$Startdate] = 1;
							
							$NewActualDate = $dateForDB;
							if($Day=="Sat") {
								$NewActualDate = date( 'Y-m-d', strtotime( $dateForDB . ' -1 day' ) );
								$NotTrading[$IsnKey][$NewActualDate] = 1;
							} else if($Day=="Sun") {
								$NewActualDate = date( 'Y-m-d', strtotime( $dateForDB . ' -2 day' ) );
								$NotTrading[$IsnKey][$NewActualDate] = 1;
							}
							$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
							$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
							$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
							$qry .= " ON PRC.fs_perm_sec_id = CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
							$qry .= " WHERE ISN.isin = '".$IsnKey."'  AND PRC.date = '".$NewActualDate."'"; 
							$stmt = sqlsrv_query( $connection, $qry , array(), array( "Scrollable" => SQLSRV_CURSOR_KEYSET ));  
							$TmpPricerecord = sqlsrv_fetch_array( $stmt, SQLSRV_FETCH_ASSOC);
							
							if(count($TmpPricerecord)>0) {
								$FinalPriceData[$i][$IsnKey][$Startdate]['price'] 			= $TmpPricerecord['p_price'];
								$FinalPriceData[$i][$IsnKey][$Startdate]['currency'] 		= $TmpPricerecord['currency'];	
								//FinalPriceData[$i][$IsnKey][$Startdate]['exchangeRate'] 	= $TmpPricerecord['exchangeRate'];
								
							} else  {
								$flagSecuritiesNotTradingOnFirDay++;
								$NotTrading[$IsnKey][$NewActualDate] = 1;
							}
							 
							 if($flagSecuritiesNotTradingOnFirDay>=1) {		
								$NewActualDate = date( 'Y-m-d', strtotime( $NewActualDate . ' -1 day' ) );	
								// check all securities are trading on 1 day (NewActualDate) before given date i.e $dateForDB
								
								$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
								$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
								$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
								$qry .= " ON PRC.fs_perm_sec_id = CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
								$qry .= " WHERE ISN.isin = '".$IsnKey."'  AND PRC.date = '".$NewActualDate."'";			
								
								$stmt = sqlsrv_query( $connection, $qry , array(), array( "Scrollable" => SQLSRV_CURSOR_KEYSET )); 
								$TmpPricerecord = sqlsrv_fetch_array( $stmt, SQLSRV_FETCH_ASSOC);
								if(count($TmpPricerecord)>0) {
									$FinalPriceData[$i][$IsnKey][$Startdate]['price'] 			=$TmpPricerecord['p_price'];
									$FinalPriceData[$i][$IsnKey][$Startdate]['currency'] 		= $TmpPricerecord['currency'];
									//FinalPriceData[$i][$IsnKey][$Startdate]['exchangeRate'] 	= $TmpPricerecord['exchangeRate'];
								
								} else  {
									$flagSecuritiesNotTradingOnThuDay++;
									$NotTrading[$IsnKey][$NewActualDate] = 1;
								}			
								
							 }
							 
							  if($flagSecuritiesNotTradingOnThuDay>=1) {		
								$NewActualDate = date( 'Y-m-d', strtotime( $NewActualDate . ' -1 day' ) );	
								// check all securities are trading on 1 day (NewActualDate) before given date i.e $dateForDB
								
								$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
								$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
								$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
								$qry .= " ON PRC.fs_perm_sec_id = CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
								$qry .= " WHERE ISN.isin = '".$IsnKey."'  AND PRC.date = '".$NewActualDate."'";			
								
								$stmt = sqlsrv_query( $connection, $qry , array(), array( "Scrollable" => SQLSRV_CURSOR_KEYSET )); 
								$TmpPricerecord = sqlsrv_fetch_array( $stmt, SQLSRV_FETCH_ASSOC);
								if(count($TmpPricerecord)>0) {
									$FinalPriceData[$i][$IsnKey][$Startdate]['price'] 			=$TmpPricerecord['p_price'];
									$FinalPriceData[$i][$IsnKey][$Startdate]['currency'] 		= $TmpPricerecord['currency'];
									//FinalPriceData[$i][$IsnKey][$Startdate]['exchangeRate'] 	= $TmpPricerecord['exchangeRate'];
								
								} else  {
									$flagSecuritiesNotTradingOnWedDay++;
									$NotTrading[$IsnKey][$NewActualDate] = 1;
								}			
								
							 }
							 
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
						$TmpDivisorPk[$i][$Startdate][$IsnKey]['ADJdividendUSD'] 	= $FinalPriceData[$i][$IsnKey][$Startdate]['dividendUSD']*(1-(str_replace("%","",$FinalPriceData[$i][$IsnKey][$Startdate]['tax'])/100));
							

							
						/* End Calculation for InvestmentValuesPk */ 
						
						$NoOfSharesOnDate[$Startdate] = $NoOfSharesOnDate[$Startdate] + $NoOfShares[$i][$Startdate][$IsnKey];	
						
						
						
						
						// check the current isin does have 5 days price continue
							//$fiveDates till start dates 
							
							$fiveDates = array(
												$Startdate,
												date( 'Y-m-d', strtotime( $Startdate . ' -1 day' ) ),
												date( 'Y-m-d', strtotime( $Startdate . ' -2 day' ) ),
												date( 'Y-m-d', strtotime( $Startdate . ' -3 day' ) ),
												date( 'Y-m-d', strtotime( $Startdate . ' -4 day' ) )
												);
							
							if(count($NotTrading[$IsnKey])>0) {
								
								foreach($fiveDates as $key =>$Fdate) {
									if($NotTrading[$IsnKey][$Fdate]) {
										$NottradContiDays[$IsnKey] =  $NottradContiDays[$IsnKey] + 1 ;
									}
								}
								
								if($NottradContiDays[$IsnKey] < 5) 
									$NottradContiDays[$IsnKey] = 0;
							}	
							
							
							
							 if($NottradContiDays[$IsnKey] >= 5) {
								 $NoOfShares[$i][date( 'Y-m-d', strtotime( $Startdate . ' -1 day' ) )][$IsnKey] = 0;
								 $NoOfShares[$i][date( 'Y-m-d', strtotime( $Startdate . ' -2 day' ) )][$IsnKey] = 0;
								 $NoOfShares[$i][date( 'Y-m-d', strtotime( $Startdate . ' -3 day' ) )][$IsnKey] = 0;
								 $NoOfShares[$i][date( 'Y-m-d', strtotime( $Startdate . ' -4 day' ) )][$IsnKey] = 0;								
								 $NoOfShares[$i][$Startdate][$IsnKey] = 0;
								
								 $FinalPriceData[$i][$IsnKey][date( 'Y-m-d', strtotime( $Startdate . ' -1 day' ) )]['NoOfShares'] = 0; 
								 $FinalPriceData[$i][$IsnKey][date( 'Y-m-d', strtotime( $Startdate . ' -2 day' ) )]['NoOfShares'] = 0; 
								 $FinalPriceData[$i][$IsnKey][date( 'Y-m-d', strtotime( $Startdate . ' -3 day' ) )]['NoOfShares'] = 0; 
								 $FinalPriceData[$i][$IsnKey][date( 'Y-m-d', strtotime( $Startdate . ' -4 day' ) )]['NoOfShares'] = 0; 								
								 $FinalPriceData[$i][$IsnKey][$Startdate]['NoOfShares'] = 0;								
							 }
						
							$Startdate = date( 'Y-m-d', strtotime( $Startdate . ' +1 day' ) );
						
				}
				
			}			
		
		
		}
		
		unset($TmpDividendRecords);
		unset($TmpSplitsRecords);
		unset($TmpExRates);
		unset($DataTmpPrice);
		/*echo "<pre>"; 
		print_r($TmpDivisorPk);
		echo "</pre>";
	*/
		
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
		$tmpSumOfSharesADJDividendUSD 	= array();
		
		
		for($p=0;$p < count($TmpDivisorPk);$p++) {
			$ctn = 0 ;
			foreach($TmpDivisorPk[$p] as $keydts => $DateValue) {
				$sum1 = 0.0;	
				$sum2 = 0.0;
				$sum3 = 0.0;
				$sum4 = 0.0;				
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
						$sum4 = $sum4 + ( $DataISIN['ADJdividendUSD'] * $DataISIN['NK'] ) ;
					} 					
					
				}
				
				$tmpSumOfSharesDividend[$p][$keydts] 	= round($sum1,13,PHP_ROUND_HALF_UP); 
				$tmpSumOfSharesPrice[$p][$keydts] 		= round($sum2,13,PHP_ROUND_HALF_UP);
				$tmpSumOfSharesDividendUSD[$p][$keydts] = round($sum3,13,PHP_ROUND_HALF_UP);
				$tmpSumOfSharesADJDividendUSD[$p][$keydts]=round($sum4,13,PHP_ROUND_HALF_UP);
			    
			
			}
			
		}
		/*echo "<pre>"; 
		print_r($tmpSumOfSharesDividendUSD);
		echo "</pre>";
		echo "<pre>"; 
		print_r($tmpSumOfSharesADJDividendUSD);
		echo "</pre>";
	*/
		//exit;
		
		unset($TmpDivisorPk);
		$factorPR = array();
		$factorPR[0] =  1;
		$factorTR = array();
		$factorTR[0] =  1;
		$factorNR = array();
		$factorNR[0] =  1;
		
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
					$ccc = $b / $IndexValueN[$p][$daybefore]; 
					
					$dd 	= $tmpSumOfSharesDividendUSD[$p][$keydts] / $IndexValueT[$p][$daybefore];				
					$dda 	= $tmpSumOfSharesADJDividendUSD[$p][$keydts] / $IndexValueN[$p][$daybefore];				
					
					$DivisorP[$p][$keydts] = $DivisorP[$p][$daybefore] - $a - $c ;
					$DivisorT[$p][$keydts] = $DivisorT[$p][$daybefore] - $dd - $cc ;
					$DivisorN[$p][$keydts] = $DivisorN[$p][$daybefore] - $dda - $ccc ;						
					$V2[$p][$keydts] = $dd;
					$V1[$p][$keydts] = $cc ;
					} else { 
						$DivisorP[$p][$keydts]  = $DivisorP[$p][$daybefore];
						$DivisorT[$p][$keydts]  = $DivisorT[$p][$daybefore];
						$DivisorN[$p][$keydts]  = $DivisorN[$p][$daybefore];
					}
					
					$DivisorP[$p][$keydts] 		= round($DivisorP[$p][$keydts],13,PHP_ROUND_HALF_UP);
					$DivisorT[$p][$keydts] 		= round($DivisorT[$p][$keydts],13,PHP_ROUND_HALF_UP);
					$DivisorN[$p][$keydts] 		= round($DivisorN[$p][$keydts],13,PHP_ROUND_HALF_UP);					
					
					
					
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
				
				if($DivisorN[$p][$keydts]>0) {
						
						$tt = $InvestmentValuesPk[$p][$keydts] / $DivisorN[$p][$keydts] ; 						
						$IndexValueN[$p][$keydts]  	= round( $tt ,13,PHP_ROUND_HALF_UP);
						
					} else {
							$IndexValueN[$p][$keydts] = 0.00;
					}
				
			$tday = $_POST['EndDate'][$p]; 
			$lastday = date( 'Y-m-d', strtotime( $tday ) );		
			$factorPR[$p+1] = $factorPR[$p] * $IndexValueP[$p][$lastday] / 1000;
			$factorTR[$p+1] = $factorTR[$p] * $IndexValueT[$p][$lastday] / 1000;
			$factorNR[$p+1] = $factorNR[$p] * $IndexValueN[$p][$lastday] / 1000;
			
			$newindexP[$p][$keydts] = 	round( $IndexValueP[$p][$keydts] * $factorPR[$p],13,PHP_ROUND_HALF_UP);
			$newindexT[$p][$keydts] =   	round( $IndexValueT[$p][$keydts] * $factorTR[$p] ,13,PHP_ROUND_HALF_UP);
			$newindexN[$p][$keydts] =   	round( $IndexValueN[$p][$keydts] * $factorNR[$p] ,13,PHP_ROUND_HALF_UP);
					
			//$IndexValueP[$p][$keydts]  	= round( $newindexP ,13,PHP_ROUND_HALF_UP);
			//$IndexValueT[$p][$keydts]  	= round( $newindexT ,13,PHP_ROUND_HALF_UP);
		
		
			//$newindexP = 	round( $IndexValueP[$p][$keydts] * $factorPR[$p],13,PHP_ROUND_HALF_UP);
				//	$newindexT =   	round( $IndexValueT[$p][$keydts] * $factorTR[$p] ,13,PHP_ROUND_HALF_UP);
					
				//	$IndexValueP[$p][$keydts]  	= round( $newindexP ,13,PHP_ROUND_HALF_UP);
				//	$IndexValueT[$p][$keydts]  	= round( $newindexT ,13,PHP_ROUND_HALF_UP);
					
					
				} 
			}
			
		
		
			
		}
		//echo "<pre>"; 
		//print_r($InvestmentValuesPk);
		//echo "</pre>";
		//echo "<pre>"; 
		//print_r($DivisorT);
		//echo "</pre>";
		//echo "<pre>"; 
		//print_r($V1);
		//echo "</pre>";
		//echo "<pre>"; 
		//print_r($V2);
		//echo "</pre>";
		//echo "<pre>"; 
		//print_r($FinalPriceData);
		//echo "</pre>";
	//	exit;
		
		$title2 = date('Y-m-d-').time()."_Constituants.csv";
		$filename =dirname(__FILE__)."/csvfiles/".$title2;		
		$srNo = 0;	
		$file =  fopen($filename, 'w');
		$titledate = 'Date';
		$titleindexpr = 'Index PR';
		$titleindextr = 'Index TR';
		$titleindexnr = 'Index NTR';
		$header = array("S.No.",$titledate,$titleindexpr,$titleindextr,$titleindexnr,"ISIN","Currency","Country","TAX","Close Price","Share","Exchange Rate","Weight PR","Weight TR","Weight NTR","Dividend"," Spin"," Splitfactor","DivisorPR","divisorTR","DivisorNTR","InvestmentValue","Price in USD");
		ob_start();
		fputcsv ($file, $header);		
		foreach($FinalPriceData as $k=> $isinData)
		{
			foreach($isinData as $isin=> $dates)
		{
			
		$i=0;
			foreach($dates as $date=> $data)
		{
			
			
			if($k>0 && $i==1)
			{$fields=	array(($k+1),$date,$newindexP[$k][$date],$newindexT[$k][$date],$newindexN[$k][$date],$isin,$data['currency'],$data['country'],$data['tax'],$data['price'],$data['NoOfShares'],$data['exchangeRate'],round((($data['NoOfShares']*$data['newChangedPriceUSD'])/($newindexP[$k][$date]*$DivisorP[$k][$date]))*($newindexP[$k][$date]/1000),13,PHP_ROUND_HALF_UP),
			round((($data['NoOfShares']*$data['newChangedPriceUSD'])/($newindexT[$k][$date]*$DivisorT[$k][$date]))*($newindexT[$k][$date]/1000),13,PHP_ROUND_HALF_UP),
			round((($data['NoOfShares']*$data['newChangedPriceUSD'])/($newindexN[$k][$date]*$DivisorN[$k][$date]))*($newindexN[$k][$date]/1000),13,PHP_ROUND_HALF_UP),$data['dividend'],$data['spinoff'],$data['splitfactor'],$DivisorP[$k][$date],$DivisorT[$k][$date],$DivisorN[$k][$date],$InvestmentValuesPk[$k][$date],$data['newChangedPriceUSD']);
				fputcsv($file,$fields);
			}else{
			$fields=	array(($k+1),$date,$newindexP[$k][$date],$newindexT[$k][$date],$newindexN[$k][$date],$isin,$data['currency'],$data['country'],$data['tax'],$data['price'],$data['NoOfShares'],$data['exchangeRate'],round(($data['NoOfShares']*$data['newChangedPriceUSD'])/($newindexP[$k][$date]*$DivisorP[$k][$date]),13,PHP_ROUND_HALF_UP),
			round(($data['NoOfShares']*$data['newChangedPriceUSD'])/($newindexT[$k][$date]*$DivisorT[$k][$date]),13,PHP_ROUND_HALF_UP),
			round(($data['NoOfShares']*$data['newChangedPriceUSD'])/($newindexN[$k][$date]*$DivisorN[$k][$date]),13,PHP_ROUND_HALF_UP),$data['dividend'],$data['spinoff'],$data['splitfactor'],$DivisorP[$k][$date],$DivisorT[$k][$date],$DivisorN[$k][$date],$InvestmentValuesPk[$k][$date],$data['newChangedPriceUSD']);
				fputcsv($file,$fields);
				
			}
		$i++;
		
		}
			
		}
			
		}
		fclose($file);
		
		?>
		<div class="row">
					<div class="col-lg-12 col-xs-12"><label>All Date's formats are MM/DD/YYYY </label></div>
					<div class="col-lg-12 col-xs-12"></div>
			</div>
			<div class="row">
					<div class="col-lg-1 col-xs-1"><label>SR No.</label></div>			
					<div class="col-lg-2 col-xs-2"><label>Date</label></div>
					<div class="col-lg-2 col-xs-2"><label>Index PR</label></div>
					<div class="col-lg-2 col-xs-2"><label>Index TR</label></div>
					<div class="col-lg-2 col-xs-2"><label>Index NTR</label></div>
										
			</div>
		<?php	
		$title = date('Y-m-d-').time().".csv";
		$filename =dirname(__FILE__)."/csvfiles/".$title;		
		$srNo = 0;	
		$file =  fopen($filename, 'w');
		$titledate = 'Date';
		$titleindexpr = 'Index PR';
		$titleindextr = 'Index TR';
		$titleindexnr = 'Index NTR';
		$header = array($titledate,$titleindexpr,$titleindextr,$titleindexnr);
		ob_start();
		fputcsv ($file, $header);		
		$html = '';
		for($i=0;$i<count( $IndexValueP);$i++) {
			$StartDate = $_POST['StartDate'][$i];
			$EndDate = $_POST['EndDate'][$i];
			$prdshow = $i + 1; 	
			?>
			
		<?php
			foreach($newindexP[$i] as $Date =>$indexValue) {
				
				$indexValueTR =$newindexT[$i][$Date] ;
				$indexValueNR =$newindexN[$i][$Date] ;
				$srNo++;
				
				if($srNo > 5 && $indexValue==1000) {
					$srNo--;
					continue;
				}
				
				$adate = date( 'm/d/Y', strtotime( $Date ) );
				$fields = array($adate,$indexValue,$indexValueTR,$indexValueNR);
				fputcsv($file,$fields);
				
				
			?>
			<div class="row">
			<div class="col-lg-1 col-xs-1"><?php echo $srNo?></div>					
			<div class="col-lg-2 col-xs-2"><?php echo $adate?></div>
			<div class="col-lg-2 col-xs-2"><?php echo$indexValue?></div>
			<div class="col-lg-2 col-xs-2"><?php echo $indexValueTR?></div>	
<div class="col-lg-2 col-xs-2"><?php echo $indexValueNR?></div>				
			</div>
		<?php		}
		}
		
		fclose($file);

		if($srNo) {	
		$url = "http://204.80.90.133/backtestenginedemo/download.php?file=".$title;		
		$url2 = "http://204.80.90.133/backtestenginedemo/download.php?file=".$title2;		
		
		 } ?>	
	</div>

<?php } else { ?>
<div class="container main-body">	
		<div class="row">
				<div class="col-lg-6 col-xs-6"><label>Some thing is wrong some where, Please try again.</label></div>
				<div class="col-lg-6 col-xs-6"><a class="btn btn-primary" href="calculations.php">New Calculation </a></div>
			</div>
<?php } ?>

<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.11.2/moment.min.js"></script>
<script src="http://204.80.90.133/backtestengine/plugins/daterangepicker/daterangepicker.js"></script>
<!-- datepicker -->
<script src="http://204.80.90.133/backtestengine/plugins/datepicker/bootstrap-datepicker.js"></script>

<?php require_once("footer.php"); ?>
<script> 
 $(document).ready(function() {
	$("#downloadhref").attr("href","<?php echo $url?>"); 
		$("#downloadhref2").attr("href","<?php echo $url2?>"); 
	$("#downloadhref").attr("title","<?php echo $title?>");
		
 });

</script>
