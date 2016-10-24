# -*- coding: utf-8 -*-
import json
import os
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
filename_in = "result/mafengwo_new.json"
filename_out = "result/mafengwo1.csv"
#filename_out1 = "result/mafengwo_convert.json"

f_in = open(filename_in, 'r')
if not os.path.exists(filename_out):
	line = f_in.readline()
	lineItem = json.loads(line)
	lineDict = dict(lineItem)
	f = open(filename_out, 'w')
	f.write(','.join(lineDict.keys())+'\n')
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
	lineItem = json.loads(line)
	lineDict = dict(lineItem)
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
#f_out1.close()

