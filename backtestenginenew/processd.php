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
//echo "deepak";
//exit;

if($_POST['SecuritiesWeightJSON'] && $_POST['StartDate'] && $_POST['EndDate'] && $_POST['currency']) {
	
	$SecuritiesWeightJSON=array();
	getTax($TAXDATA);
	$TmpSecuritiesWeightJSON = (array) JSON_decode($_POST['SecuritiesWeightJSON']);
foreach($TmpSecuritiesWeightJSON as $tmpval) {
	$SecuritiesWeightJSON[] = (array) $tmpval;
}
unset($TmpSecuritiesWeightJSON);

$finalArray=array();
if(!empty ($_POST['StartDate']) && !empty ($_POST['EndDate']))
{
	//echo $_POST['period'];
	for($i=0;$i<$_POST['period'];$i++)
	{
		if($i==0)
		{
			$finalArray[$i][date("Y-m-d",strtotime($_POST['StartDate'][$i]))]['PR_mcap']=$investmentvalue;
			$finalArray[$i][date("Y-m-d",strtotime($_POST['StartDate'][$i]))]['PR_index_value']=$index_value;
			$finalArray[$i][date("Y-m-d",strtotime($_POST['StartDate'][$i]))]['PR_divisor']=$divisor;
			$finalArray[$i][date("Y-m-d",strtotime($_POST['StartDate'][$i]))]['TR_mcap']=$investmentvalue;
			$finalArray[$i][date("Y-m-d",strtotime($_POST['StartDate'][$i]))]['TR_index_value']=$index_value;
			$finalArray[$i][date("Y-m-d",strtotime($_POST['StartDate'][$i]))]['TR_divisor']=$divisor;
			$finalArray[$i][date("Y-m-d",strtotime($_POST['StartDate'][$i]))]['NTR_mcap']=$investmentvalue;
			$finalArray[$i][date("Y-m-d",strtotime($_POST['StartDate'][$i]))]['NTR_index_value']=$index_value;
			$finalArray[$i][date("Y-m-d",strtotime($_POST['StartDate'][$i]))]['NTR_divisor']=$divisor;
		}
		
		
		$delisting	= array();
		$cas	= array();
$shares=array();


		$allPrices=getPrices($_POST['StartDate'][$i],$_POST['EndDate'][$i],array_keys($SecuritiesWeightJSON[$i]));
	getCurrencyCombo($allcurrency,$_POST['currency'],$allPrices,$_POST['StartDate'][$i],$_POST['EndDate'][$i]);
	ValidatePrices($allPrices,$_POST['StartDate'][$i],$_POST['EndDate'][$i],$numberofDays,array_keys($SecuritiesWeightJSON[$i]),$delisting);
	ValidateCurrency($allcurrency,$_POST['StartDate'][$i],$_POST['EndDate'][$i],$numberofDays,$_POST['currency']);
	getDividends($cas,$_POST['StartDate'][$i],$_POST['EndDate'][$i],array_keys($SecuritiesWeightJSON[$i]));
	
	//nprint($allcurrency);
	//exit;
	
	if($i==0)
		{
		CalcShare($shares,$SecuritiesWeightJSON[$i],$_POST['StartDate'][$i],$finalArray[$i][date("Y-m-d",strtotime($_POST['StartDate'][$i]))],$allPrices,$allcurrency);
		
		
		}else{
			CalcShare($shares,$SecuritiesWeightJSON[$i],$_POST['StartDate'][$i],$finalArray[$i-1][date('Y-m-d', strtotime($_POST['EndDate'][$i-1]))],$allPrices,$allcurrency);
		}
		
		CalcIndex($allPrices,$allcurrency,$shares,$_POST['StartDate'][$i],$_POST['EndDate'][$i],$i,$finalArray,$delisting,$cas,$TAXDATA);
		
		
		
		
		
		
		}
		
		
		
		
		
		
		
		//nprint($finalArray);

	 $title2 = date('Y-m-d-').time()."_tempreport.csv";
		$filename =dirname(__FILE__)."/csvfiles/".$title2;		
		$srNo = 0;	
		$file =  fopen($filename, 'w');
		
		$header = array("S.No","Date","Index Value PR","Market CAP PR","Divisor PR","Index Value TR","Market CAP TR","Divisor TR","Index Value NTR","Market CAP NTR","Divisor NTR","ISIN","Currency","Country","TAX","Share PR","Share TR","Share NTR","Local Price","USD PRICE","MCAP PR","MCAP TR","MCAP NTR","Currency Price","Price Date","Weight PR","Weight TR","Weight NTR","Dividend","Split","Spin");
		ob_start();
		fputcsv ($file, $header);	
if(!empty($finalArray))
{
	foreach($finalArray as $k=>$dates){
		foreach($dates as $date=>$data)
		{
			foreach($data['Securities'] as  $isind=>$isindata )
			{
				fputcsv ($file, array($k,$date,$data['PR_index_value'],$data['PR_mcap'],$data['PR_divisor'],$data['TR_index_value'],$data['TR_mcap'],$data['TR_divisor'],$data['NTR_index_value'],$data['NTR_mcap'],$data['NTR_divisor'],$isind,$isindata['currencysymbol'],$isindata['country'],$isindata['tax'],$isindata['PR_share'],$isindata['TR_share'],$isindata['NTR_share'],$isindata['localprice'],$isindata['PRUSDPRICE'],$isindata['sprmcap'],$isindata['strmcap'],$isindata['sntrmcap'],$isindata['currency'],$isindata['price_date'],$isindata['PR_weight'],$isindata['TR_weight'],$isindata['NTR_weight'],isset($isindata['ca']['dividend'])?$isindata['ca']['dividend']:"",isset($isindata['ca']['split'])?$isindata['ca']['split']:"",isset($isindata['ca']['spin'])?$isindata['ca']['spin']:""));
			}
		}
	}
}	
		
	fclose($file); 
// $filename; 	
}



$url = "http://204.80.90.133/backtestenginedemo/download.php?file=".$title2;		
		$url2 = "http://204.80.90.133/backtestenginedemo/download.php?file=".$title2;		
		
	
	
}

?>

<div class="container main-body">	
		<div class="row">
				<div class="col-lg-6 col-xs-6"><a target="_blank" class="btn btn-primary" id="downloadhref" href="#" title="">Download Index Values file</a></div>
				<div class="col-lg-6 col-xs-6"><a target="_blank" class="btn btn-primary" id="downloadhref2" href="#" title="">Download Portfolio Output file</a></div>
				<div class="col-lg-6 col-xs-6"><a class="btn btn-primary" href="calculations.php">New Calculation </a></div>
			</div>
		
		
		<div class="row" id="resultDiv"> </div></div>
		
		<?php require_once("footer.php"); ?>
<script> 
 $(document).ready(function() {
	$("#downloadhref").attr("href","<?php echo $url?>"); 
		$("#downloadhref2").attr("href","<?php echo $url2?>"); 
	$("#downloadhref").attr("title","<?php echo $title?>");
		
 });

</script>