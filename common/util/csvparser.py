#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author:Wooce Yang

import csv
import os
from StringIO import StringIO

def getPythonPath():
	path = os.environ['PYTHONPATH'][1:]
	return path

class CCsvParser:
	def __init__(self):
		pass
	@staticmethod
	def parse(input_file):
		input_file = getPythonPath()+'/template/'+input_file
		src = file(input_file, "rb")
		line = src.readline()
		heading = [_head.strip() for _head in line.split(",")]
		return CCsvParser._parse_csv(input_file, heading, skip=1)

	@staticmethod
	def _parse_csv(input_file, csv_heading, skip=0,strip=True):
		src = file(input_file, "rb")
		reader = csv.DictReader(src, csv_heading)
		# skip the first line
		for i in xrange(skip):
			reader.next()
		result_dict = {}
		for row in reader:
			if strip:
				for _k, _v in row.items():
					row[_k] = _v.strip()
				#print 'key: ', row['id']
				result_dict[row['id']] = row
		return result_dict
