<?php
ini_set('display_errors', 'On');
error_reporting(E_ALL);
$dir = 'homework';

$folders = array();
$file_list = array();

$iterator = new DirectoryIterator($dir);
foreach ($iterator as $fileinfo) {
	if(!$fileinfo->isDot()){
		if($fileinfo->isDir())
			array_push($folders, $fileinfo->getFilename());
	}
}
foreach($folders as $folder){
	$folder = $dir.'/'.$folder;
	$files = new FileSystemIterator($folder);
	$file_struct = array();
	foreach($files as $file){
		$ext = pathinfo($file);
		switch($ext['extension']){
			case "yaml":
			$dates_file = $folder.'/'.$file->getFilename();
			$dates_parsed = yaml_parse_file($dates_file);
			$file_struct['release'] = $dates_parsed["RELEASE"];
			$file_struct['deadline'] = $dates_parsed["DEADLINE"];
			break;
			case "zip":
			$file_struct['file_path'] = $folder.'/'.$file->getFilename();
			break;
		}
	}
	array_push($file_list,$file_struct);
}

$num=1;
foreach($file_list as $file_data){
	$release = date_create_from_format('Y-m-j',$file_data['release']);
	$deadline = date_create_from_format('Y-m-j',$file_data['deadline']);

	echo "<tr>"; 
	echo "<td>".$num."</td>";
	echo "<td>".str_replace("_"," ",basename(dirname($file_data['file_path'])))."</td>";
	echo "<td>".$release->format('D, M jS, Y')."</td>";
	echo "<td>".$deadline->format('D, M jS, Y')."</td>";
	echo "<td> <a href=\"".$file_data['file_path']."\" download=\"".basename(dirname($file_data['file_path']))."\">Download</a></td>";
	echo "</tr>";
	$num++;
}

?>