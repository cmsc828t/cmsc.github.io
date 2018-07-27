<?php
ini_set('display_errors', 'On');
error_reporting(E_ALL);
$update_file = 'resources/config/updates.yaml';
$update_file_parsed = yaml_parse_file($update_file);
$last_checked_yaml = $update_file_parsed["LAST_CHECKED"];
$last_hash = $update_file_parsed["HASH"];
$change = $update_file_parsed["CHANGE"];
$last_checked = date_create_from_format('Y-m-j H:i:s',$last_checked_yaml);
$time_now = new DateTime("now");

$time_difference = date_diff($last_checked,$time_now);
$time_diff_hours = $time_difference->format('%h');


if($time_diff_hours > 24){
	$new_hash = hash_file('md5', 'Syllabus.html');
	if($new_hash != $last_hash){
		$save_update = array("LAST_CHECKED"=>$time_now->format('Y-m-j H:i:s'),"HASH"=>$new_hash,"CHANGE"=>1);
		yaml_emit_file($update_file, $save_update);
	}else{
		$save_update = array("LAST_CHECKED"=>$time_now->format('Y-m-j H:i:s'),"HASH"=>$new_hash,"CHANGE"=>0);
		yaml_emit_file($update_file, $save_update);
	}
}
if(isset($_REQUEST['check'])){
	if($change == 1){
		echo "CHANGE";
	}
}
?>