# -*- coding: utf-8 -*-
import os
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
filename_in = "result/mafengwo_new.json"
filename_out = "result/china.csv"

f_in = open(filename_in, 'r')
if not os.path.exists(filename_out):
	line = f_in.readline()
	lineDict = json.loads(line)
	f = open(filename_out, 'w')
	f.write(','.join(lineDict.keys())+'\n')
	if lineDict['country'] == u'中国':		
		items = []
		for v in lineDict.values():
			newv = str(v).replace('\n\t','').replace('\"', '').replace(',','，')
			newv = "\"" + newv + "\""
			items.append(newv)
		f.write(','.join(items) + '\n')
	f.close()

f_out = open(filename_out, 'a')
#f_out1 = open(filename_out, 'a')

line = f_in.readline()
while line:
	lineDict = json.loads(line)
	if lineDict['country'] == u'中国':
		items = []
		for v in lineDict.values():
			newv = str(v).replace('\n\t','').replace('\"', '').replace(',','，')
			newv = "\"" + newv + "\""
			items.append(newv)
		f_out.write(','.join(items) + '\n')
	#	lineToWrite = json.dumps(lineDict, ensure_ascii=False) + '\n'
	#	f_out1.write(lineToWrite)
	line = f_in.readline()

f_in.close()
f_out.close()