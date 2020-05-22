<?php
error_reporting(E_ALL);
$sqlsvr_details =   array(  'UID'   => 'sa',
							'PWD'           => 'f0r3z@786',
							'Database'      => 'FDS_Datafeeds',
							'CharacterSet'  => 'UTF-8'
						);

// try to connect                    
 $connection = sqlsrv_connect("INDXX", $sqlsvr_details);
if( $connection === false ) {
     die( print_r( sqlsrv_errors(), true));
}

function ValidateDividends($delisting,&$cas){
	//nprint($delisting);
	//nprint($cas);
	
	if(!empty($delisting)){
	foreach($delisting as $date => $isins )
	{
	foreach($isins as $isin)
	{
		foreach($cas as $cadate => $cadata)
		{
			///nprint(array_keys($cadata));
	if(in_array($isin,array_keys($cadata)) && strtotime($cadate)>=strtotime($date))
		unset($cas[$cadate][$isin]);
		}		
	}

	
	}
	}
	//exit;
}

function getTax(&$TAXDATA, $taxRateFile){
	
if($taxRateFile['error']!=0 ){
		
		//echo "a";
		//exit;
	global $connection;
	$taxqry = " SELECT ba.tax ,ba.Country ,ca.iso_country from FDS_DataFeeds.dbo.tax_rate ba left join FDS_DataFeeds.ref_v2.country_map ca on ba.Country=ca.country_desc ";
				
				//echo $qry;
				//exit;
				
				$taxres = sqlsrv_query( $connection, $taxqry );
				
				
					
				while( $record = sqlsrv_fetch_array( $taxres, SQLSRV_FETCH_ASSOC) ) {
					$TAXDATA[$record['Country']]=$record['tax'];
	}}else{
		
		//echo "b";
		//exit;
		
		$Readfile 		= fopen($taxRateFile['tmp_name'], 'r');
		while (($line = fgetcsv($Readfile)) !== FALSE) {
			$TAXDATA[$line[0]]=$line[1];
		}
	}
}

