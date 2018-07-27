#!/usr/bin/env python

import glob
import os
from grader_db import upload_submissions

root_dir = '/var/www/html'
upload_dir = root_dir + '/uploads'
upload_list = glob.glob(upload_dir+"/*.zip")
for each_upload in upload_list:
	username = os.path.basename(each_upload).split("_")[0]
	project = 'P1Ph1'
	upload_submissions(username,project)
