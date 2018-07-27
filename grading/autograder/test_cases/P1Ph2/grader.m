function [grade_data] = grader(grader_folder, cont_folder,~)
%% OUTPUT STRUCT
num_tests = 2;
grade_data = zeros(num_tests,2);
%% LOAD ALL TRAJECTORIES
cd(cont_folder);
fprintf("Loading Controller Handle\n");
controller_func_handle = str2func('controller');
% cd(traj_folder);
fprintf("Loading Trajectory Diamond Handle\n");
traj_diamond_func_handle = str2func('diamond');
fprintf("Loading Trajectory Circle Handle\n");
traj_circle_func_handle = str2func('circle');
addpath(genpath(grader_folder));
%% RUN DIAMOND SIMULATOR
cd(grader_folder);
fprintf("Starting Quad Simulator - Diamond\n");
[ErrorPos,time,sim_error] = grader_runsim(traj_diamond_func_handle, controller_func_handle,cont_folder);
if sim_error == 0
    fprintf("Position Error: %f,%f,%f\n", ErrorPos(1),ErrorPos(2),ErrorPos(3));
    fprintf("Simulation Time: %f\n", time);
    err_score = ((15.0 - ((ErrorPos(1) + ErrorPos(2) + ErrorPos(3))/3))/15.0)*100;
    time_score = ((30.0 - time)/30.0)*100;
    total_score = (err_score + time_score)/2; % 100
    
    grade_data(1,1) = 0;
    grade_data(1,2) = total_score;
    
    fprintf("Time Score: %f\n", time_score);
    fprintf("Position Score: %f\n", err_score);
    fprintf("Total Score: %f\n", total_score);
elseif sim_error == 1
    fprintf("Simulation Error - Diamond\n");
    grade_data(1,1) = 1;
    grade_data(1,2) = 0;
end
%% RUN CIRCLE SIMULATOR
cd(grader_folder);
fprintf("Starting Quad Simulator - Circle\n");
[ErrorPos,time,sim_error] = grader_runsim(traj_circle_func_handle, controller_func_handle, cont_folder);
if sim_error == 0
    fprintf("Position Error: %f,%f,%f\n", ErrorPos(1),ErrorPos(2),ErrorPos(3));
    fprintf("Simulation Time: %f\n", time);
        
    err_score = ((15.0 - ((ErrorPos(1) + ErrorPos(2) + ErrorPos(3))/3))/15.0)*100;
    time_score = ((30.0 - time)/30.0)*100;
    total_score = (err_score + time_score)/2;

    grade_data(2,1) = 0;
    grade_data(2,2) = total_score;
    
    fprintf("Time Score: %f\n", time_score);
    fprintf("Position Score: %f\n", err_score);
    fprintf("Total Score: %f\n", total_score);
elseif sim_error == 1
    fprintf("Simulation Error - Circle\n");
    grade_data(2,1) = 1;
    grade_data(2,2) = 0;
end
end