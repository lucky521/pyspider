__author__ = "Lucky"
## -*- coding:utf-8 -*-
'''
Remove useless newline char and align

orginal_data: 
aaaaaa
aaaa

bbbb
bb

cc

dd
dddd

result_data:
aaaaa aaaa
bbbb bb
cc
dd dddd

'''
import re
##############################################
input_filename = "tailed_pure_original_data.md"
output_filename = "tailed_align_" + input_filename
##############################################
sfile = file(input_filename)
dfile = file(output_filename, 'w')
file_string = sfile.read()


origin_regex = "\r\n\r\n"
target_string = "#####"
tailed_string = re.sub(origin_regex, target_string, file_string)
file_string = tailed_string


origin_regex = "\r\n"
target_string = " "
tailed_string = re.sub(origin_regex, target_string, file_string)
file_string = tailed_string

origin_regex = "#####"
target_string = "\r\n"
tailed_string = re.sub(origin_regex, target_string, file_string)
file_string = tailed_string


dfile.write(file_string)
sfile.close()
dfile.close()
