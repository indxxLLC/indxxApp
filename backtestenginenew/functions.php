<?php
error_reporting(0);
$sqlsvr_details =   array(  'UID'   => 'sa',
							'PWD'           => 'f0r3z@786',
							'Database'      => 'FDS_Datafeeds',
							'CharacterSet'  => 'UTF-8'
						);

// try to connect                    
$connection = sqlsrv_connect("INDXX", $sqlsvr_details);

function CheckPriceforAllISINs($SecuritiesUniqueISNs,$prd,$dateForDB) {
	
	$prd = $prd + 1; 
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
	for($chkISN = 0; $chkISN < count($SecuritiesUniqueISNs); $chkISN++) {
		$securityISN =  $SecuritiesUniqueISNs[$chkISN];	
		$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
		$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
		$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
		$qry .= " ON PRC.fs_perm_sec_id = ISN.fs_primary_listing_id";
		$qry .= " WHERE ISN.isin = '".$securityISN."'  AND PRC.date = '".$NewActualDate."'"; 		 
		
		$a = sqlsrv_query( $connection, $qry );			
		$Rows =  sqlsrv_num_rows( $a);		
		$records = sqlsrv_fetch_array( $a, SQLSRV_FETCH_ASSOC);		
		
		if($Rows === false) {
			$NotTradingmessage .= " <li>Error : Security - $securityISN of period - $prd is not trading start at the start of the period . Please check your portfolio.</li>";
			$flagSecuritiesNotTradingOnFirDay++;		
		}
		
		
	}
	
	
	// check for Thrusday. check no security is trading on given date i.e. $dateForDB
	
	if($flagSecuritiesNotTradingOnFirDay>=1) {		
		$NewActualDate = date( 'Y-m-d', strtotime( $NewActualDate . ' -1 day' ) );	
		// check all securities are trading on 1 day (NewActualDate) before given date i.e $dateForDB
		for($chkISN = 0; $chkISN < count($SecuritiesUniqueISNs); $chkISN++) {
			$securityISN =  $SecuritiesUniqueISNs[$chkISN];	
			$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
			$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
			$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
			$qry .= " ON PRC.fs_perm_sec_id = ISN.fs_primary_listing_id";
			$qry .= " WHERE ISN.isin = '".$securityISN."'  AND PRC.date = '".$NewActualDate."'";			
			$a = sqlsrv_query( $connection, $qry );
			$Rows =  sqlsrv_num_rows( $a);		
			$records = sqlsrv_fetch_array( $a, SQLSRV_FETCH_ASSOC);		
		
			if($Rows === false) {				
					$flagSecuritiesNotTradingOnThuDay++;		
			}
			
		}
		
	}
	
	// check for Monday. check no security is trading on given date i.e. $dateForDB
	
	if($flagSecuritiesNotTradingOnThuDay>=1) {		
		$NewActualDate = date( 'Y-m-d', strtotime( $NewActualDate . ' +4 day' ) );	
		// check all securities are trading on 1 day (NewActualDate) before given date i.e $dateForDB
		for($chkISN = 0; $chkISN < count($SecuritiesUniqueISNs); $chkISN++) {
			$securityISN =  $SecuritiesUniqueISNs[$chkISN];	
			$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
			$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
			$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
			$qry .= " ON PRC.fs_perm_sec_id = ISN.fs_primary_listing_id";
			$qry .= " WHERE ISN.isin = '".$securityISN."'  AND PRC.date = '".$NewActualDate."'";			
			$a = sqlsrv_query( $connection, $qry );
			$Rows =  sqlsrv_num_rows( $a);		
			$records = sqlsrv_fetch_array( $a, SQLSRV_FETCH_ASSOC);		
		
			if($Rows === false) {				
				$flagSecuritiesNotTradingOnMonDay++;		
			}
			
		}
		
	}
	
	// check for Tuesday. check no security is trading on given date i.e. $dateForDB
	
	if($flagSecuritiesNotTradingOnMonDay>=1) {		
		$NewActualDate = date( 'Y-m-d', strtotime( $NewActualDate . ' +1 day' ) );	
		// check all securities are trading on 1 day (NewActualDate) before given date i.e $dateForDB
		for($chkISN = 0; $chkISN < count($SecuritiesUniqueISNs); $chkISN++) {
			$securityISN =  $SecuritiesUniqueISNs[$chkISN];	
			$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id"; 
			$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
			$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
			$qry .= " ON PRC.fs_perm_sec_id = ISN.fs_primary_listing_id";
			$qry .= " WHERE ISN.isin = '".$securityISN."'  AND PRC.date = '".$NewActualDate."'";			
			$a = sqlsrv_query( $connection, $qry );
			$Rows =  sqlsrv_num_rows( $a);		
			$records = sqlsrv_fetch_array( $a, SQLSRV_FETCH_ASSOC);		
		
			if($Rows === false) {				
				$flagSecuritiesNotTradingOnTuesDay++;		
			}
			
		}
		
	}
	
	
	
	if($flagSecuritiesNotTradingOnFirDay==0) {
		return array("sucess"=> true,"thedate"=>$NewActualDate);	
		
	} else if($flagSecuritiesNotTradingOnThuDay==0) {
		return array("sucess"=> true,"thedate"=>$NewActualDate);	
		
	} else if($flagSecuritiesNotTradingOnMonDay==0) {
		return array("sucess"=> true,"thedate"=>$NewActualDate);	
		
	} else if($flagSecuritiesNotTradingOnTuesDay==0) {
		return array("sucess"=> true,"thedate"=>$NewActualDate);	
		
	} else {
		echo "all fial"; die;
		return array("sucess"=> false);	
	}
	
}
