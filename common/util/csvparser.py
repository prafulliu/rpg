# -*- coding:utf-8 -*-

import csv
import os
from StringIO import StringIO
import cProfile
#path:  /home/liupf/rpg/common/util
#_p:    /home/liupf/rpg/co/template/task.csv


def get_file_path(file):
	abspath = os.path.abspath(__file__)
	path = os.path.split(abspath)[0]
	path = path[0:len(path)-len('util')]+'template/'+file
	return path

class CCsvParser:
	def __init__(self, file):
		self.file    = file
		self.col_name_list = []
		self.k2pkdict = {}
		self.pk2vdict = self.parse()

	def trans_type(self, _dict):
		for k, v in _dict.iteritems():
			if type(v) == type([]):
				_v = []
				for i in xrange(1,len(v)):
					_v.append(trans_type(v[i]))
				_dict[k] = v
			elif type(v) == type('a'):
				try:
					_dict[k] = int(v)
				except:
					if v == '':
						_dict[k] = None
		return _dict

	def parse(self):
		input_file = get_file_path(self.file)
		src = file(input_file, "rb")
		line = src.readline()
		heading = [_head.strip() for _head in line.split(",")]
		self.col_name_list = heading 
		return self._parse_csv(input_file, heading, skip=1)

	def _parse_csv(self, input_file, csv_heading, skip=0):
		src = file(input_file, "rb")
		reader = csv.DictReader(src, csv_heading)
		# skip the first line
		for i in xrange(skip):
			reader.next()
		result_dict = {}
		k2pkdict = {}
		for head in csv_heading:
			k2pkdict[head] = {}
		pk = csv_heading[0]
		for row in reader:
			for _k, _v in row.iteritems():
				row[_k] = _v.strip()
			result_dict[row[pk]] = self.trans_type(row)

		for k, v in result_dict.iteritems():
			for head in csv_heading:
				k2pkdict[head].setdefault(v[head], set([])).add(k)

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
		for _k, _v in query.iteritems():
			if _v in self.k2pkdict[_k]:
				pklist = list(self.k2pkdict[_k][_v])
				print 'pklist: %s' % (pklist)
				for i in xrange(len(pklist)):
					query_result[pklist[i]] = self.get(pklist[i])
		return query_result

	def find(self, query):
		print 'query: ', query
		query_result = {}
		if self.chk_query(query):
			query_result = self.get_query(query)
		return query_result

def main():
	p = CCsvParser("task.csv")
	#print p.pk2vdict
	id = 10001
	#print p.get_all()
	# mql = {'snpc':'200000001'}
	mql = {'id':10001}
	r = p.find(mql)
	print r
	# for i in xrange(10):
	# 	r = p.get(id)
	# 	print r
	# 	id = id + i


if __name__ == '__main__':
	#cProfile.run("main()")
	# main()
	get_file_path('task.csv')
	
