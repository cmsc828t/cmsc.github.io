import yaml
import matlab.engine
import time
from timeout import timeout
from grader_db import write_score

def exit_grader(eval_log,username,score,project,error_msg,close_log = False):
	eval_log.write(error_msg)
	if close_log:
		eval_log.close()
	write_score(username,score,project)
	return

