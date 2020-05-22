<?php
error_reporting(E_ALL);
require_once("header.php");
require_once("functions_new.php");

$messgae 		= ""; 
$warrning 		= "";  
$buttonFlag 	= false;  
$securities 	= array();
$currency 		= 'USD'; 
$showPRD 		= 0; 
$url 			= '';
$title 			= '';
$numberofDays=5;
$investmentvalue=100000;
$index_value=1000;
$divisor=100;
$allcurrency=array();
$TAXDATA	= array();



$target_Path = "inputs/";
$target_Path = $target_Path.basename( $_FILES['CVSFile']['name'] );

if (move_uploaded_file( $_FILES['CVSFile']['tmp_name'], $target_Path )) {
     // echo "<P>FILE UPLOADED TO: $target_file</P>";
   } else {
     // echo "<P>MOVE UPLOADED FILE FAILED!</P>";
    //  print_r(error_get_last());
   }


//nprint($_POST);
	//exit;
$_POST['StartDate'] = explode(',',trim($_POST['StartDate'],"[]"));
$_POST['EndDate'] = explode(',',trim($_POST['EndDate'],"[]"));
$_POST['currency']='USD';
if($_POST['SecuritiesWeightJSON'] && $_POST['StartDate'] && $_POST['EndDate'] && $_POST['currency']) {


	getTax($TAXDATA,$_FILES['tCVSFile']);

//nprint($TAXDATA);
	//exit;
	
	$SecuritiesWeightJSON=array();
	$TmpSecuritiesWeightJSON = (array) JSON_decode($_POST['SecuritiesWeightJSON']);
foreach($TmpSecuritiesWeightJSON as $tmpval) {
	$SecuritiesWeightJSON[] = (array) $tmpval;
}

//nprint($SecuritiesWeightJSON);
	//exit;
unset($TmpSecuritiesWeightJSON);
	
	$SecuritiesCountryJSON=array();
	$TmpSecuritiesCountryJSON = (array) JSON_decode($_POST['Securitiescountry']);
foreach($TmpSecuritiesCountryJSON as $tmpval) {
	$SecuritiesCountryJSON[] = (array) $tmpval;
}
unset($TmpSecuritiesCountryJSON);

$finalArray=array();
if(!empty ($_POST['StartDate']) && !empty ($_POST['EndDate']))
{
	// echo $_POST['period']; die;
	for($i=0;$i<$_POST['period'];$i++)
	{
		// echo 'frdfjgjsfgjfg'; die;
		if($i==0)
		{
			$finalArray[$i][date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i])))]['PR_mcap']=$investmentvalue;
			$finalArray[$i][date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i])))]['PR_index_value']=$index_value;
			$finalArray[$i][date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i])))]['PR_divisor']=$divisor;
			$finalArray[$i][date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i])))]['TR_mcap']=$investmentvalue;
			$finalArray[$i][date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i])))]['TR_index_value']=$index_value;
			$finalArray[$i][date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i])))]['TR_divisor']=$divisor;
			$finalArray[$i][date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i])))]['NTR_mcap']=$investmentvalue;
			$finalArray[$i][date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i])))]['NTR_index_value']=$index_value;
			$finalArray[$i][date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i])))]['NTR_divisor']=$divisor;
		}
		 // print_r($finalArray); die;
		
		$delisting	= array();
		$cas	= array();
$shares=array();

	$allPrices=getPrices(date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i]))),date("Y-m-d",strtotime(json_decode($_POST['EndDate'][$i]))),array_keys($SecuritiesWeightJSON[$i]),$SecuritiesCountryJSON[$i]);
	getCurrencyCombo($allcurrency,$_POST['currency'],$allPrices,date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i]))),date("Y-m-d",strtotime(json_decode($_POST['EndDate'][$i]))));
	
	////nprint($allcurrency);
	//exit;
	
	ValidatePrices($allPrices,date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i]))),date("Y-m-d",strtotime(json_decode($_POST['EndDate'][$i]))),$numberofDays,array_keys($SecuritiesWeightJSON[$i]),$delisting);
	ValidateCurrency($allcurrency,date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i]))),date("Y-m-d",strtotime(json_decode($_POST['EndDate'][$i]))),$numberofDays,$_POST['currency']);
	getDividends($cas,date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i]))),date("Y-m-d",strtotime(json_decode($_POST['EndDate'][$i]))),array_keys($SecuritiesWeightJSON[$i]));
