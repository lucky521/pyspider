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
input_filename = "original_data.txt"
output_filename = "tailed_align_" + input_filename
##############################################
sfile = file(input_filename)
dfile = file(output_filename, 'w')
origin_regex = "((?!\r\n).\r\n(?!\r\n).)"
target_string = " "
file_string = sfile.read()
tailed_string = re.sub(origin_regex, target_string, file_string)
dfile.write(tailed_string)

sfile.close()
dfile.close()




