<?php
if($_GET['file']) {
	$dispalyname = $_GET['file'];
	$filename = dirname(__FILE__)."/csvfiles/".$_GET['file'];
	if (file_exists($filename)) {
		header("Content-Length: " . filesize($filename));
		header('Content-Type: application/octet-stream');
		header('Content-Disposition: attachment; filename='.$dispalyname);
		readfile($filename);
		//unlink($filename);
	}
}
	
?>