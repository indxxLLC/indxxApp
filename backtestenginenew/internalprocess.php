<?php

	
	require_once("Database.php");
	$db = new Database();
	$db->connection();
	$HTML = ''; 

		
	
	$securities 	=  JSON_decode($_POST['securities']);
	echo "<pre>";
	print_r($securities);
	die;
	$currency 		=  $_POST['currency'];
	$showPRD 		= $_POST['period'] + 1 ; 
	
	
	$HTML .= '<div class="row">
		<div class="col-lg-12 col-xs-12"><label>Data of period '.$showPRD.'</label></div>
	</div>
	<div class="row">
			<div class="col-lg-1 col-xs-1"><label>SR</label></div>
			<div class="col-lg-3 col-xs-3"><label>Security ISN</label></div>
			<div class="col-lg-2 col-xs-2"><label>Currency</label></div>
			<div class="col-lg-2 col-xs-2"><label>Date (MM/DD/YYYY)</label></div>
			<div class="col-lg-2 col-xs-2"><label>Price</label></div>
			<div class="col-lg-2 col-xs-2"><label>Excange Rate</label></div>
	</div>';
		
			
	$sr = 1 ;
	$SecurityISN = '';
	$price = 0.0;
	$exRate = 0.0;
	
	for($chkISN = 0; $chkISN < count($securities[$_POST['period']]); $chkISN++) {
		
		$securityISN 	= $securities[$_POST['period']][$chkISN];
		$StartDate 		= $_POST['StartDate'];
		$EndDate 		= $_POST['EndDate'];
		
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
			//$records =  (array) $db->query($qry);
			
			if(count($records['data'])<=0) {									
				$price  = 0.0;		
			} else {						
				$price  = $records['p_price'];
			}
			
			$HTML .= '<div class="row">
				<div class="col-lg-1 col-xs-1">'.$sr.'</div>
				<div class="col-lg-3 col-xs-3">'.$securityISN.'</div>
				<div class="col-lg-2 col-xs-2">'.$currency.'</div>
				<div class="col-lg-2 col-xs-2">'.$date.'</div>
				<div class="col-lg-2 col-xs-2">'.$price.'</div>
				<div class="col-lg-2 col-xs-2">Excange Rate</div>
		</div>';
		
		
		$sr++;
		$date 		= date( 'm/d/Y', strtotime( $date . ' +1 day' ) );
		}
	}
								
		
	echo $HTML;	
	exit();	
		
		
		
		
		