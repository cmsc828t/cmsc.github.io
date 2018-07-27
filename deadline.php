<?php
ini_set('display_errors', 'On');
error_reporting(E_ALL);

$dir = 'deadlines';

if(isset($_REQUEST['type'])){
	if ($_REQUEST['type']=='CHECK_DEADLINE') {
		$project_name = $_REQUEST['project'];
		$deadline_file = $dir.'/'.$project_name."_deadline.yaml";
		
		$deadline_parsed = yaml_parse_file($deadline_file);
		$deadline_start_yaml = $deadline_parsed["RELEASE"];
		$deadline_end_yaml = $deadline_parsed["DEADLINE"];

		$deadline_start = date_create_from_format('Y-m-j H:i:s',$deadline_start_yaml);
		$deadline_end = date_create_from_format('Y-m-j H:i:s',$deadline_end_yaml);
		$time_now = new DateTime("now");

		if($time_now < $deadline_start){
			echo "TIME_NOT_STARTED";
		}else if ($time_now > $deadline_end){
			echo "TIME_EXPIRED";
		}else if ($time_now < $deadline_end && $time_now > $deadline_start){
			echo "TIME_VALID";
		}
	}
}
?>