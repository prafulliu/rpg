#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import os
from StringIO import StringIO

def getPythonPath():
	path = os.environ['PYTHONPATH'][1:]
	return path

class CCsvParser:
	def __init__(self, file):
		self.file    = file
		self.col_name_list = []
		self.k2pkdict = {}
		self.pk2vdict = self.parse()

	def parse(self):
		input_file = getPythonPath()+'/template/'+self.file
		src = file(input_file, "rb")
		line = src.readline()
		heading = [_head.strip() for _head in line.split(",")]
		self.col_name_list = heading 
		return self._parse_csv(input_file, heading, skip=1)

	def _parse_csv(self, input_file, csv_heading, skip=0, strip=True):
		src = file(input_file, "rb")
		reader = csv.DictReader(src, csv_heading)
		# skip the first line
		for i in xrange(skip):
			reader.next()
		result_dict = {}
		k2pkdict = {}
		for head in csv_heading:
			k2pkdict[head] = {}
		for row in reader:
			if strip:
				for _k, _v in row.items():
					row[_k] = _v.strip()
					for __v in csv_heading:
						try:
							if row['id'] not in k2pkdict[__v][row[__v]]:
								k2pkdict[__v][row[__v]].append(row['id'])
						except:
							k2pkdict[__v][row[__v]] = []
						#k2pkdict[__v][row[__v]] = row['id']
				result_dict[row['id']] = row
		self.k2pkdict = k2pkdict
		return result_dict

	def chk_query(self, query):
		result = True
		if query == None or type(query) != 'dict':
			_query = set(query)
			_col_name_list = set(self.col_name_list)
			if len(_query&_col_name_list) != len(query):
				result = False
		print 'result: ', result
		return result
		
	def get(self, key):
		return self.pk2vdict[key]

	def get_all(self):
		return self.pk2vdict
	
	def get_query(self, query):
		query_result = {}
		for _k, _v in query.items():
			if _v in self.k2pkdict[_k]:
				pklist = self.k2pkdict[_k][_v]
				for i in xrange(len(pklist)):
					query_result[pklist[i]] = self.get(pklist[i])
		print 'self.col_name_list: ', self.col_name_list
		print 'query_result: ', query_result
		return query_result

	def find(self, query):
		print 'query: ', query
		query_result = {}
		if self.chk_query(query):
			query_result = self.get_query(query)
		return query_result

if __name__ == '__main__':
	p = CCsvParser("task.csv")
	#print p.pk2vdict
	id = '10001'
	#print p.get_all()
	mql = {'snpc':'200000001'}
	#mql = {'id':'10001'}
	#r = p.find(mql)
	r = p.get(id)
	#r = p.get_all()
	#print p.pk2vdict.keys()
	print r
