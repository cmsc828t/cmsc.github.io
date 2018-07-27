
$(window).on("load",function(){
	$(".nav li").removeClass("active");
	$(".nav li:first-child").addClass("active");
	to_load = "Homepage.html";
	$( "#PageContainer" ).empty();
	$( "#PageContainer" ).load( to_load,function(){
		$("#PageContainer").height(100);
	});
	$("#upload_alert").hide();
	check_syllabus_updates();
});

function check_syllabus_updates(){
	$.ajax({
		type: "POST",
		url: "update_checker.php?check",
		success: function(result){
			if(result == "CHANGE"){
				$(".badge").text("!");
			}else{
				$(".badge").text("");
			}
		}
	});

}

$("ul#project_select li").click(function(){
	var db_fetch = {};
	li_to_disable = $(this);
	db_fetch.type="CHECK_DEADLINE";
	db_fetch.project = li_to_disable.text();
	$.ajax({
		type: "POST",
		url: "deadline.php",
		data:db_fetch,
		async:false,
		success: function(result){
			if( ($("#welcome_msg").text().split(",")[1]).toString().trim() != '@kganguly'){
				if(result == "TIME_EXPIRED"){
					$("#submit_proj_btn").attr('disabled',true);
					set_upload_alert("Submission deadline for " + li_to_disable.text() +" passed.",'danger');
				}else if(result == "TIME_NOT_STARTED"){
					$("#submit_proj_btn").attr('disabled',true);
					li_to_disable.addClass('disabled');
					set_upload_alert("Submission portal for " + li_to_disable.text() +" not open.",'danger');
				}else if(result == "TIME_VALID"){
					$("#submit_proj_btn").attr('disabled',false);
					li_to_disable.removeClass('disabled');
					set_upload_alert("Please submit " + li_to_disable.text(),'success');
				}
			}
		}

	});
});

function set_upload_alert(msg,type){
	$('#upload_alert').removeClass();
	$('#upload_alert').addClass('alert');
	$('#upload_alert').addClass('alert-'+type);
	$("#upload_alert").text(msg);
	$("#upload_alert").show();
}

$(".nav li").on("click", function(e) {
	$(".nav li").removeClass("active");
	$(this).addClass("active");
	to_load = $(this).text() + ".html";
	to_load = to_load.replace("!","");
	if ($(this).text() == "Submit"){
		to_load = $(location).attr('href') + $(this).text() + ".html";
		window.open(to_load,"_blank");
		to_load="Homepage.html";
	}
	$( "#PageContainer" ).empty();
	$( "#PageContainer" ).load( to_load,function(){
		$("#PageContainer").height(100);
	});
	return false;
});

$("#submit_control button").on("click", function(e) {
	switch($(this).text()){
		case "Submissions":
		var db_fetch = {};
		db_fetch.type="get_student";
		db_fetch.data=$("#username_hidden").attr("name");
		$.ajax({
			type: "POST",
			url: "db.php",
			data:db_fetch,
			success: function(result){
				$(".submission-table").find("tr:gt(0)").remove();
				$('.submission-table tr:last').after(result);
			}
		});
		break;
		case "Leaderboard":
		break;
	}
});

$(function(){
	$(".dropdown-menu").on('click', 'li a', function(){
		$("#selected_proj").text($(this).text());
		$("#selected_proj").val($(this).text());
	});
});

var files=false;
var proj_type=null;
var uname=$("#username_hidden").attr("name");
$('input[type=file]').on('change', prepareUpload);
$('#submission_form').on('submit', uploadFiles);

$('#project_select li').on('click', function(){
	proj_type=$(this).text();
});

function prepareUpload(e){
	file_check = e.target.files;
	var fileExtension = ['zip'];
	if ($.inArray($('input[type=file]').val().split('.').pop().toLowerCase(), fileExtension) == -1) {
		set_upload_alert("Only '.zip' format is allowed.","danger");
        $('input[type=file]').val(''); // Clean field
        return false;
    }
}

function uploadFiles(e){
	e.stopPropagation();
	e.preventDefault();

	var submit_data = new FormData();
	$.each($('input[type=file]')[0].files, function(i, file) {
		files=true;
		submit_data.append('file', file);
	});
	submit_data.append('uname',uname);
	submit_data.append('proj_type',proj_type);

	if(proj_type==null){
		set_upload_alert("Please set project type.","danger");
		return;
	}else if(files==false){
		set_upload_alert("Please upload files correctly.","danger");
		return;
	}else if(uname==null){
		set_upload_alert("Please sign in correctly.","danger");
		return;	
	}else{
		set_upload_alert("All good, uploading now.","success");
	}
	$("#submit_proj_btn").button('loading');
	$.ajax({
		url: "db.php?type=submission",
		type: 'POST',
		data: submit_data,
		async:false,
		contentType: false,
		processData: false,
		success: function (response) {
			console.log(response);
			var parsedArray =  JSON.parse(response);
			var response_type = parsedArray.TYPE;
			var response_msg = parsedArray.MESSAGE;
			var alert_type;

			switch(response_type){
				case "SUCCESS":
				alert_type="success";
				break;
				case "SIZE_ERROR":
				case "UPLOAD_ERROR":
				case "LIMIT_ERROR":
				case "DB_ERROR":
				alert_type="danger";
				break;
				default:
				alert_type="warning";
			}
			set_upload_alert(response_msg,alert_type);
			$('input[type=file]').val(''); 
			$("#submit_proj_btn").button('reset');
		}
	});
	return false;
}

$('.submission-table').on('click','td:not(:first-child)',function () {
	submission_id = $(this).closest('td').parent().find('td').eq(0).text();
	graded = $(this).closest('td').parent().find('td').eq(3).text();
	if(graded == 1){
		var db_comment = {};
		db_comment.type="get_comment";
		db_comment.data=submission_id;
		$.ajax({
			type: "POST",
			url: "db.php",
			data:db_comment,
			success: function(result){
				$("#submission_comments").html(result);
			}
		});
	}
} );