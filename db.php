<?php
ini_set('display_errors', 'On');
error_reporting(E_ALL);

function db_query($sql){
	$server = "localhost";
	$db_user = "cmsc828t";
	$db_pass = "cmsc828t";
	$db_name = "cmsc828t";

	$conn = new mysqli($server, $db_user, $db_pass, $db_name);

	if ($conn->connect_error) {
		echo "Connection failed";
		die("Connection failed: " . $conn->connect_error);
	} 

	if(!$result = $conn->query($sql)){
		echo "Query failed";
		die($conn->error);
	}
	$conn->close();
	return $result;
}

function db_insert($sql){
	$server = "localhost";
	$db_user = "cmsc828t";
	$db_pass = "cmsc828t";
	$db_name = "cmsc828t";
	$insert_error = true;

	$conn = new mysqli($server, $db_user, $db_pass, $db_name);

	if ($conn->connect_error) {
		echo "Connection failed";
		die("Connection failed: " . $conn->connect_error);
	} 

	if ($conn->query($sql) === TRUE) {
		$insert_error = false;
	} else {
		$insert_error = true;
	}
	$conn->close();
	return $insert_error;
}

function send_message($error_type,$error_msg){
	$return_msg = array();
	$return_msg['TYPE'] = $error_type;
	$return_msg['MESSAGE'] = $error_msg;
	echo json_encode($return_msg);
}

if(isset($_REQUEST['type'])){
	if ($_REQUEST['type']=='get_student') {
		$student_name = $_REQUEST['data'];

		$sql = "INSERT IGNORE INTO students (student_name) VALUES ('$student_name')";
		$insert_error = db_insert($sql);
		if($insert_error){
			send_message('DB_ERROR', "Failed to add student to database.");
			exit;
		}else{
			$sql = "SELECT * FROM submission WHERE student_name = '$student_name'";
			$result = db_query($sql);
			if ($result->num_rows > 0) {
				while($row = $result->fetch_assoc()) {
					echo "<tr>"; 
					echo "<td>".$row["submission_id"]."</td>";
					echo "<td>".$row["submission_time"]."</td>";
					echo "<td>".$row["submission_project"]."</td>";
					echo "<td>".$row["submission_graded"]."</td>";
					echo "<td>".$row["submission_score"]."</td>";
					echo "</tr>";
				}
			} else {
				echo "<tr>"; 
				echo "<td>----</td>";
				echo "<td>----</td>";
				echo "<td>----</td>";
				echo "<td>----</td>";
				echo "<td>----</td>";
				echo "</tr>";
			}
		}
	}else if($_REQUEST['type']=='get_comment'){
		$submission_id = $_REQUEST['data'];
		$sql = "SELECT student_name,submission_project FROM submission WHERE submission_id=$submission_id";
		$result = db_query($sql);
		if ($result->num_rows > 0) {
			while($row = $result->fetch_assoc()) {
				$comment_file = $row['student_name']."_".$row['submission_project']."_code.txt";
			}
		}
		$full_comment = "/var/www/html/grading/evaluated/".$comment_file;
		$comment_open = fopen($full_comment, 'r');
		if(filesize($full_comment) > 0){
			echo nl2br(fread($comment_open,filesize($full_comment)));
		}
		fclose($comment_open);
	}else if($_REQUEST['type']=='submission'){

		// CHECK EMPTY FILE ERROR
		if($_FILES['file']['error']===UPLOAD_ERR_NO_FILE){
			send_message('UPLOAD_ERROR', 'No file received.');
			exit;
		}else{
			$file_received = $_FILES['file'];
		}

		// CHECK FILE SIZE
		if ($_FILES['file']['size'] > 1000000) {
			send_message('SIZE_ERROR', 'Exceeded filesize limit.');
			exit;
		}else if($_FILES['file']['size'] < 1){
			send_message('SIZE_ERROR', 'File size too small.');
			exit;
		}

		// ALL OKAY, PROCEED TO UPLOAD
		$upload_dir = "/var/www/html/uploads/";
		$file_uid = $_POST['uname']."_".$_POST['proj_type']."_";
		$file_name = $_FILES["file"]["name"];
		$full_file = $upload_dir.$file_uid.$file_name;
		$error = true;

		// UPLOAD VARIABLES
		$student_name = $_POST['uname'];
		$submission_project = $_POST['proj_type'];
		$submission_graded = 0;
		$submission_score = 0;
		if($submission_project == 'P1Ph3'){
			$submit_limit = "10";	
		}
		else if($submission_project == 'P1Ph2'){
                        $submit_limit = "7";
                }
		else{
			$submit_limit = "5";	
		}
		

		// CHECK SUBMISSION COUNT
		$sql="SELECT COUNT('submission_id') FROM submission WHERE student_name='$student_name' AND submission_project='$submission_project'";
		$count_result = db_query($sql);
		
		if ($count_result->num_rows > 0) {
			$row = mysqli_fetch_row($count_result);
			$submit_count=$row[0];
		}

		if($submit_count >= $submit_limit){
			send_message('LIMIT_ERROR', "Exceeded upload limit of ".$submit_limit." submissions. Contact course TA.");
		}else{
			// UPLOAD THE FILE
			if(move_uploaded_file($_FILES["file"]["tmp_name"],  $full_file)){
				$error = false;
			}else{
				$error = true;
			}
			if(!$error){
				$sql = "INSERT INTO submission (student_name, submission_project, submission_graded, submission_score)
				VALUES ('$student_name', '$submission_project', $submission_graded, $submission_score)";

				$insert_error = db_insert($sql);
				if(!$insert_error){
					send_message('SUCCESS', "Received file ". $file_name ." from ". $student_name." for project ". $submission_project);
				}else{
					send_message('DB_ERROR', "Failed to insert upload to database.");
				}
			}else{
				send_message('UPLOAD_ERROR', "Failed to upload file");
			}
		}
	}
}
?>