ValidateDividends($delisting,$cas);
	if($i==0)
		{
		CalcShare($shares,$SecuritiesWeightJSON[$i],date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i]))),$finalArray[$i][date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i])))],$allPrices,$allcurrency);
		
		
		}else{
			CalcShare($shares,$SecuritiesWeightJSON[$i],date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i]))),$finalArray[$i-1][date('Y-m-d',strtotime(json_decode($_POST['EndDate'][$i-1])))],$allPrices,$allcurrency);
		}
		
		
		//nprint($cas);
	//exit;
		
		CalcIndex($allPrices,$allcurrency,$shares,date("Y-m-d",strtotime(json_decode($_POST['StartDate'][$i]))),date("Y-m-d",strtotime(json_decode($_POST['EndDate'][$i]))),$i,$finalArray,$delisting,$cas,$TAXDATA,$_POST['spinoff']);
			
		
		
		
		
		
		}
		
		

	
		
		/*require_once ('PHPExcel/PHPExcel.php');
        require_once ('PHPExcel/PHPExcel/IOFactory.php');
		
		
		$objPHPExcel = new PHPExcel();
 $objPHPExcel->getProperties()->setCreator("creater");
 $objPHPExcel->getProperties()->setLastModifiedBy("Middle field");
 $objPHPExcel->getProperties()->setSubject("Subject");
 
 
		$objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel, "Excel5");
 //$objWorkSheet = $objPHPExcel->createSheet();
 $work_sheet_count=2;//number of sheets you want to create
 $work_sheet=0;
 while($work_sheet<=$work_sheet_count){ 
     if($work_sheet==0){
         $objWorkSheet = $objPHPExcel->createSheet($work_sheet); //Setting index when creating

      //Write cells
      $objWorkSheet->setCellValue('A1', 'Date')
                   ->setCellValue('B1', 'PR')
                   ->setCellValue('C1', 'TR')
                   ->setCellValue('D1', 'NTR');

				 if(!empty($finalArray))
{
	$i=2;
	foreach($finalArray as $k=>$dates){
		foreach($dates as $date=>$data)
{
	   $objWorkSheet->setCellValue('A'.$i, $date)
                   ->setCellValue('B'.$i, $data['PR_index_value'])
                   ->setCellValue('C'.$i, $data['TR_index_value'])
                   ->setCellValue('D'.$i, $data['NTR_index_value']);
	
	$i++;
	
	 file_put_contents('csvfiles/log_'.date("j.n.Y").'.txt', "Writing index values for ".$date."-".$i."\n", FILE_APPEND);	
}}}  
				   
				   
				   
      // Rename sheet
      $objWorkSheet->setTitle("Index Values");
		
		
		
		
     }
     if($work_sheet==1){
                 $objWorkSheet = $objPHPExcel->createSheet($work_sheet); //Setting index when creating

      //Write cells
	  
	  ////	$header = array("S.No","Date","Index Value PR","Market CAP PR","Divisor PR","Index Value TR","Market CAP TR","Divisor TR","Index Value NTR","Market CAP NTR","Divisor NTR","ISIN","Currency","Country","TAX","Share PR","Share TR","Share NTR","Local Price","USD PRICE","MCAP PR","MCAP TR","MCAP NTR","Currency Price","Price Date","Weight PR","Weight TR","Weight NTR","Dividend","Split","Spin");
      $objWorkSheet->setCellValue('A1', 'S.No.')
					->setCellValue('B1', 'Date')
                   ->setCellValue('C1', 'Index Value PR')
				   ->setCellValue('D1', 'Market Value PR')
				   ->setCellValue('E1', 'Divisor PR')
                   ->setCellValue('F1', 'Index Value TR')
				     ->setCellValue('G1', 'Market Value TR')
				   ->setCellValue('H1', 'Divisor TR')
                   ->setCellValue('I1', 'Index Value NTR')
				     ->setCellValue('J1', 'Market Value NTR')
				   ->setCellValue('K1', 'Divisor NTR')
				   ->setCellValue('L1', 'ISIN')
				   ->setCellValue('M1', 'Currency')
				   ->setCellValue('N1', 'Country')
				   ->setCellValue('O1', 'TAX')
				   ->setCellValue('P1', 'Share PR')
				   ->setCellValue('Q1', 'Share TR')
				   ->setCellValue('R1', 'Share NTR')
				   ->setCellValue('S1', 'Local Price')
				   ->setCellValue('T1', 'USD PRICE')
				   ->setCellValue('U1', 'MCAP PR')
				   ->setCellValue('V1', 'MCAP TR')
				   ->setCellValue('W1', 'MCAP NTR')
				   ->setCellValue('X1', 'Currency Price')
				   ->setCellValue('Y1', 'Price Date')
				   ->setCellValue('Z1', 'Weight PR')
				   ->setCellValue('AA1', 'Weight TR')
				   ->setCellValue('AB1', 'Weight NTR')
				   ->setCellValue('AC1', 'Dividend')
				   ->setCellValue('AD1', 'Split')
				   ->setCellValue('AE1', 'Spin');

				 if(!empty($finalArray))
{
	$i=2;
	foreach($finalArray as $k=>$dates){
		foreach($dates as $date=>$data)
		{
			foreach($data['Securities'] as  $isind=>$isindata )
			{
				
				
				
				
				
				
				
				
				//fputcsv ($file, ,,,,,,,,,,,,,,,,,,,,,,,,,,,));
				
				
				$objWorkSheet->setCellValue('A'.$i, $k)
					->setCellValue('B'.$i, $date)
                   ->setCellValue('C'.$i, $data['PR_index_value'])
				   ->setCellValue('D'.$i, $data['PR_mcap'])
				   ->setCellValue('E'.$i,$data['PR_divisor'])
                   ->setCellValue('F'.$i, $data['TR_index_value'])
				     ->setCellValue('G'.$i, $data['TR_mcap'])
				   ->setCellValue('H'.$i, $data['TR_divisor'])
                   ->setCellValue('I'.$i, $data['NTR_index_value'])
				     ->setCellValue('J'.$i, $data['NTR_mcap'])
				   ->setCellValue('K'.$i, $data['NTR_divisor'])
				   ->setCellValue('L'.$i, $isind)
				   ->setCellValue('M'.$i, $isindata['currencysymbol'])
				   ->setCellValue('N'.$i, $isindata['country'])
				   ->setCellValue('O'.$i, $isindata['tax'])
				   ->setCellValue('P'.$i, $isindata['PR_share'])
				   ->setCellValue('Q'.$i, $isindata['TR_share'])
				   ->setCellValue('R'.$i, $isindata['NTR_share'])
				   ->setCellValue('S'.$i, $isindata['localprice'])
				   ->setCellValue('T'.$i, $isindata['PRUSDPRICE'])
				   ->setCellValue('U'.$i, $isindata['sprmcap'])
				   ->setCellValue('V'.$i, $isindata['strmcap'])
				   ->setCellValue('W'.$i, $isindata['sntrmcap'])
				   ->setCellValue('X'.$i, $isindata['currency'])
				   ->setCellValue('Y'.$i, $isindata['price_date'])
				   ->setCellValue('Z'.$i, $isindata['PR_weight'])
				   ->setCellValue('AA'.$i, $isindata['TR_weight'])
				   ->setCellValue('AB'.$i, $isindata['NTR_weight'])
				   ->setCellValue('AC'.$i, isset($isindata['ca']['dividend'])?$isindata['ca']['dividend']:"")
				   ->setCellValue('AD'.$i, isset($isindata['ca']['split'])?$isindata['ca']['split']:"")
				   ->setCellValue('AE'.$i, isset($isindata['ca']['spin'])?$isindata['ca']['spin']:"");
				
				 file_put_contents('csvfiles/log_'.date("j.n.Y").'.txt', "Writing constituants values for ".$date."-".$i."\n", FILE_APPEND);	
				$i++;
			}
		}
	}
}	
				   
				   
				   
      // Rename sheet
      $objWorkSheet->setTitle("Constituants");
		
		
     }
    
     $work_sheet++;
 }
		
		 $title3 = date('Y-m-d-').time()."_tempreport.xls";
		$filename = dirname(__FILE__)."/csvfiles/".$title3;
		
$objWriter->save($filename);
		
	

*/
	
		
		//nprint($finalArray);
		// print_r($allPrices);
	
		  $title = date('Y-m-d-').time()."_indexreport.csv";
		$filename =dirname(__FILE__)."/csvfiles/".$title;		
		$srNo = 0;	
		$file =  fopen($filename, 'w');
		
		$header = array("S.No","Date","Index Value PR","Index Value TR","Index Value NTR");
		ob_start();
		fputcsv ($file, $header);	
