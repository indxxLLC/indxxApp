<?php
ob_start();
session_start();
error_reporting(E_ALL & ~E_NOTICE);
require_once("Database.php");

$db = new Database();
$db->connection();

$sqlsvr_details =   array(  'UID'   => 'sa',
							'PWD'           => 'f0r3z@786',
							'Database'      => 'FDS_Datafeeds',
							'CharacterSet'  => 'UTF-8'
						);

// try to connect                    
$connection = sqlsrv_connect("INDXX", $sqlsvr_details);

$userPicturePath = "/backtest_engine/userimages/";


		
$recordsPerPage = 20;
$msg 				= '';
$pageArray 			= array(
							"/backtest_engine/calculations.php",
							"/backtest_engine/process.php" 							
						     
							);
 

 if(isset($_SESSION['userDisplayNamne']) && $_SERVER['PHP_SELF'] == "/backtest_engine/index.php"){
	header("location:calculations.php");
}

if(!isset($_SESSION['userDisplayNamne']) && (in_array($_SERVER['PHP_SELF'],$pageArray))){
	header("location:index.php");
}


if (isset($_POST['login']) && !empty($_POST['username']) 
   && !empty($_POST['password'])) { 
	
	// Remove all illegal characters from email
	$email = $_POST['username'];
	if (!filter_var($email, FILTER_VALIDATE_EMAIL) === false) { 
		
		if(($_POST['username']==='sgoyal@indxx.com' && $_POST['password']==='sgoyal')|| ($_POST['username']==='aagarwal@indxx.com' && $_POST['password']==='aagarwal') || ($_POST['username']==='apoddar@indxx.com' && $_POST['password']==='apoddar') || ($_POST['username']==='adityak@indxx.com' && $_POST['password']==='adityak') || ($_POST['username']==='pjohn@indxx.com' && $_POST['password']==='Prad123!')|| ($_POST['username']==='hsinghal@indxx.com' && $_POST['password']==='hsinghal') || ($_POST['username']==='srajvanshi@indxx.com' && $_POST['password']==='shubhangi') || ($_POST['username']==='kghildya@indxx.com' && $_POST['password']==='kunal')) {		
			$_SESSION['userDisplayNamne'] = $_POST['username']; 
			$_POST['username'] === 'srajvanshi@indxx.com'?$_SESSION['userDisplaySex'] = $sex =  "F":$_SESSION['userDisplaySex'] = $sex =  "M";
			$picture = '';
			
			if($picture)
			$_SESSION['userDisplayPic'] = $picture; 
			else {
				if($sex==='M') 
					$_SESSION['userDisplayPic'] = $userPicturePath."male.png";
				else
					$_SESSION['userDisplayPic'] = $userPicturePath."female.jpg";
			}
			header("location:calculations.php");
		} else {
			$msg = 'Wrong username or password. Please try again.';
			session_unset();	
		}
	}else {
		$msg = "$email is not a valid email address";
		session_unset();	
	}
			
}
	
   


  