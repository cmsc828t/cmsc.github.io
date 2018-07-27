#!/usr/bin/env python
import os
import sys
import argparse
import zipfile as zipper
from grader_db import *
from grader_P1Ph2_helper import *
import matlab.engine
import matlab

root_dir = '/var/www/html/'
grading_dir = root_dir + 'grading/'
autograder_dir = grading_dir + 'autograder/'
evaluated_dir = grading_dir + 'evaluated'
test_dir = autograder_dir + 'test_cases/P1Ph2/'
upload_dir = root_dir + 'uploads/'

parser = argparse.ArgumentParser()
parser.add_argument('-gradestudent',default=None,dest='student_id')
parser.add_argument('-dockpoints', action='store_true', default=False)
args = parser.parse_args()

if args.student_id is None:
    upload_list = [upload_item for upload_item in os.listdir(upload_dir) if upload_item.endswith("_P1Ph2_code.zip")]
else:
    upload_list = [upload_item for upload_item in os.listdir(upload_dir) if upload_item.endswith("_P1Ph2_code.zip") and upload_item in args.student_id+"_P1Ph2_code.zip"]

print("Starting Matlab...")
# eng = matlab.engine.connect_matlab()
eng = matlab.engine.start_matlab("-nosplash -nojvm -nodisplay -nodesktop")
print(matlab.engine.find_matlab())


eng.cd(root_dir)
eng.addpath(eng.genpath(upload_dir), eng.genpath(test_dir))

for each_submission in upload_list:
	score = 0
	eng.restoredefaultpath
	eng.cd(root_dir)
	to_unzip = upload_dir + each_submission
	unzip_folder = os.path.splitext(to_unzip)[0]
	submission_name = os.path.splitext(each_submission)[0]
	zipped_file = zipper.ZipFile(to_unzip,'r')
	zipped_file.extractall(unzip_folder)
	zipped_file.close()
    
	username = submission_name.split("_")[0]
	project = submission_name.split("_")[1]

	print("Evaluating: " + submission_name)

	# Start evaluation logs
	eval_log = open(evaluated_dir + "/" + submission_name + ".txt", "w")

	if not os.path.exists(unzip_folder + '/code'):
		error_msg = "Code Submission Format Error (Incorrect File/Folder Paths)\n"
		if args.dockpoints:
			exit_grader(eval_log,username,score,project,error_msg,close_log=False)
		else:
			exit_grader(eval_log,username,score,project,error_msg,close_log=True)
			continue

	try:
		grade_data = eng.grader(test_dir,unzip_folder+"/code",unzip_folder+"/code/trajectories")
 	except matlab.engine.MatlabExecutionError as exec_err:
 		error_msg = "Matlab Execution Error\n"
 		exit_grader(eval_log,username,score,project,error_msg)
 		continue

	error_diamond = grade_data[0][0] if grade_data[0][0] > 0.0 else 0
	score_diamond = grade_data[0][1] if grade_data[0][1] > 0.0 else 0
	error_circle = grade_data[1][0] if grade_data[1][0] > 0.0 else 0
	score_circle = grade_data[1][1] if grade_data[1][1] > 0.0 else 0

	if error_diamond is 1:
		error_msg = "Diamond Trajectory Error...\n"
		exit_grader(eval_log,username,score,project,error_msg,close_log=False)
	if error_circle is 1:
		error_msg = "Circle Trajectory Error...\n"
		exit_grader(eval_log,username,score,project,error_msg,close_log=False)

	score = score_diamond + score_circle

	if args.dockpoints:
		score -= score*0.2
		error_msg = "Manually graded. 20% points docked.\n"
		exit_grader(eval_log,username,score,project,error_msg,close_log=False)

	if score == 0:
		error_msg = "Code Position and/or Timing Constraints Failed\n"
		exit_grader(eval_log,username,score,project,error_msg,close_log=True)
	else:
		error_msg = "All tests successfully passed.\nFinal scores out of 200 points.\n"
		exit_grader(eval_log,username,score,project,error_msg,close_log=True)	

	print("Final Score: " + str(score))
	print("\n")