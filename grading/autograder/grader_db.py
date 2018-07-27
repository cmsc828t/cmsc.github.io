import pymysql.cursors

def write_score(username,score,project):
	conn = pymysql.connect(host='localhost',
	                             user='cmsc828t',
	                             password='cmsc828t',
	                             db='cmsc828t',
	                             autocommit=True
	                             )
	try:
		with conn.cursor() as cursor:
			sql = ("UPDATE submission SET submission_graded=%d,submission_score=%d WHERE student_name='%s' AND submission_project='%s' ORDER BY submission_time DESC LIMIT 1")%(1,score,username,project)
			cursor.execute(sql)
	finally:
		conn.close()

def upload_submissions(username,project):
	conn = pymysql.connect(host='localhost',
	                             user='cmsc828t',
	                             password='cmsc828t',
	                             db='cmsc828t',
	                             autocommit=True
	                             )
	try:
		with conn.cursor() as cursor:
			sql = ("INSERT INTO submission (student_name,submission_project,submission_graded,submission_score) VALUES ('%s','%s',%d,%d)")%(username,project,0,0)
			cursor.execute(sql)
	finally:
		conn.close()