if(!empty($finalArray))
{ 
	foreach($finalArray as $k=>$dates){
		$j=0;
		
		foreach($dates as $date=>$data)
		{
			
		
	if($j>0 || $k==0)
				fputcsv ($file, array($k+1,$date,$data['PR_index_value'],$data['TR_index_value'],$data['NTR_index_value']));
		$j++;	
		}
	}
}	
		
	fclose($file); 
		
	  $title2 = date('Y-m-d-').time()."_Constituentsreport.csv";
		$filename =dirname(__FILE__)."/csvfiles/".$title2;		
		$srNo = 0;	
		$file =  fopen($filename, 'w');
		
		$header = array("S.No","Date","Index Value PR","Market CAP PR","Divisor PR","Index Value TR","Market CAP TR","Divisor TR","Index Value NTR","Market CAP NTR","Divisor NTR","ISIN","Currency","Country","TAX","Share PR","Share TR","Share NTR","Local Price","USD PRICE","MCAP PR","MCAP TR","MCAP NTR","Currency Price","Price Date","Weight PR","Weight TR","Weight NTR","Dividend","Special Dividend","Split","Spin");
		ob_start();
		fputcsv ($file, $header);	
if(!empty($finalArray))
{
	foreach($finalArray as $k=>$dates){
		foreach($dates as $date=>$data)
		{
			$data_arr = $data['Securities'];
			foreach($data_arr as  $isind=>$isindata )
			{
				
				//nprint($isindata);
				$dividend="";
				$specialDividend="";
				$spin="";
				if(array_key_exists("ca",$isindata))
					{
				foreach($isindata['ca'] as $type=>$cadata)
				{
					if(is_array($cadata)){
					if(!array_key_exists("split",$cadata))
					{
						if(in_array($type,array(11,134)))
						{
							$specialDividend.=$cadata['dividend']." ".$cadata['currency']." ";
							
						}
						else{
							$dividend.=$cadata['dividend']." ".$cadata['currency']." ";
						}
						if(is_array($cadata)){
						if(array_key_exists("spin",$cadata)){
							$spin.=$cadata['spin'];
						}}
						
						
					}}
				}
				
					}
				
				fputcsv ($file, array($k+1,$date,$data['PR_index_value'],$data['PR_mcap'],$data['PR_divisor'],$data['TR_index_value'],$data['TR_mcap'],$data['TR_divisor'],$data['NTR_index_value'],$data['NTR_mcap'],$data['NTR_divisor'],$isind,$isindata['currencysymbol'],$isindata['country'],$isindata['tax'],$isindata['PR_share'],$isindata['TR_share'],$isindata['NTR_share'],$isindata['localprice'],$isindata['PRUSDPRICE'],$isindata['sprmcap'],$isindata['strmcap'],$isindata['sntrmcap'],$isindata['currency'],$isindata['price_date'],$isindata['PR_weight'],$isindata['TR_weight'],$isindata['NTR_weight'],$dividend,$specialDividend,isset($isindata['ca']['split'])?$isindata['ca']['split']:"",$spin));
			}
		}
	}
}	
		
	fclose($file); 
