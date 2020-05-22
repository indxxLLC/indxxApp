<?php

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
	$NotTradingmessage 			= '';
	require_once("Database.php");
	$db = new Database();
	$db->connection();
	
	if(isset($_POST['period']) && $_POST['period'] > 0 ) {		
		
		if($_FILES["CVSFile"]["name"]) { 
			
			$temp 			= explode(".", $_FILES["CVSFile"]["name"]);			
			//$mime 			= mime_content_type($_FILES['CVSFile']['tmp_name']);	
			$ext 			= strtolower($temp[sizeof($temp)-1]);	
			if(trim(strtolower($ext)) == "csv") { 
			//if("text/plain" === trim($mime)  && trim(strtolower($ext)) == "csv") {
				
				$Readfile 		= fopen($_FILES['CVSFile']['tmp_name'], 'r');
				
				$file_contents = array();
				$totalLines = 0;
				$overAllPeriods = 1;
				$PeriodBreakPoints = array();
				
				while (($line = fgetcsv($Readfile)) !== FALSE) {
					
					if($totalLines>=1) {	
						if(!isset($line[0]) || !is_numeric($line[0]) || $line[0] <= 0 ) {						
							$periodNull = true;
							break;
						}
						
						if(isset($line[2])) {
							if(!is_numeric($line[2])) {
								$line[2] = str_replace("%","",$line[2]);
								if($line[2]){
								$line[2] = number_format($line[2],7);
								} else {
									$SecuritiesWeightNull = true;
									break;
								}
								if($line[2] <= 0 || $line[2] >= 100) {
									$SecuritiesWeightNull = true;
									break;
								}									
							} 
						} else {
							$SecuritiesWeightNull = true;
							break;
						}
						
					if(!isset($line[2])  || !is_numeric($line[2]) || $line[2] <= 0 || $line[2] >= 100 ) {
							$SecuritiesWeightNull = true;
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
					}
					
				  
				  $totalLines++;
				  
				  
				}
				
				fclose($Readfile);
				
				if($periodNull || $SecuritiesWeightNull) {
					$message .= " <li>Error	:	Few Securities does not have proper period or proper weight. Please check your portfolio.</li>";
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
				
				if($_POST['period']!=$overAllPeriods) {
					$message = " <li>Error:The period,you entered does not match from uploaded portfolio. Please Upload Correct file.</li>";
					$success 	=  true;
					$file  = '';
				} else {	 
					$chkSecurityISN = array();	
					$chkSecurityISNFlag = true;
					$PDCounter = 0;
					for($outer= 0; $outer < $overAllPeriods; $outer++) {
						$totalWeightInteger = number_format($totalWeight[$outer],3); 						
						
						if($totalWeightInteger < 99.50 ||  $totalWeightInteger > 100.44 ) {
							$showp = intval($outer) + 1 ; 
							$message .= " <li>Error	:Total weight of period $showp  is ".number_format($totalWeight[$outer],2)."% Please check your portfolio.</li>";
						}
						
						$totalWeight_five_percentage_interger = number_format($totalWeight_five_percentage[$outer],2); 
						
						if($totalWeight_five_percentage_interger > 45.000) {
							$showp = intval($outer) + 1 ; 
							$warrning .= "<li>Warning : Sum of weights of securities for period  $showp with greater than 5% weight is ".number_format($totalWeight_five_percentage[$outer],2)."% </li>";
							$warrningNoHTML .= "  Sum of weights of securities for period $showp with greater than 5% weight is ".number_format($totalWeight_five_percentage[$outer],2)."%.";	
						}		
						
						// CHECK ALL SECCURITIES ARE TRADING ON ALL PEROIDS START DATE	
						$dateForDB = date('Y-m-d',strtotime($_POST['StartDate'][$outer])); 
						
						$Day = date('D',strtotime($_POST['StartDate'][$outer])); 
						
						$dateForDBDaybefore = date( 'Y-m-d', strtotime( $dateForDB . ' -1 day' ) );
						$dateForDBDayafter 	= date( 'Y-m-d', strtotime( $dateForDB . ' +1 day' ) );
						
						if($Day=="Sun") {
							$dateForDBDaybefore = date( 'Y-m-d', strtotime( $dateForDB . ' -2 day' ) );
							$dateForDBDayafter 	= date( 'Y-m-d', strtotime( $dateForDB . ' +1 day' ) );
						} else if($Day=="Sat") {
							$dateForDBDaybefore = date( 'Y-m-d', strtotime( $dateForDB . ' -1 day' ) );
							$dateForDBDayafter 	= date( 'Y-m-d', strtotime( $dateForDB . ' +2 day' ) );
							
						}
						
						$securityISN = '';
						$PDCounter++ ; 
						$flagSecuritiesNotTrading = 0; 
						for($chkISN = 0; $chkISN < count($SecuritiesUniqueISNs[$outer]); $chkISN++) {
							$securityISN =  $SecuritiesUniqueISNs[$outer][$chkISN];	
							$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
							$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
							$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
							$qry .= " ON PRC.fs_perm_sec_id = ISN.fs_primary_listing_id";
							$qry .= " WHERE ISN.isin = '".$securityISN."'  AND ( PRC.date = '".$dateForDB."' OR PRC.date = '".$dateForDBDaybefore."' OR PRC.date = '".$dateForDBDayafter."' )";
							
							$records = $db->query($qry);
							
							if(count($records)<=0) {
								$chkSecurityISN[$PDCounter] = $PDCounter; 
								$chkSecurityISNFlag = false; 
							    $NotTradingmessage .= " <li>Error : Security - $securityISN of period - $PDCounter is not trading start at the start of the period . Please check your portfolio.</li>";
								$flagSecuritiesNotTrading++;		
							}
							
						}
						// may these three days are off
						if($flagSecuritiesNotTrading>=1) {
							
							
							$dateForDB = date('Y-m-d',strtotime($_POST['StartDate'][$outer])); 
							$Day = date('D',strtotime($_POST['StartDate'][$outer]));
							
							if($Day=="Fri") {
								$dateForDBDaybefore = date( 'Y-m-d', strtotime( $dateForDB . ' -1 day' ) );
								$dateForDBDayafter 	= date( 'Y-m-d', strtotime( $dateForDB . ' +3 day' ) );
							}
														
							$securityISN = '';							
							$NotTradingmessage = '';
							
							$flagSecuritiesNotTrading = 0; 
							for($chkISN = 0; $chkISN < count($SecuritiesUniqueISNs[$outer]); $chkISN++) {
								$securityISN =  $SecuritiesUniqueISNs[$outer][$chkISN];	
								$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
								$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
								$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
								$qry .= " ON PRC.fs_perm_sec_id = ISN.fs_primary_listing_id";
								$qry .= " WHERE ISN.isin = '".$securityISN."'  AND ( PRC.date = '".$dateForDB."' OR PRC.date = '".$dateForDBDaybefore."' OR PRC.date = '".$dateForDBDayafter."' )";
								
								$records = $db->query($qry);
								if(count($records)<=0) {									
									$chkSecurityISNFlag = false; 
									$NotTradingmessage .= " <li>Error : Security - $securityISN of period - $PDCounter is not trading start at the start of the period . Please check your portfolio.</li>";
									$flagSecuritiesNotTrading++;		
								}
								
							}
						}						
					
					}
					
					if(!$chkSecurityISNFlag) {						
						$message .=  $NotTradingmessage;
						foreach($chkSecurityISN as $key => $val) {
							$message .= " <li>Error	: Few Securities of period - $val is not trading start at the start of the period . Please check your portfolio.</li>";
						}
						
					}					
					
					
					$file  = time().".".$ext;
					
					move_uploaded_file($_FILES['CVSFile']['tmp_name'], 'tmp/' . $file );
					$success 	=  true;
					//message .= "System have checked uploaded file. There is no error.";					
					
				}
				
				
			} else {
				$message = "<li>Error	:	File type and extension is not valid. Please upload only csv file.</li>";
				$success 	=  true;
			}
			
		} else {			
			$message = "<li>Error	: Please upload portfolio. </li>";	
			$success 	=  true;
		}
		
		
	} else {
		$message = "<li>Error	: Please enter no of period(s). </li>";	
		$success 	=  true;		
	}
	
	$Securities =  JSON_encode($SecuritiesUniqueISNs);
	
	if($file)
		$returnArr = array("message"=>$message,"warrning"=>$warrning,"success"=>$success,"file"=>$file,"warrningNoHTML"=>$warrningNoHTML,"Securities" => $Securities);
	else
		$returnArr = array("message"=>$message,"warrning"=>$warrning,"success"=>$success,"file"=>"","warrningNoHTML"=>$warrningNoHTML,"Securities" => $Securities);
	
	echo JSON_encode($returnArr);	
	exit();	
		
		
		
		
		