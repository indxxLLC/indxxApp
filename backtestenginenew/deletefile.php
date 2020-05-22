<?php
if(isset($_POST['Proceed']) && $_POST['Proceed']=="delete" && isset($_POST['filename'])) {
	if(file_exists(dirname(__FILE__)."/tmp/".$_POST['filename'])) {
		unlink(dirname(__FILE__)."/tmp/".$_POST['filename']);	
	}
	
}

exit();
  