__author__ = "Lucky"
## -*- coding:utf-8 -*-
'''
Remove Miscellaneous content
'''
import urllib
import urllib2
import re,time
import threading
from copy import deepcopy
##############################################
input_filename = "orginal_data.md"
output_filename = "tailed_pure_" + input_filename
##############################################
# get match regex
match_list = []
match_list_file = file("match_regex.txt")
for line in match_list_file:
	match_list.append(line.rstrip('\r\n'))
match_list_file.close()
print match_list

sfile = file(input_filename)
dfile = file(output_filename, 'w')

file_string = sfile.read()
tailed_string = ""
for item in match_list:	
	if len(item) == 0:
		pass
	tailed_string = re.sub(item, "", file_string)
	file_string = tailed_string
dfile.write(tailed_string)

sfile.close()
dfile.close()