// $filename; 

 
}


$url = "download.php?file=".$title;		
		$url2 = "download.php?file=".$title2;		
		
	
	
}

?>

	

<div class="container main-body">	
		<div class="row">
				<div class="col-lg-6 col-xs-6"><a target="_blank" class="btn btn-primary" id="downloadhref" href="#" title="">Download Index Values file</a> <a target="_blank" class="btn btn-primary" id="downloadhref2" href="#" title="">Download Constituents file</a></div>
				
				<div class="col-lg-6 col-xs-6"><a class="btn btn-primary" href="calculations.php">New Calculation </a></div>
			</div>
		
		
		<div class="row" id="resultDiv">

<div class="row">
					<div class="col-lg-12 col-xs-12"><label>All Date's formats are YYYY-MM-DD </label></div>
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
	 if(!empty($finalArray))
{
	
	foreach($finalArray as $k=>$dates){
		foreach($dates as $date=>$data)
{
	  
	 echo ' <div class="row">
			<div class="col-lg-1 col-xs-1">'.($k+1).'</div>					
			<div class="col-lg-2 col-xs-2">'.$date.'</div>
			<div class="col-lg-2 col-xs-2">'.round($data['PR_index_value'],13).'</div>
			<div class="col-lg-2 col-xs-2">'.round($data['TR_index_value'],13).'</div>	
<div class="col-lg-2 col-xs-2">'.round($data['NTR_index_value'],13).'</div>				
			</div>';
	  
	
	
}}}  
	?>	





		</div></div>
		
		<?php require_once("footer.php"); ?>
<script> 
 $(document).ready(function() {
	$("#downloadhref").attr("href","<?php echo $url?>"); 
		$("#downloadhref2").attr("href","<?php echo $url2?>"); 
	$("#downloadhref").attr("title","<?php echo $title?>");
		
 });

</script>