<?php
error_reporting(0);
$sqlsvr_details = array('UID'   => 'sa',
					'PWD'           => 'f0r3z@786',
					'Database'      => 'FDS_Datafeeds',
					'CharacterSet'  => 'UTF-8'
				);
// try to connect                    
$connection = sqlsrv_connect("INDXX", $sqlsvr_details);
//require_once("functions.php");
$message 					= '';
$warrning 					= '';
$success 					=  false;
$file 						= '';
$warrningNoHTML 			= '';
$SecuritiesWeightNull  		= false;
$periodNull  				= false;
$SecuritiesNull  			= false;
$SecuritiesWeightNotNumeric = false;
$SecuritiesUniqueISNs		= array();
$SecuritiesStartDate		= array();
$SecuritiesStartDate1		= array();
$SecuritiesEndDate		= array();
$NotTradingmessage 			= '';	
$checkResult 				= array();
$SecuritiesWeight 			= array();
$Securitiescountry 			= array();
$ISIN_arr = '';
// if(isset($_POST['period']) && $_POST['period'] > 0 ) {		
if($_FILES["CVSFile"]["name"]) { 
	$temp = explode(".", $_FILES["CVSFile"]["name"]);			
	//$mime = mime_content_type($_FILES['CVSFile']['tmp_name']);	
	$ext = strtolower($temp[sizeof($temp)-1]);	
	if(trim(strtolower($ext)) == "csv") { 
	//if("text/plain" === trim($mime)  && trim(strtolower($ext)) == "csv") {
		$Readfile = fopen($_FILES['CVSFile']['tmp_name'], 'r');
		$file_contents = array();
		$totalLines = 0;
		$overAllPeriods = 1;
		$PeriodBreakPoints = array();
		while (($line = fgetcsv($Readfile)) !== FALSE) {
			if($totalLines>=1) {	
				if(!isset($line[0]) || !is_numeric($line[0]) ) {				//|| $line[0] <= 0 		
					$periodNull = true;
					$ISIN_arr = $line[1];
					break;
				}
				if(!isset($line[3])|| $line[3] <= 0 ) {						
					$SecuritiesStartDateNull = true;
					$ISIN_arr = $line[1];
					break;
				}
				if(isset($line[2])) {
					if(!is_numeric($line[2])) {
						$line[2] = str_replace("%","",$line[2]);
						// if($line[2]){
						// $line[2] = number_format($line[2]);
						// } else {
							// $SecuritiesWeightNull = true;
							// break;
						// }
						if($line[2] < 0 || $line[2] > 100) {
							$SecuritiesWeightNull = true;
							$ISIN_arr = $line[1];
							break;
						}else{
							$line[2] = number_format($line[2]);
						}
					} 
				} else {
					$SecuritiesWeightNull = true;
					$ISIN_arr = $line[1];
					break;
				}
			if(!isset($line[2])  || !is_numeric($line[2]) || $line[2] < 0 || $line[2] > 100 ) {
					$SecuritiesWeightNull = true;
					$ISIN_arr = $line[1];
					break;
				}
			}
			$file_contents[$totalLines] = $line;
			if($totalLines==1) {									
				$PeriodBreakPoints[] = $line[0];
			}
			if($totalLines>=2) {						
				if($file_contents[$totalLines][0] > $file_contents[$totalLines-1][0]) {
					$PeriodBreakPoints[] = $totalLines;	
				}				
			}
			$tperiodNo =  count($PeriodBreakPoints) - 1;
			if($totalLines==1)
				$tperiodNo = 0;
			if( $tperiodNo >= 0 ) {						
				$SecuritiesUniqueISNs[$tperiodNo][] = $line[1];
				$SecuritiesStartDate[$tperiodNo][] = $line[3];
				$SecuritiesStartDate1[$tperiodNo] = $line[3];
				$SecuritiesEndDate[$tperiodNo] = $line[4];
			}
			if($tperiodNo>=0) {
				$SecuritiesWeight[$tperiodNo][$line[1]]= $line[2];
				$Securitiescountry[$tperiodNo][$line[1]]=$line[5];
			}
		  $totalLines++;				  
		}	
		fclose($Readfile);
		if($periodNull || $SecuritiesStartDateNull) { //$SecuritiesWeightNull ||
			$message .= " <li style='list-style:none;'>Error	:	$ISIN_arr do not have proper period, proper weight or proper Start Date and End Date. Please check your portfolio.</li>";
			$returnArr = array("message"=>$message,"warrning"=>"","success"=>"true","file"=>"","warrningNoHTML"=>"");		
			echo JSON_encode($returnArr);
			exit();	
		} else {	
			$PeriodBreakPoints[] 	= $totalLines ;	
			$overAllPeriods 		= count($PeriodBreakPoints)	-	1; 
			$totalWeight = array();	
			$totalWeight_five_percentage = array();	
			for($outer= 0; $outer < $overAllPeriods; $outer++) { 				
					$Weight	= 0;
					$five_percentage_Weight = 0;
					for($We=$PeriodBreakPoints[$outer]; $We < $PeriodBreakPoints[$outer+1]; $We++) {
						$weight_with_seven_points = number_format($file_contents[$We][2],7);
						if($weight_with_seven_points) {	
							$Weight	 += $weight_with_seven_points;
							if($weight_with_seven_points >= 5) {
								$five_percentage_Weight	 += $weight_with_seven_points;
							}
						}
					}
					$totalWeight[] = $Weight;
					$totalWeight_five_percentage[] = $five_percentage_Weight;
				}
		} 
		// if($_POST['period']!=$overAllPeriods) {
			// $message = " <li style='list-style:none;'>Error:The period,you entered does not match from uploaded portfolio. Please Upload Correct file.</li>";
			// $success 	=  true;
			// $file  = '';
		// } else {	 
			$chkSecurityISN = array();	
			$chkSecurityISNFlag = true;
			$PDCounter = 0;
			for($outer= 0; $outer < $overAllPeriods; $outer++) {
				$totalWeightInteger = number_format($totalWeight[$outer],3); 						
				if($totalWeightInteger < 99.50 ||  $totalWeightInteger > 100.44 ) {
					$showp = intval($outer) + 1 ; 
					$message .= " <li style='list-style:none;'>Error	:Total weight of period $showp  is ".number_format($totalWeight[$outer],2)."% Please check your portfolio.</li>";
				}
				$totalWeight_five_percentage_interger = number_format($totalWeight_five_percentage[$outer],2); 
				if($totalWeight_five_percentage_interger > 45.000) {
					$showp = intval($outer) + 1 ; 
					$warrning .= "<li style='list-style:none;'>Warning : Sum of weights of securities for period  $showp with greater than 5% weight is ".number_format($totalWeight_five_percentage[$outer],2)."% </li>";
					$warrningNoHTML .= "  Sum of weights of securities for period $showp with greater than 5% weight is ".number_format($totalWeight_five_percentage[$outer],2)."%.";	
				}	
$qry = "SELECT PRC.p_price ,PRC.date , PRC.fs_perm_sec_id,ISN.isin"; 
	$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
	$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
	$qry .= " ON PRC.fs_perm_sec_id =CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
	$qry .= " WHERE ISN.isin in  (". "'" . implode ( "', '", array_values($SecuritiesUniqueISNs[$outer]) ) . "'".")  AND  PRC.date between '".date('Y-m-d', strtotime("-5 day", strtotime($SecuritiesStartDate1[$outer])))."' and '".date('Y-m-d', strtotime($SecuritiesStartDate1[$outer])) ."'";						
	$qry .= " ORDER BY ISN.isin, PRC.date ";
	$a = sqlsrv_query( $connection, $qry );
	$count= 0;
		$pricearray=array();
	while( $record = sqlsrv_fetch_array( $a, SQLSRV_FETCH_ASSOC) ) {
		$DBdatArray = (array) $record['date'];
		$pricearray[$record['isin']]=date( 'Y-m-d', strtotime($DBdatArray['date']) );
	}
	for($chkISN = 0; $chkISN < count($SecuritiesUniqueISNs[$outer]); $chkISN++) {
	$securityISN =  $SecuritiesUniqueISNs[$outer][$chkISN];
	if(!in_array($securityISN, array_keys($pricearray))){
		$message .= " <li style='list-style:none;'>Error	:  Securities $securityISN of period - $showp is not trading start at the start of the period . Please check your portfolio.</li>";
					$chkSecurityISNFlag = false;
	}
	}
				// CHECK ALL SECCURITIES ARE TRADING ON ALL PEROIDS START DATE	
				$dateForDB = date('Y-m-d',strtotime($_POST['StartDate'][$outer])); 	
				$flagSecuritiesNotTrading = 0; 						
				//$tmpcheckResult = CheckPriceforAllISINs($SecuritiesUniqueISNs[$outer],$outer,$dateForDB);
				//  code start for dates validations 
				/*
				$chkSecurityISNFlag = false; 
				$flagSecuritiesNotTradingOnFirDay = 0;
				$flagSecuritiesNotTradingOnThuDay = 0 ;
				$flagSecuritiesNotTradingOnMonDay = 0 ;
				$flagSecuritiesNotTradingOnTuesDay = 0 ;
				$Day = date('D',strtotime($dateForDB));
				$NewActualDate = $dateForDB;
				if($Day=="Sat") {
					$NewActualDate = date( 'Y-m-d', strtotime( $dateForDB . ' -1 day' ) );
				} else if($Day=="Sun") {
					$NewActualDate = date( 'Y-m-d', strtotime( $dateForDB . ' -2 day' ) );
				}
				// check for Firday. check all securities are trading on given date i.e $dateForDB
				for($chkISN = 0; $chkISN < count($SecuritiesUniqueISNs[$outer]); $chkISN++) {
					$securityISN =  $SecuritiesUniqueISNs[$outer][$chkISN];	
					$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
					$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
					$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
					$qry .= " ON PRC.fs_perm_sec_id = CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
					$qry .= " WHERE ISN.isin = '".$securityISN."'  AND PRC.date = '".$NewActualDate."'"; 													
					$stmt = sqlsrv_query( $connection, $qry , array(), array( "Scrollable" => SQLSRV_CURSOR_KEYSET ));  
					$row_count = sqlsrv_num_rows( $stmt );  
					if ($row_count == false) {   
						$NotTradingmessage .= " <li style='list-style:none;'>Error : Security - $securityISN of period - $prd is not trading start at the start of the period . Please check your portfolio.</li>";
						$flagSecuritiesNotTradingOnFirDay++;
					}else if ($row_count == 0)  {
						$NotTradingmessage .= " <li style='list-style:none;'>Error : Security - $securityISN of period - $prd is not trading start at the start of the period . Please check your portfolio.</li>";
						$flagSecuritiesNotTradingOnFirDay++;
					}	
				}
				// check for Thrusday. check no security is trading on given date i.e. $dateForDB
				if($flagSecuritiesNotTradingOnFirDay>=1) {		
					$NewActualDate = date( 'Y-m-d', strtotime( $NewActualDate . ' -1 day' ) );	
					// check all securities are trading on 1 day (NewActualDate) before given date i.e $dateForDB
					for($chkISN = 0; $chkISN < count($SecuritiesUniqueISNs[$outer]); $chkISN++) {
						$securityISN =  $SecuritiesUniqueISNs[$outer][$chkISN];	
						$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
						$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
						$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
						$qry .= " ON PRC.fs_perm_sec_id = CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
						$qry .= " WHERE ISN.isin = '".$securityISN."'  AND PRC.date = '".$NewActualDate."'";			
						$stmt = sqlsrv_query( $connection, $qry , array(), array( "Scrollable" => SQLSRV_CURSOR_KEYSET ));  
						$row_count = sqlsrv_num_rows( $stmt );  
						if ($row_count == false) { 
							$flagSecuritiesNotTradingOnThuDay++;
						}else if ($row_count == 0)  {									
							$flagSecuritiesNotTradingOnThuDay++;
						}
					}
				}
				// check for Monday. check no security is trading on given date i.e. $dateForDB
				if($flagSecuritiesNotTradingOnThuDay>=1) {		
					$NewActualDate = date( 'Y-m-d', strtotime( $NewActualDate . ' +4 day' ) );	
					// check all securities are trading on 1 day (NewActualDate) before given date i.e $dateForDB
					for($chkISN = 0; $chkISN < count($SecuritiesUniqueISNs[$outer]); $chkISN++) {
						$securityISN =  $SecuritiesUniqueISNs[$outer][$chkISN];	
						$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
						$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
						$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
						$qry .= " ON PRC.fs_perm_sec_id = CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
						$qry .= " WHERE ISN.isin = '".$securityISN."'  AND PRC.date = '".$NewActualDate."'";			
						$stmt = sqlsrv_query( $connection, $qry , array(), array( "Scrollable" => SQLSRV_CURSOR_KEYSET ));  
						$row_count = sqlsrv_num_rows( $stmt );  
						if ($row_count == false) { 
							$flagSecuritiesNotTradingOnMonDay++;
						}else if ($row_count == 0)  {									
							$flagSecuritiesNotTradingOnMonDay++;
						}
					}
				}
				// check for Tuesday. check no security is trading on given date i.e. $dateForDB
				if($flagSecuritiesNotTradingOnMonDay>=1) {		
					$NewActualDate = date( 'Y-m-d', strtotime( $NewActualDate . ' +1 day' ) );	
					// check all securities are trading on 1 day (NewActualDate) before given date i.e $dateForDB
					for($chkISN = 0; $chkISN < count($SecuritiesUniqueISNs[$outer]); $chkISN++) {
						$securityISN =  $SecuritiesUniqueISNs[$outer][$chkISN];	
						$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
						$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
						$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
						$qry .= " ON PRC.fs_perm_sec_id = CASE WHE ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
						$qry .= " WHERE ISN.isin = '".$securityISN."'  AND PRC.date = '".$NewActualDate."'";			
						$stmt = sqlsrv_query( $connection, $qry , array(), array( "Scrollable" => SQLSRV_CURSOR_KEYSET ));  
						$row_count = sqlsrv_num_rows( $stmt );  
						if ($row_count == false) { 
							$flagSecuritiesNotTradingOnTuesDay++;
						}else if ($row_count == 0)  {									
							$flagSecuritiesNotTradingOnTuesDay++;
						}
					}
				}
				if($flagSecuritiesNotTradingOnFirDay==0) {
					$tmpcheckResult =  array("sucess"=> true,"thedate"=>date('m/d/Y',strtotime($NewActualDate)));	
				} else if($flagSecuritiesNotTradingOnThuDay==0 && $flagSecuritiesNotTradingOnFirDay > 0 ) {
					$tmpcheckResult = array("sucess"=> true,"thedate"=>date('m/d/Y',strtotime($NewActualDate)));	
				} else if($flagSecuritiesNotTradingOnMonDay==0 && $flagSecuritiesNotTradingOnThuDay > 0  && $flagSecuritiesNotTradingOnFirDay > 0) {
					$tmpcheckResult = array("sucess"=> true,"thedate"=>date('m/d/Y',strtotime($NewActualDate)));	
				} else if($flagSecuritiesNotTradingOnTuesDay==0 && $flagSecuritiesNotTradingOnMonDay > 0  && $flagSecuritiesNotTradingOnThuDay > 0  && $flagSecuritiesNotTradingOnFirDay > 0) {
					$tmpcheckResult = array("sucess"=> true,"thedate"=>date('m/d/Y',strtotime($NewActualDate)));	
				} else {
					$tmpcheckResult = array("sucess"=> false);	
				}
				// code end ofr date validations
				$checkResult[] = $tmpcheckResult ;
				if(!$tmpcheckResult['sucess']) {
					$showp = intval($outer) + 1 ; 
					$message .= " <li style='list-style:none;'>Error	: Few Securities of period - $showp is not trading start at the start of the period . Please check your portfolio.</li>";
					$chkSecurityISNFlag = false;
				}						
			*/
			}	
			// }
			if($message=="") {
				$file  = time().".".$ext;						
				move_uploaded_file($_FILES['CVSFile']['tmp_name'], 'tmp/' . $file );
			}
			$success 	=  true;
			//message .= "System have checked uploaded file. There is no error.";	
	} else {
		$message = "<li style='list-style:none;'>Error	:	File type and extension is not valid. Please upload only csv file.</li>";
		$success 	=  true;
	}
} else {			
	$message = "<li style='list-style:none;'>Error	: Please upload portfolio. </li>";	
	$success 	=  true;
}
// } 
// else {
// $message = "<li style='list-style:none;'>Error	: Please enter no of period(s). </li>";	
// $success 	=  true;		
// }
		  // print_r($SecuritiesUniqueISNs);
		  // print_r($SecuritiesStartDate);
		  // print_r($SecuritiesWeight);
		  // print_r($checkResult);
		  // die;
