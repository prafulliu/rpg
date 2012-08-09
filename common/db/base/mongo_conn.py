# -*- coding: utf-8 -*
import pymongo
import db.base.auto_inc_pk as auto_inc_pk
import db.base.collection_name as collection_name

class CMongoConn():
	#def __init__(self, col, db=collection_name.DB, ip='192.168.16.99', port=27017):
	def __init__(self, col, db=collection_name.DB, ip='localhost', port=27017):
		self._dbconn = pymongo.Connection(ip, port)
		self._db = self._dbconn[db]
		self._col = self._db[col]
		self._auto_inc_pk = auto_inc_pk.CAutoIncPk(col)
		
	def get_db(self):
		return self._db
	
	def get_collection(self):
		return self._col
	
	def get_aut_inc_pk(self):
		return self._auto_inc_pk


# if __name__ == "__main__":
	# db = 'rpg'
	# tab = 'job'
	# conn = CMongoConn(tab)