function CalcIndex($allPrices,$allcurrency,&$shares,$StartDate,$endDate,$i,&$finalArray,$delisting,&$cas,&$TAXDATA,$spinoff){
	
		//nprint($allcurrency);
	$dates=getDatesFromRange($StartDate,$endDate);
	 foreach($dates as  $k=> $date){
		 $PR_divisor=0;
		  $TR_divisor=0;
		   $NTR_divisor=0;
		 $sumPR=0;
		 $IndexPR=0;
		 $sumTR=0;
		 $IndexTR=0;
		 $sumNTR=0;
		 $IndexNTR=0;
		 
		
		 
		if($i==0 && $k==0 && date("Y-m-d",strtotime($StartDate))==date("Y-m-d",strtotime($date)))
		{
		//	echo "first daz". $date;
		
		 $PR_divisor=$finalArray[$i][date("Y-m-d",strtotime($date))]['PR_divisor'];
		 		 $IndexPR=$finalArray[$i][date("Y-m-d",strtotime($date))]['PR_index_value'];
				 
				 $TR_divisor=$finalArray[$i][date("Y-m-d",strtotime($date))]['TR_divisor'];
		 		 $IndexTR=$finalArray[$i][date("Y-m-d",strtotime($date))]['TR_index_value'];
				 
				 $NTR_divisor=$finalArray[$i][date("Y-m-d",strtotime($date))]['NTR_divisor'];
		 		 $IndexNTR=$finalArray[$i][date("Y-m-d",strtotime($date))]['NTR_index_value'];
		}elseif($i!=0 && $k==0 && date("Y-m-d",strtotime($StartDate))==date("Y-m-d",strtotime($date))){
			
			//echo "Reconstitution day". $date;
			$PR_divisor=$finalArray[$i-1][date("Y-m-d",strtotime($date))]['PR_divisor'];
			$IndexPR=$finalArray[$i-1][date("Y-m-d",strtotime($date))]['PR_index_value'];
			
			 $TR_divisor=$finalArray[$i-1][date("Y-m-d",strtotime($date))]['TR_divisor'];
		 		 $IndexTR=$finalArray[$i-1][date("Y-m-d",strtotime($date))]['TR_index_value'];
				 
				 $NTR_divisor=$finalArray[$i-1][date("Y-m-d",strtotime($date))]['NTR_divisor'];
		 		 $IndexNTR=$finalArray[$i-1][date("Y-m-d",strtotime($date))]['NTR_index_value'];
			
		}
		else{
			//echo "other daY daz". $date;
			$PR_divisor=$finalArray[$i][date('Y-m-d', strtotime("-1 day", strtotime($date)))]['PR_divisor'];
			$IndexPR=$finalArray[$i][date('Y-m-d', strtotime("-1 day", strtotime($date)))]['PR_index_value'];
			
			
			$TR_divisor=$finalArray[$i][date('Y-m-d', strtotime("-1 day", strtotime($date)))]['TR_divisor'];
		 		 $IndexTR=$finalArray[$i][date('Y-m-d', strtotime("-1 day", strtotime($date)))]['TR_index_value'];
				 
				 $NTR_divisor=$finalArray[$i][date('Y-m-d', strtotime("-1 day", strtotime($date)))]['NTR_divisor'];
		 		 $IndexNTR=$finalArray[$i][date('Y-m-d', strtotime("-1 day", strtotime($date)))]['NTR_index_value'];
			
		}
		if(!empty($delisting)){
		if(array_key_exists($date,$delisting)){
			$delistingsumPR=0;
			$delistingsumTR=0;
			$delistingsumNTR=0;
			foreach($delisting[$date] as $disin){
				//nprint($disin);
				
				
				$delistingsumPR+=($shares['PR'][$disin]*($allPrices[$disin][date("Y-m-d", strtotime("-1 day", strtotime($date)))]['price']/$allcurrency[$allPrices[$disin][date("Y-m-d", strtotime("-1 day", strtotime($date)))]['date']][$allPrices[$disin][date("Y-m-d",strtotime("-1 day",strtotime($date)))]['currency']]))	;
				unset($shares['PR'][$disin]);
				$delistingsumTR+=($shares['TR'][$disin]*($allPrices[$disin][date("Y-m-d", strtotime("-1 day", strtotime($date)))]['price']/$allcurrency[$allPrices[$disin][date("Y-m-d", strtotime("-1 day", strtotime($date)))]['date']][$allPrices[$disin][date("Y-m-d",strtotime("-1 day",strtotime($date)))]['currency']]))	;
				unset($shares['TR'][$disin]);
				$delistingsumNTR+=($shares['NTR'][$disin]*($allPrices[$disin][date("Y-m-d", strtotime("-1 day", strtotime($date)))]['price']/$allcurrency[$allPrices[$disin][date("Y-m-d", strtotime("-1 day", strtotime($date)))]['date']][$allPrices[$disin][date("Y-m-d",strtotime("-1 day",strtotime($date)))]['currency']]))	;
				unset($shares['NTR'][$disin]);
			}
			/////delisting code 
			
			$PR_divisor=$PR_divisor-($delistingsumPR/$IndexPR);
			$TR_divisor=$TR_divisor-($delistingsumTR/$IndexTR);
			$NTR_divisor=$NTR_divisor-($delistingsumNTR/$IndexNTR);
		}
		}
		
		
		if(!empty($shares['PR'])){
			if(array_key_exists($date,$cas))
			{
				 if($i==0 && $k==0 && date("Y-m-d",strtotime($StartDate))==date("Y-m-d",strtotime($date)))
		{}elseif($i!=0 && $k==0 && date("Y-m-d",strtotime($StartDate))==date("Y-m-d",strtotime($date)))
				 {}else{
				foreach($cas[$date] as $isin=>$ca2 ){
 $finalArray[$i][$date]['Securities'][$isin]['ca']=$ca2;				
				
					$shareimpact=1;
					$priceimpact=1;
					foreach($ca2 as $type=>$ca){
					//$finalArray[$i][$date]['Securities'][$isin]['ca']['dividend'][]=$ca['dividend']." ".$ca['currency'];
					
					$base_price=$allPrices[$isin][date("Y-m-d",strtotime("-1 day", strtotime($date)))]['price'];
					//$divisorimpact=0;
		 if(in_array($type,array(11,134)))
		
		{
					//nprint($ca);
						$newPrice=$base_price-$ca['dividend'];
						 $priceimpact= $priceimpact*($newPrice/$base_price);
						 
						$PR_divisor=$PR_divisor-((($ca['dividend']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime("-1 day", strtotime($date)))]['date']][$allPrices[$isin][date("Y-m-d",strtotime("-1 day", strtotime($date)))]['currency']])*$shares['PR'][$isin])/$IndexPR); 
										
		}
		
		//echo $isin."-".$date;
		//nprint($type);
		//nprint($ca);
		if(is_array($ca)){
				if(array_key_exists('spin',$ca) && $ca['spin']==1)
					{
						
						
						$newPrice=$base_price-$ca['dividend'];
						 $priceimpact= $priceimpact*($newPrice/$base_price);
						if($spinoff){
							$shareimpact=$shareimpact*(1/$priceimpact);
						}else{ 
						$PR_divisor=$PR_divisor-((($ca['dividend']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime("-1 day", strtotime($date)))]['date']][$allPrices[$isin][date("Y-m-d",strtotime("-1 day", strtotime($date)))]['currency']])*$shares['PR'][$isin])/$IndexPR); 
		}}}
					}
					
					
					if(array_key_exists('split',$ca2))
					{
						$newPrice=$base_price*$ca2['split'];
						 $priceimpact= $priceimpact/($newPrice/$base_price);
						 $newShare=$shares['PR'][$isin]/$ca2['split'];
						 $shareimpact=$shareimpact*($newShare/$shares['PR'][$isin]);
					}
					
					$shares['PR'][$isin]=$shares['PR'][$isin]*$shareimpact;
					//$allPrices[$isin][date("Y-m-d",strtotime($date))]['new_price']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['price']*$priceimpact;
				}
			}
			
			}
			
			
			

			foreach($shares['PR'] as $isin=>$share){
				$sumPR+=round(($share*$allPrices[$isin][date("Y-m-d",strtotime($date))]['price']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']]),13);
			
		$finalArray[$i][$date]['Securities'][$isin]['tax']=$TAXDATA[$allPrices[$isin][date("Y-m-d",strtotime($date))]['country']];
		$finalArray[$i][$date]['Securities'][$isin]['country']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['country'];
		//$finalArray[$i][$date]['Securities'][$isin]['adj_PR_price']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['new_price'];
		$finalArray[$i][$date]['Securities'][$isin]['currencysymbol']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency'];
		$finalArray[$i][$date]['Securities'][$isin]['localprice']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['price'];
		$finalArray[$i][$date]['Securities'][$isin]['price_date']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['date'];
		 $finalArray[$i][$date]['Securities'][$isin]['PR_share']=$share;
		
		$finalArray[$i][$date]['Securities'][$isin]['currency']=$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']];
		$finalArray[$i][$date]['Securities'][$isin]['sprmcap']=round(($share*($allPrices[$isin][date("Y-m-d",strtotime($date))]['price']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']])),13);
		 $finalArray[$i][$date]['Securities'][$isin]['PRUSDPRICE']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['price']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']];
		
		}
		
		
		$finalArray[$i][$date]['PR_mcap']=round($sumPR,13);
		$finalArray[$i][$date]['PR_divisor']=$PR_divisor;
		$finalArray[$i][$date]['PR_index_value']=round($sumPR/$PR_divisor,13);
		}
		
		else{
			$finalArray[$i][$date]=$finalArray[$i][date("Y-m-d",strtotime("-1 day", strtotime($date)))];
		}
		
		if(!empty($shares['TR'])){
			
			
			
			if(array_key_exists($date,$cas))
			{ if($i==0 && $k==0 && date("Y-m-d",strtotime($StartDate))==date("Y-m-d",strtotime($date)))
		{}elseif($i!=0 && $k==0 && date("Y-m-d",strtotime($StartDate))==date("Y-m-d",strtotime($date)))
				 {}else{
				 
				
				foreach($cas[$date] as $isin=>$ca2 ){
					
					$shareimpact=1;
					$priceimpact=1;
					//$divisorimpact=0;
		 
		 foreach($ca2 as $type=>$ca){
					$base_price=$allPrices[$isin][date("Y-m-d",strtotime("-1 day", strtotime($date)))]['price'];
					if(is_array($ca)){
					if(array_key_exists('dividend',$ca))
					{
						$newPrice=$base_price-$ca['dividend'];
						 $priceimpact= $priceimpact*($newPrice/$base_price);
					if(array_key_exists('spin',$ca) && $ca['spin']==1  && $spinoff==1)
					{
							$shareimpact=$shareimpact*(1/$priceimpact);
					}
					else{
						
			
						
						
						 
						$TR_divisor=$TR_divisor-((($ca['dividend']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime("-1 day", strtotime($date)))]['date']][$allPrices[$isin][date("Y-m-d",strtotime("-1 day", strtotime($date)))]['currency']])*$shares['TR'][$isin])/$IndexTR); 
					}
						
					}
					}
		 }
		 
		 
	//nprint($ca)	;
	if(is_array($ca2)){
	
			if(array_key_exists('split',$ca2))
					{
						$newPrice=$base_price*$ca2['split'];
						 $priceimpact= $priceimpact*($newPrice/$base_price);
						 $newShare=$shares['TR'][$isin]/$ca2['split'];
						 $shareimpact=$shareimpact*($newShare/$shares['TR'][$isin]);
					}
		 }
					$shares['TR'][$isin]=$shares['TR'][$isin]*$shareimpact;
				//	$allPrices[$isin][date("Y-m-d",strtotime($date))]['new_price']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['price']*$priceimpact;
				}
			}}
			
			
			
			
			foreach($shares['TR'] as $isin=>$share){
				$sumTR+=round(($share*($allPrices[$isin][date("Y-m-d",strtotime($date))]['price']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']])),13)	;
		
		
	//$finalArray[$i][$date]['Securities'][$isin]['adj_TR_price']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['new_price'];
		$finalArray[$i][$date]['Securities'][$isin]['TR_share']=$share;
		$finalArray[$i][$date]['Securities'][$isin]['strmcap']=round(($share*($allPrices[$isin][date("Y-m-d",strtotime($date))]['price']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']])),13);
		$finalArray[$i][$date]['Securities'][$isin]['TRUSDPRICE']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['price']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']];
		
		}
		
		
		$finalArray[$i][$date]['TR_mcap']=round($sumTR,13);
		$finalArray[$i][$date]['TR_divisor']=$TR_divisor;
		$finalArray[$i][$date]['TR_index_value']=round($sumTR/$TR_divisor,13);
		}
		
		else{
			$finalArray[$i][$date]=$finalArray[$i][date("Y-m-d",strtotime("-1 day", strtotime($date)))];
		}
		
		
		
		if(!empty($shares['NTR'])){
			
			
			if(array_key_exists($date,$cas))
			{
				if($i==0 && $k==0 && date("Y-m-d",strtotime($StartDate))==date("Y-m-d",strtotime($date)))
		{}elseif($i!=0 && $k==0 && date("Y-m-d",strtotime($StartDate))==date("Y-m-d",strtotime($date)))
				 {}else{ 
				
				foreach($cas[$date] as $isin=>$ca2 ){
					
					$shareimpact=1;
					$priceimpact=1;
					//$divisorimpact=0;
		 
		 
					$base_price=$allPrices[$isin][date("Y-m-d",strtotime("-1 day", strtotime($date)))]['price'];
					foreach($ca2 as $type=>$ca){
						if(is_array($ca)){
						
					if(array_key_exists('dividend',$ca))
					{
						
						if(array_key_exists('spin',$ca) && $ca['spin']==1)
					{
						$ca['dividend']=$ca['dividend'];
					}else
					{$ca['dividend']=$ca['dividend']*(1-(str_replace("%","",$TAXDATA[$allPrices[$isin][date("Y-m-d",strtotime($date))]['country']])/100));
					}
						
						$newPrice=$base_price-$ca['dividend'];
						 $priceimpact= $priceimpact*($newPrice/$base_price);
						 
						 
						 if(array_key_exists('spin',$ca) && $ca['spin']==1  && $spinoff==1)
					{
							$shareimpact=$shareimpact*(1/$priceimpact);
					}
					else{
						
						 
						 
						$NTR_divisor=$NTR_divisor-((($ca['dividend']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime("-1 day", strtotime($date)))]['date']][$allPrices[$isin][date("Y-m-d",strtotime("-1 day", strtotime($date)))]['currency']])*$shares['NTR'][$isin])/$IndexNTR) ;
					}
						}
						}
					}
					if(is_array($ca2)){
					if(array_key_exists('split',$ca2))
					{
						$newPrice=$base_price*$ca2['split'];
						 $priceimpact= $priceimpact*($newPrice/$base_price);
						 $newShare=$shares['NTR'][$isin]/$ca2['split'];
						 $shareimpact=$shareimpact*($newShare/$shares['NTR'][$isin]);
					}
					}
					$shares['NTR'][$isin]=$shares['NTR'][$isin]*$shareimpact;
					//$allPrices[$isin][date("Y-m-d",strtotime($date))]['new_price']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['price']*$priceimpact;
				}
			}
			}
			
			
			
			
			
			foreach($shares['NTR'] as $isin=>$share){
				$sumNTR+=round(($share*($allPrices[$isin][date("Y-m-d",strtotime($date))]['price']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']])),13)	;
		
		
	//$finalArray[$i][$date]['Securities'][$isin]['adj_NTR_price']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['new_price'];
		$finalArray[$i][$date]['Securities'][$isin]['NTR_share']=$share;
		$finalArray[$i][$date]['Securities'][$isin]['sntrmcap']=round(($share*($allPrices[$isin][date("Y-m-d",strtotime($date))]['price']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']])),13)	;
		$finalArray[$i][$date]['Securities'][$isin]['NTRUSDPRICE']=$allPrices[$isin][date("Y-m-d",strtotime($date))]['price']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']];
		}
		
		//nprint($finalArray);
		//exit;
		$finalArray[$i][$date]['NTR_mcap']=round($sumNTR,13);
		$finalArray[$i][$date]['NTR_divisor']=$NTR_divisor;
		$finalArray[$i][$date]['NTR_index_value']=round($sumNTR/$NTR_divisor,13);
		}
		
		else{
			$finalArray[$i][$date]=$finalArray[$i][date("Y-m-d",strtotime("-1 day", strtotime($date)))];
		}
		$final_arr = $finalArray[$i][$date]['Securities'];
		foreach($final_arr as $isin=>$data){
			
			$finalArray[$i][$date]['Securities'][$isin]['PR_weight']=($data['PR_share']*($data['localprice']/$data['currency']))/$finalArray[$i][$date]['PR_mcap'];
			$finalArray[$i][$date]['Securities'][$isin]['TR_weight']=($data['TR_share']*($data['localprice']/$data['currency']))/$finalArray[$i][$date]['TR_mcap'];
			$finalArray[$i][$date]['Securities'][$isin]['NTR_weight']=($data['NTR_share']*($data['localprice']/$data['currency']))/$finalArray[$i][$date]['NTR_mcap'];
			
		}
		
		
		
		// file_put_contents('csvfiles/log_'.date("j.n.Y").'.txt', "Calculation done for ".$date."-".$i."\n", FILE_APPEND);	
		
	 }
	
 
	
}

function CalcShare(&$shares,$SecuritiesWeight,$date,$finalArray,&$allPrices,&$allcurrency)
{
	//nprint($SecuritiesWeight);
	//exit;
	// print_r($allPrices);
//die;
	 foreach($SecuritiesWeight as $isin=>$weight){
		 
 $shares['NTR'][$isin]=round(( $finalArray['NTR_mcap'] * ( $weight / 100 ) ) / ($allPrices[$isin][date("Y-m-d",strtotime($date))]['price']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']]),13);		
		$shares['TR'][$isin]=round(( $finalArray['TR_mcap'] * ( $weight / 100 ) ) / ($allPrices[$isin][date("Y-m-d",strtotime($date))]['price']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']]),13);
		 $shares['PR'][$isin]=round(( $finalArray['PR_mcap'] * ( $weight / 100 ) ) / ($allPrices[$isin][date("Y-m-d",strtotime($date))]['price']/$allcurrency[$allPrices[$isin][date("Y-m-d",strtotime($date))]['date']][$allPrices[$isin][date("Y-m-d",strtotime($date))]['currency']]),13);
		 
	 
	 }
}


 function getDatesFromRange($start, $end, $format = 'Y-m-d') {
    $array = array();
    $interval = new DateInterval('P1D');

    $realEnd = new DateTime($end);
    $realEnd->add($interval);

    $period = new DatePeriod(new DateTime($start), $interval, $realEnd);

    foreach($period as $date) { 
        $array[] = $date->format($format); 
    }

    return $array;
}



function ValidateCurrency(&$allcurrency,$startDate,$endDate,$numberofDays,$sourse)
{ $dates=getDatesFromRange($startDate,$endDate);
	 foreach($dates as $date){
		 //
		 
	 if(!array_key_exists($date,$allcurrency))
		 {
			 $flag=false;
					 for ($i=0;$i<$numberofDays; $i++)
					{
						if(array_key_exists($date,$allcurrency))
						{
								
								$allcurrency[$date]=$allcurrency[date('Y-m-d', strtotime("-".($i+1)." day", strtotime($date)))];
								$flag=true;
							break;
						}
						
						
					}
		 }
		
		 
		 
		
	 }

	
}
function ValidatePrices(&$allPrices,$startDate,$endDate,$numberofDays,$isins,&$delisting){
 
  $dates=getDatesFromRange($startDate,$endDate);
 foreach($allPrices as $isin=>$price){

	  if ((date("Y-m-d",strtotime(max(array_keys($price)))) >= date("Y-m-d",strtotime($startDate))) && (date("Y-m-d",strtotime(max(array_keys($price)))) <= date("Y-m-d",strtotime($endDate))))
    {
     $delisting[date("Y-m-d",strtotime("+1 day",strtotime(max(array_keys($price)))))][]=$isin;
    }
	 foreach($dates as $date){
		 if(!array_key_exists($date,$price))
		 {		 for ($i=0;$i<$numberofDays; $i++)
					{
						if(array_key_exists(date('Y-m-d', strtotime("-".($i+1)." day", strtotime($date))),$price))
						{
								
								$allPrices[$isin][$date]=$allPrices[$isin][date('Y-m-d', strtotime("-".($i+1)." day", strtotime($date)))];
								$flag=true;
							break;
						}
						
					}

			 
		 }

		


	 }
	 
	
 }
 
}
 function ValidatePrices_old(&$allPrices,$startDate,$endDate,$numberofDays,$isins){
	 $dates=getDatesFromRange($startDate,$endDate);
	 foreach($dates as $date){
		 if(array_key_exists($date,$allPrices))
		 {
			foreach($isins as  $isink=> $isin){
				if(!array_key_exists($isin,$allPrices[$date]))
				{$flag=false;
					 for ($i=0;$i<$numberofDays; $i++)
					{
						if(array_key_exists($isin,$allPrices[date('Y-m-d', strtotime("-".($i+1)." day", strtotime($date)))]))
						{
								
								$allPrices[$date][$isin]=$allPrices[date('Y-m-d', strtotime("-".($i+1)." day", strtotime($date)))][$isin];
								$flag=true;
							break;
						}
						
						
					}
					
					if(!$flag){
					echo "historical Price not available for ".$isin ." on ".$date." so Go to DB <br>";
					}
				}else{
				$flag=true;
					for ($i=0;$i<$numberofDays; $i++)
					{   
				//nprint($isin);
				//nprint($allPrices[date('Y-m-d', strtotime("+".($i+1)." day", strtotime($date)))]);
				
						if(!array_key_exists($isin,$allPrices[date('Y-m-d', strtotime("+".($i+1)." day", strtotime($date)))]))
						{
							$flag=false;
							
							//echo $isin." ".date('Y-m-d', strtotime("+".($i+1)." day", strtotime($date)))." ".$date."<br>";
							
						}else{
							
							//echo "Price  available for ".$isin ." on next day of ".$date." for ".date('Y-m-d', strtotime('+'.($i+1).' day', $date))." so assign the last available price <br>";
							$flag=true;
							break;
						}
					}
					
					
				if(!$flag)
				{
					
					$allPrices[date('Y-m-d', strtotime("+1 day", strtotime($date)))][$isin]['DELISTING']=TRUE;
					//echo "delisting found for ".$isin." on ".$date."<br>";
					unset($isins[$isink]);
				}
					
				}
				
			}
			
			 
			 
		 }else{
			 
			 if(!getPreviousDayPrices($date,$allPrices,$numberofDays,$isins))
			 {
				 echo "price not available for date ".$date."  Go to DB<br>"; 
				 
			 }
		
		 }
		 
		 
		 
		 
	 }
	 
	 
	 
	 
	 
	 
	 
	 
	 
	 
	 
 }
 
 

 
function  getPreviousDayPrices($date,&$allPrices,$numberofDays,$isins){
	
$flag=false;
	for ($i=0;$i<$numberofDays; $i++)
	{
		$date1=date('Y-m-d', strtotime("-".($i+1)." day", strtotime($date)));
		foreach($isins as  $isink=> $isin){
				if(!array_key_exists($isin,$allPrices[$date1]))
				{
					getPreviousDayPrices($date1,$allPrices,$numberofDays,$isins);
				}else{
					$allPrices[$date]=$allPrices[$date1];
					
					$flag=true;
					break;
				}
	}
}



return $flag;
}

			 
 function nprint($array)
 {
	 echo "<pre>";
	 print_r($array);
	 echo "</pre>";
 } 
 
 function getCurrencyCombo(&$allcurrency,$source,&$pricearray,$startDate,$endDate)
{global $connection;
	
	
	$currency=array();
	 // $currency[]
	
	if(!empty($pricearray))
	{
		foreach($pricearray as $date)
		{
			
			if(!empty($date)){
			foreach($date as $isin)
			{
			if (!in_array($isin['currency'], $currency)&& $source!=$isin['currency'])
			  {
			  $currency[]=$isin['currency'];
			  }
			}
			}
		}
	}
	
	
	//nprint( $currency);
	//nprint( $pricearray);
	
	
	
	
	$qry = "SELECT RTS.iso_currency, RTS.date, RTS.exch_rate_usd, RTS.exch_rate_per_usd"; 
		$qry .= " FROM FDS_DataFeeds.ref_v2.fx_rates_usd  AS RTS"; 			
		$qry .= " WHERE RTS.date between '".date('Y-m-d', strtotime("-5 day", strtotime($startDate)))."' and '".date('Y-m-d', strtotime("+5 day", strtotime($endDate))) ."'";	
		$qry .= " and RTS.iso_currency in ( ". "'" . implode ( "', '", $currency ) . "'".")";			
		$qry .= " ORDER BY RTS.date ";
		//echo $qry;
		//exit;
	
	$count=0;
	
		$d = sqlsrv_query( $connection, $qry );	
		
		while( $record = sqlsrv_fetch_array( $d, SQLSRV_FETCH_ASSOC) ) {
			
		$DBdatArray = (array) $record['date'];
		
		$allcurrency[date( 'Y-m-d', strtotime($DBdatArray['date']) )][$record['iso_currency']]=$record['exch_rate_per_usd'];
		 $allcurrency[date( 'Y-m-d', strtotime($DBdatArray['date']) )][$source]=1;
		
			$count++;
		}

		
		
		
		if($count==0){
		$allcurrency[date('Y-m-d', strtotime("-5 day", strtotime($startDate)))][$source]=1;
		$allcurrency[date('Y-m-d', strtotime("-4 day", strtotime($startDate)))][$source]=1;
		$allcurrency[date('Y-m-d', strtotime("-3 day", strtotime($startDate)))][$source]=1;
		$allcurrency[date('Y-m-d', strtotime("-2 day", strtotime($startDate)))][$source]=1;
		$allcurrency[date('Y-m-d', strtotime("-1 day", strtotime($startDate)))][$source]=1;
		
		$dates=getDatesFromRange($startDate,$endDate);
	 foreach($dates as $date){
		 $allcurrency[$date][$source]=1;
		 
		 
	 }
		
		
		}
		
		
		
	//return $currencyarray;
}


function getDividends(&$cas,$startDate,$endDate,$isins){
	global $connection;
	
	/*$qry="SELECT c.isin, a.p_divs_pd,a.currency,p_divs_pd_type_code,p_divs_exdate,p_divs_pd_id
  FROM [FDS_DataFeeds].[fp_v2].[fp_basic_dividends] a 
   join [FDS_DataFeeds].[sym_v1].[sym_coverage] b
   on a.fsym_id = b.fsym_id
   join [FDS_DataFeeds].[sym_v1].[sym_isin] c
  on b.fsym_security_id = c.fsym_id
where c.isin  in  ("."'" . implode ( "', '", $isins ) . "'".") and p_divs_exdate  between '".$startDate."' and '".$endDate ."'";*/

	// Query New 1
	$qry = "SELECT DIV.*,DIV.p_divs_exdate as date ,ISN.isin
			 FROM FDS_DataFeeds.fp_v2.fp_basic_dividends  AS DIV 
			 inner join [sym_v1].[sym_coverage] c on DIV.fsym_id = c.fsym_regional_id
			 inner join [sym_v1].[sym_isin] ISN  on c.fsym_id=ISN.fsym_id";
	$qry .= " WHERE ISN.isin in  ("."'" . implode ( "', '", $isins ) . "'".")  AND  DIV.p_divs_exdate between '".$startDate."' and '".$endDate ."'";	
	$qry .= " ORDER BY ISN.isin, DIV.p_divs_exdate";
			 
	// Query Old 1		 
	/*$qry = "SELECT DIV.p_divs_pd , DIV.currency,DIV.date , DIV.p_divs_s_spinoff, DIV.fs_perm_sec_id, DIV.p_divs_pd_type_code,ISN.isin"; 
			$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_dividends_det  AS DIV"; 
			$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
			$qry .= " ON DIV.fs_perm_sec_id = CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
			$qry .= " WHERE ISN.isin in  ("."'" . implode ( "', '", $isins ) . "'".")  AND  DIV.date between '".$startDate."' and '".$endDate ."'";							
			$qry .= " ORDER BY ISN.isin, DIV.date ";*/
		
			$b = sqlsrv_query( $connection, $qry );
		//echo $qry	;
		//exit;
			
			
			$Divcount= 0;
			if(count($b) >0)
			{
				while( $record = sqlsrv_fetch_array( $b, SQLSRV_FETCH_ASSOC) ) {
					$DBdatArray = (array) $record['date'];
					//$record['isin']
					$cas[date( 'Y-m-d', strtotime($DBdatArray['date']) )][$record['isin']][$record['p_divs_pd_type_code']]['dividend']=$record['p_divs_pd'];
					$cas[date( 'Y-m-d', strtotime($DBdatArray['date']) )][$record['isin']][$record['p_divs_pd_type_code']]['spin']=$record['p_divs_s_spinoff'];
					$cas[date( 'Y-m-d', strtotime($DBdatArray['date']) )][$record['isin']][$record['p_divs_pd_type_code']]['currency']=$record['currency'];
					$cas[date( 'Y-m-d', strtotime($DBdatArray['date']) )][$record['isin']][$record['p_divs_pd_type_code']]['type']=$record['p_divs_pd_type_code'];				
				}
			}
	//Query New 2
	$qry = "SELECT a.*,a.p_split_date as date, b.isin 
			FROM [fp_v2].[fp_basic_splits] a
			inner join [sym_v1].[sym_coverage] c on a.fsym_id=c.fsym_regional_id
			inner join [sym_v1].[sym_isin] b on c.fsym_id=b.fsym_id";
	$qry .= " WHERE b.isin in  ("."'" . implode ( "', '", $isins ) . "'".")  
			AND  a.p_split_date between '".$startDate."' and '".$endDate ."'";	
	$qry .= " ORDER BY b.isin, a.p_split_date";

	
	// Query Old 2
	/*$qry = "SELECT SPT.p_split_factor, SPT.date, SPT.fs_perm_sec_id, ISN.isin"; 
			$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_splits  AS SPT"; 
			$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
			$qry .= " ON SPT.fs_perm_sec_id = CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
			$qry .= " WHERE ISN.isin in  ("."'" . implode ( "', '", $isins ) . "'".")  AND  SPT.date between '".$startDate."' and '".$endDate ."'";							
			$qry .= " ORDER BY ISN.isin, SPT.date ";*/
			//echo $qry;
			//exit;
			$c = sqlsrv_query( $connection, $qry );
			$Divcount= 0;
			//print_r(count($c));
			if(count($c) >0)
			{
				while( $record = sqlsrv_fetch_array( $c, SQLSRV_FETCH_ASSOC) ) {
					$DBdatArray = (array) $record['date'];
					//$record['isin']
					$cas[date( 'Y-m-d', strtotime($DBdatArray['date']) )][$record['isin']]['split']=$record['p_split_factor'];
				}
			}
	
	
			
}

	function getPrices($StartDate,$endDate,$isins,$country)
	{ global $connection;
		$pricearray=array();
		
		//Query New 3
		$qry = "select a.*,a.p_date as date, b.isin";
			$qry .= " from fp_v2.fp_basic_prices a";			
			$qry .= " inner join sym_v1.sym_coverage c on a.fsym_id=c.fsym_regional_id";
			$qry .= " inner join sym_v1.sym_isin b on c.fsym_id=b.fsym_id";
			$qry .= " WHERE b.isin in  (". "'" . implode ( "', '", $isins ) . "'".")  AND  a.p_date between '".date('Y-m-d', strtotime("-5 day", strtotime($StartDate)))."' and '".date('Y-m-d', strtotime($endDate)) ."'";						
			$qry .= " ORDER BY b.isin, a.p_date ";
			
		//Query Old 3
			/*$qry = "SELECT PRC.p_price , PRC.currency,PRC.date , PRC.fs_perm_sec_id,ISN.isin"; 
			$qry .= " FROM FDS_DataFeeds.fp_v1.fp_basic_bd  AS PRC"; 
			$qry .= " JOIN FDS_DataFeeds.ids_v1.h_security_isin AS ISN"; 	
			$qry .= " ON PRC.fs_perm_sec_id =CASE WHEN ISN.fs_primary_listing_id IS NULL THEN ISN.fs_primary_equity_id ELSE ISN.fs_primary_listing_id END";
			$qry .= " WHERE ISN.isin in  (". "'" . implode ( "', '", $isins ) . "'".")  AND  PRC.date between '".date('Y-m-d', strtotime("-5 day", strtotime($StartDate)))."' and '".date('Y-m-d', strtotime("+5 day", strtotime($endDate))) ."'";						
			$qry .= " ORDER BY ISN.isin, PRC.date ";*/
			
			//echo $qry;
			//exit;
			
			$a = sqlsrv_query( $connection, $qry );
			
			$count= 0;
				
			while( $record = sqlsrv_fetch_array( $a, SQLSRV_FETCH_ASSOC) ) {
				$DBdatArray = (array) $record['date'];
				
				
				
				
				
				//$record['isin']
				$pricearray[$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['date']=date( 'Y-m-d', strtotime($DBdatArray['date']) );
				$pricearray[$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['price']=$record['p_price'];
				$pricearray[$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['new_price']=$record['p_price'];
				$pricearray[$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['currency']=$record['currency'];
				$pricearray[$record['isin']][date( 'Y-m-d', strtotime($DBdatArray['date']) )]['country']=$country[$record['isin']];
			
			
			
			}
	
			return $pricearray;
	}	
	