$Securities =  JSON_encode($SecuritiesUniqueISNs);
$checkResultDates = array();
foreach($checkResult as $key =>$value) {
$checkResultDates[]  = $value['thedate'];
}
$checkResultDates =  JSON_encode($checkResultDates);
$SecuritiesWeightJSON = JSON_encode($SecuritiesWeight);
$SecuritiesStartDateJSON = JSON_encode($SecuritiesStartDate1);
$SecuritiesEndDateJSON = JSON_encode($SecuritiesEndDate);
$Periods = JSON_encode($overAllPeriods);
if($file)
$returnArr = array("message"=>$message,"warrning"=>$warrning,"success"=>$success,"thedates"=>$checkResultDates,"file"=>$file,"warrningNoHTML"=>$warrningNoHTML,"Securities" => $Securities,"SecuritiesWeightJSON" => $SecuritiesWeightJSON,"Securitiescountry" => JSON_encode($Securitiescountry),"SecuritiesStartDateJSON" => $SecuritiesStartDateJSON,"SecuritiesEndDateJSON" => $SecuritiesEndDateJSON,"Periods" => $Periods);
else
$returnArr = array("message"=>$message,"warrning"=>$warrning,"success"=>$success,"file"=>"","thedates"=>$checkResultDates,"warrningNoHTML"=>$warrningNoHTML,"Securities" => $Securities,"SecuritiesWeightJSON" => $SecuritiesWeightJSON,"SecuritiesStartDateJSON" => $SecuritiesStartDateJSON,"SecuritiesEndDateJSON" => $SecuritiesEndDateJSON,"Periods" => $Periods);
// print_r($returnArr); die;
echo JSON_encode($returnArr);	
exit();	