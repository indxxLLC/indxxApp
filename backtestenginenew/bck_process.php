<?php
if(isset($_POST['filename']) && isset($_POST['Proceed']) ) { 

//echo dirname(__FILE__)."/tmp/".$_POST['filename']; die;

	$file 		= fopen(dirname(__FILE__)."/tmp/".$_POST['filename'], 'r');
	
	$file_contents = array();
	$totalLines = 0;
	$overAllPeriods = 1;
	$PeriodBreakPoints = array();
	
	while (($line = fgetcsv($file)) !== FALSE) {
	$file_contents[$totalLines] = $line;

	if($totalLines==1) {									
		$PeriodBreakPoints[] = $line[0];									
	}

	if($totalLines>=2) {
		if($file_contents[$totalLines][0] > $file_contents[$totalLines-1][0]) {
			$PeriodBreakPoints[] = $totalLines;					
		}
	}
	$totalLines++;
	}
	
	fclose($file);
		
	if(file_exists(dirname(__FILE__)."/tmp/".$_POST['filename'])) {
		unlink(dirname(__FILE__)."/tmp/".$_POST['filename']);
	}
	
	echo "Process going on please wait...";

} 
   


  