#!/usr/bin/env python
import os
import sys
import argparse
import zipfile as zipper
from grader_db import *
from grader_P1Ph1_helper import *
import matlab.engine

root_dir = '/var/www/html/'
grading_dir = root_dir + 'grading/'
autograder_dir = grading_dir + 'autograder/'
evaluated_dir = grading_dir + 'evaluated'
test_dir = autograder_dir + 'test_cases/P1Ph1/'
upload_dir = root_dir + 'uploads/'

parser = argparse.ArgumentParser()
parser.add_argument('-gradestudent',default=None,dest='student_id')
args = parser.parse_args()

if args.student_id is None:
    upload_list = [upload_item for upload_item in os.listdir(upload_dir) if upload_item.endswith("_P1Ph1_code.zip")]
else:
    upload_list = [upload_item for upload_item in os.listdir(upload_dir) if upload_item.endswith("_P1Ph1_code.zip") and upload_item in args.student_id+"_P1Ph1_code.zip"]

eng = matlab.engine.start_matlab("-nosplash -nojvm -nodisplay -nodesktop")

eng.cd(root_dir)
eng.addpath('uploads', eng.genpath(test_dir))

for each_submission in upload_list:
    score = 0

    eng.cd(root_dir);
    to_unzip = upload_dir + each_submission
    unzip_folder = os.path.splitext(to_unzip)[0]
    submission_name = os.path.splitext(each_submission)[0]
    zipped_file = zipper.ZipFile(to_unzip,'r')
    zipped_file.extractall(unzip_folder)
    zipped_file.close()
    
    print("Evaluating: " + submission_name)

    username = submission_name.split("_")[0]
    project = submission_name.split("_")[1]

    # Start evaluation logs
    eval_log = open(evaluated_dir + "/" + submission_name + ".txt", "w")

    if os.path.exists(unzip_folder + '/code'):
        eng.cd(unzip_folder + '/code');
    else:
        eval_log.write("Code Submission Format Error (Incorrect File/Folder Paths)\n")
        eval_log.close()
        write_score(username,score,project)
        continue
   
    # Load test cases
    map_empty_params,map_empty_start,map_empty_goal = load_test_case(test_dir+'map_empty_input.yaml')
    map_0_params,map_0_start,map_0_goal = load_test_case(test_dir+'map0_input.yaml')
    map_31_params,map_31_start,map_31_goal = load_test_case(test_dir+'map3_input.yaml')
    map_32_params,map_32_start,map_32_goal = load_test_case(test_dir+'map3_input2.yaml')

    # Load map files
    map_empty_file = test_dir + 'map_empty.txt'
    map_0_file = test_dir + 'map0.txt'
    map_3_file = test_dir + 'map3.txt'
    
    # START EVALUATION
    eval_log.write(("Now evaluating: %s\n") % each_submission)
    eval_log.write("\n")

    # Load all maps
    eval_log.write("Loading maps...\n")
    eval_log.write("\n")

    map_empty = load_map_func(eng,eval_log,map_empty_file,map_empty_params)
    if map_empty is None:
        eval_log.write("Map Loading Code Error\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    map_0 = load_map_func(eng,eval_log,map_0_file,map_0_params)
    if map_0 is None:
        eval_log.write("Map Loading Code Error\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    map_31 = load_map_func(eng,eval_log,map_3_file, map_31_params)
    if map_31 is None:
        eval_log.write("Map Loading Code Error\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    map_32 = load_map_func(eng,eval_log,map_3_file, map_32_params)
    if map_32 is None:
        eval_log.write("Map Loading Code Error\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    
   
    # Collision Testing
    test_pass = 1
    valid_data = matlab.double([[0.0, -1.0, 2.0], [3.0, 17.0, 4.0], [0.0, -5.0, 0.5]])
    test_pass,score = test_collision(eng,eval_log,map_0,score,1,valid_data)
    if test_pass is 0:
        eval_log.write("Collision Tests Code Error\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    elif test_pass is 3:
        eval_log.write("No-Collision Test Failed\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    elif test_pass is 1:
        eval_log.write("Failed Collision Test Timing Constraints\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    else:
        pass
    # No-Collision Testing
    test_pass = 1
    collision_data = matlab.double([[0.0, 2.0, 1.0], [3.0, 18.5, 4.5]])
    test_pass,score = test_collision(eng,eval_log,map_0,score,0,collision_data)
    if test_pass is 0:
        eval_log.write("Collision Tests Code Error\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    elif test_pass is 3:
        eval_log.write("Collision Test Failed\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    elif test_pass is 1:
        eval_log.write("Failed Collision Test Timing Constraints\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    else:
        pass

    # Test Map0 Dijkstra
    test_pass = 1
    eval_log.write("Now testing Map 0\n")
    eval_log.write("Now testing Dijkstra\n")
    test_pass,score = test_path_planning(eng,eval_log,map_0,score,False,map_0_start,map_0_goal)
    if test_pass is 0:
        eval_log.write("Dijkstra Test Code Error\n")
        eval_log.close()
        continue
    elif test_pass is 1:
        eval_log.write("Failed Dijkstra Test Timing Constraints\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    elif test_pass is 3:
        eval_log.write("Dijkstra Test Failed\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    else:
        pass
    # Test Map0 A-Star
    test_pass = 1
    eval_log.write("Now testing A-Star\n")
    test_pass,score = test_path_planning(eng,eval_log,map_0,score,True,map_0_start,map_0_goal)
    if test_pass is 0:
        eval_log.write("A-Star Test Code Error\n")
        eval_log.close()
        continue
    elif test_pass is 1:
        eval_log.write("Failed A-Star Test Timing Constraints\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    elif test_pass is 3:
        eval_log.write("A-Star Test Failed\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    else:
        pass
    eval_log.write("\n")

    # Test MapEmpty Dijkstra
    test_pass = 1
    eval_log.write("Now testing Empty Map\n")
    test_pass,score = test_path_planning(eng,eval_log,map_empty,score,False,map_empty_start,map_empty_goal)
    if test_pass is 0:
        eval_log.write("Dijkstra Test Code Error\n")
        eval_log.close()
        continue
    elif test_pass is 1:
        eval_log.write("Failed Dijkstra Test Timing Constraints\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    elif test_pass is 3:
        eval_log.write("Dijkstra Test Failed\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    else:
        pass
    # Test MapEmpty A-Star
    test_pass = 1
    eval_log.write("Now testing A-Star\n")
    test_pass,score = test_path_planning(eng,eval_log,map_empty,score,True,map_empty_start,map_empty_goal)
    if test_pass is 0:
        eval_log.write("A-Star Test Code Error\n")
        eval_log.close()
        continue
    elif test_pass is 1:
        eval_log.write("Failed A-Star Test Timing Constraints\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    elif test_pass is 3:
        eval_log.write("A-Star Test Failed\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    else:
        pass
    eval_log.write("\n")

    # Test Map3_1 Dijkstra
    test_pass = 1
    eval_log.write("Now testing Map 3 Input 1\n")
    test_pass,score = test_path_planning(eng,eval_log,map_31,score,False,map_31_start,map_31_goal)
    if test_pass is 0:
        eval_log.write("Dijkstra Test Code Error\n")
        eval_log.close()
        continue
    elif test_pass is 1:
        eval_log.write("Failed Dijkstra Test Timing Constraints\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    elif test_pass is 3:
        eval_log.write("Dijkstra Test Failed\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    else:
        pass
    # Test Map3_1 A-Star
    test_pass = 1
    eval_log.write("Now testing A-Star\n")
    test_pass,score = test_path_planning(eng,eval_log,map_31,score,True,map_31_start,map_31_goal)
    if test_pass is 0:
        eval_log.write("A-Star Test Code Error\n")
        eval_log.close()
        continue
    elif test_pass is 1:
        eval_log.write("Failed A-Star Test Timing Constraints\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    elif test_pass is 3:
        eval_log.write("A-Star Test Failed\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    else:
        pass
    eval_log.write("\n")

    # Test Map3_2 Dijkstra
    test_pass = 1
    eval_log.write("Now testing Map 3 Input 2\n")
    test_pass,score = test_path_planning(eng,eval_log,map_32,score,False,map_32_start,map_32_goal)
    if test_pass is 0:
        eval_log.write("Dijkstra Test Code Error\n")
        eval_log.close()
        continue
    elif test_pass is 1:
        eval_log.write("Failed Dijkstra Test Timing Constraints\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    elif test_pass is 3:
        eval_log.write("Dijkstra Test Failed\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    else:
        pass
    # Test Map3_2 A-Star
    test_pass = 1
    eval_log.write("Now testing A-Star\n")
    test_pass,score = test_path_planning(eng,eval_log,map_31,score,True,map_32_start,map_32_goal)
    if test_pass is 0:
        eval_log.write("A-Star Test Code Error\n")
        eval_log.close()
        continue
    elif test_pass is 1:
        eval_log.write("Failed A-Star Test Timing Constraints\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    elif test_pass is 3:
        eval_log.write("A-Star Test Failed\n")
        eval_log.close()
        write_score(username,score,project)
        continue
    else:
        pass
    eval_log.write("\n")

    # Write score to DB
    write_score(username,score,project)

    # Close evaluation logs
    eval_log.close()
