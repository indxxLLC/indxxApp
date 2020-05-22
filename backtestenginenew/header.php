<?php
require_once("userdetials.php");
?>
<!DOCTYPE html>
<html lang="en">
  <head>
 <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>Back Test Engine </title>
  <!-- Tell the browser to be responsive to screen width -->
  <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
  <!-- Bootstrap 3.3.6 -->
  <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
  <!-- Font Awesome -->
  <link rel="stylesheet" href="css/font-awesome.min.css">

  <!-- Theme style -->
  <link rel="stylesheet" href="dist/css/AdminLTE.css">

  <!-- AdminLTE Skins. Choose a skin from the css/skins
       folder instead of downloading all of them to reduce the load. -->
  <link rel="stylesheet" href="dist/css/skins/_all-skins.min.css">  
 
  <!-- Date Picker -->
  <link rel="stylesheet" href="plugins/datepicker/datepicker3.css">
  <!-- Daterange picker -->
  <link rel="stylesheet" href="plugins/daterangepicker/daterangepicker.css">
 

  <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
  <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
  <!--[if lt IE 9]>
  <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
  <![endif]-->

    <!-- Le fav and touch icons -->
    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="http://www.indxx.com/images/favicon.ico">
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="http://www.indxx.com/images/favicon.ico">
      <link rel="apple-touch-icon-precomposed" sizes="72x72" href="http://www.indxx.com/images/favicon.ico">
                    <link rel="apple-touch-icon-precomposed" href="http://www.indxx.com/images/favicon.ico">
                                   <link rel="shortcut icon" href="http://www.indxx.com/images/favicon.ico">

   <script src="plugins/jQuery/jquery-2.2.3.min.js"></script>

<script src="https://code.jquery.com/ui/1.11.4/jquery-ui.min.js"></script>

<script src="bootstrap/js/bootstrap.min.js"></script>




<!-- Bootstrap WYSIHTML5 -->
  <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->    
    <script src="js/jquery.js"></script>
  </head>
<body class="hold-transition skin-blue sidebar-mini">
<div class="wrapper">

  <header class="main-header">
    <!-- Logo -->
    <a href="index2.html" class="logo" style="background-color:#CCCCCC;">
      <!-- mini logo for sidebar mini 50x50 pixels -->
      <span class="logo-mini"><img src ="images/logo.png" class="head_logo" title="logo" alt="logo" style="height:32px;"/></span>
      <!-- logo for regular state and mobile devices -->
	 
      <span class="logo-lg"><img src ="images/logo.png" class="head_logo" title="logo" alt="logo" style="height:32px;"/> </span>
	  <br/><br/><br/>
    </a>
    <!-- Header Navbar: style can be found in header.less -->
    <nav class="navbar navbar-static-top">
	 <section class="content-header">
      <h1>Back Test Calculation</h1>    
	  
    </section>
	<?php if(isset($_SESSION['userDisplayNamne'])) { ?>
      <!-- Sidebar toggle button-->
      <a href="#" class="sidebar-toggle" data-toggle="offcanvas" role="button">
        <span class="sr-only">Toggle navigation</span>
      </a>
		
	
      <div class="navbar-custom-menu">
        <ul class="nav navbar-nav">
          <!-- Messages: style can be found in dropdown.less-->
          
			  
			  <li class="dropdown user user-menu">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
             <!--  <img src="<?=$_SESSION['userDisplayPic']?>" class="user-image" alt="User Image"> -->
              <span class="hidden-xs"><?=$_SESSION['userDisplayNamne']?></span>
            </a> 
              </li>
			 



   <li class="dropdown user user-menu">
            <a href="inputs/" target='_blank'>
              <span class="hidden-xs">Input Files</span>
            </a> 
              </li>
			   <li class="dropdown user user-menu">
            <a href="csvfiles/"  target='_blank'>
              <span class="hidden-xs">Output Files</span>
            </a> 
              </li>

			  <li class="dropdown user user-menu">
            <a href="logout.php">
              <span class="hidden-xs">Logout</span>
            </a> 
              </li>
			   
          <li>
           
          </li>
        </ul>
      </div>
	<?php } ?>
    </nav>
  </header>
  
  <?php if(isset($_SESSION['userDisplayNamne'])) { ?>  
  <aside class="main-sidebar">   
    <section class="sidebar">
    </section>	    
  </aside>
    
  <?php } ?>
  <div class="content-wrapper">    
    <section class="content">
