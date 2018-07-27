import yaml
import matlab.engine
import time
from timeout import timeout
from grader_db import write_score

def load_test_case(map_yaml):
    map_test_stream = open(map_yaml, 'r')
    map_test_file = yaml.load(map_test_stream)
    map_load_params = {}
    map_start = {}
    map_goal = {}
    for doc in map_test_file:
        for vals in map_test_file[doc]:
            if doc == "load_map_params":
                for k, v in vals.items():
                    map_load_params[k] = v
            if doc == "test_start":
                for k, v in vals.items():
                    map_start[k] = v
            if doc == "test_goal":
                for k, v in vals.items():
                    map_goal[k] = v
    map_test_stream.close()
    return map_load_params,map_start,map_goal

@timeout(15)
def load_map_func(eng,eval_log,map_file,map_params):
    try:
        loaded_map = eng.load_map(map_file, map_params['x'], map_params['y'], map_params['z'],nargout=1)
        return loaded_map
    except ValueError as val_err:
        return None
    except matlab.engine.MatlabExecutionError as exec_err:
        print("Map MATLAB Error")
        return None
    except OSError as timer_err:
        print("Map Timing Error")
        return None

@timeout(30)
def test_collision(eng,eval_log,map_obj,score,collide_type,collide_data):
    eval_log.write("Now testing collision\n")
    # Collision Test
    try:
        if collide_type is 1:
            valid_data = collide_data
            collision_test = eng.collide(map_obj, valid_data)
            collision_test = [item for sublist in collision_test for item in sublist]
            if (any(collision_test) is True):
                test_pass = 3
                return test_pass,score
            else:
                eval_log.write("No-Collision Test Passed\n")
                score += 100
                test_pass = 2
        elif collide_type is 0:
            collision_data = collide_data
            collision_test = eng.collide(map_obj, collision_data)
            collision_test = [item for sublist in collision_test for item in sublist]
            if (all(collision_test) is False):
                test_pass = 3
                return test_pass,score
            else:
                eval_log.write("Collision Test Passed\n")
                eval_log.write("\n")
                test_pass = 2
                score += 100
    except matlab.engine.MatlabExecutionError as exec_err:
        print("Collide MATLAB Error")
        test_pass = 0
        return test_pass,score
    except OSError as timer_err:
        print("Collide Timing Error")
        test_pass = 1
        return test_pass,score

    return test_pass,score

@timeout(30)
def test_path_planning(eng,eval_log,map_obj,score,astar,map_start,map_goal):
    start_test = matlab.double([map_start['x'], map_start['y'], map_start['z']])
    goal_test = matlab.double([map_goal['x'], map_goal['y'], map_goal['z']])
    try:
        if not astar:
                start_time = time.time()
                dijkstra_path, dijkstra_num = eng.dijkstra(map_obj, start_test, goal_test, nargout=2)
                if dijkstra_num > 0:
                    elapsed_time = time.time() - start_time
                    score += ((30.0 - elapsed_time)/30.0)*100
                    eval_log.write(("Dijkstra Time: %f\n") % elapsed_time)
                    eval_log.write(("Dijkstra NumNodes: %f\n") % dijkstra_num)
                    eval_log.write("Dijkstra Passed\n")
                    eval_log.write("\n")
                    test_pass = 2
                else:
                    test_pass = 3
                    return test_pass,score
        else:
                start_time = time.time()
                astar_path, astar_num = eng.dijkstra(map_obj, start_test, goal_test, 1, nargout=2)
                if astar_num > 0:
                    elapsed_time = time.time() - start_time
                    score += ((30.0 - elapsed_time)/30.0)*100
                    eval_log.write(("A-Star Time: %f\n") % elapsed_time)
                    eval_log.write(("A-Star NumNodes: %f\n") % astar_num)
                    eval_log.write("A-Star Passed\n")
                    eval_log.write("\n")
                    test_pass = 2
                else:
                    test_pass = 3
                    return test_pass,score
    except matlab.engine.MatlabExecutionError as exec_err:
        print("Planning MATLAB Error")
        test_pass = 0
        return test_pass,score
    except OSError as timer_err:
        print("Planning Timing Error")
        test_pass = 1
        return test_pass,score

    return test_pass,score