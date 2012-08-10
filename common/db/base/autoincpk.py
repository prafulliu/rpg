# -*- coding: utf-8 -*
import pymongo
import mongoconf

IP = mongoconf.IP
PORT = mongoconf.PORT
DB = mongoconf.DB_SERVER
COL = mongoconf.COL_AUTO_INC_PK

class CAutoIncPk():
    def __init__(self, ip=IP, port=PORT, db=DB, col=COL):
		print 'called __init__'
		self._conn = pymongo.Connection(ip, port)
		self._db = self._conn[db]
		self._col = self._db[col]

    def get_pk_by_name(self, col_name):
		print 'called get_pk_by_name'
		if not col_name:
			raise AssertionError('col_name should not be None')
		col = self._col.find_one({'_id':'identity_key'})
		if col:
			try:
				pk = col[col_name]
				col[col_name] = col[col_name] + 1
				self._col.save(col)
			except:
				col[col_name] = 0
				self._col.save(col)
				pk = 0
		print 'pk: ', pk
		return pk
    
if __name__ == "__main__":
	c = CAutoIncPk(mongoconf.IP, mongoconf.PORT, mongoconf.DB_SERVER, mongoconf.COL_AUTO_INC_PK)
	print c.get_pk_by_name(col_name)
