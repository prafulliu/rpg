# -*- coding: utf-8 -*
from db.base.DataBaseAccess import DataBaseAccess
import db.base.mongo_conf as mongo_conf

server_access = DataBaseAccess(mongo_conf.ADDRESS, mongo_conf.PORT,
                                                      mongo_conf.DB_SERVER)
COL_AUTO_INC_PK = mongo_conf.AUTO_INC_PK

def get_pk_by_name(col_name):
    if not col_name: raise AssertionError('col_name should not be None')
    col = server_access.query_one(COL_AUTO_INC_PK, {'_id':'identity_key'})
    if col:
        #try:
        print 'right'
        pk = col[col_name]
        col[col_name] = col[col_name] + 1
        server_access.insert(COL_AUTO_INC_PK, col)
        #except:
        #    print 'error'
        #    server_access.insert(COL_AUTO_INC_PK, {'_id':'identity_key', col_name:0})
        #    pk = 0
    print 'p', pk
    return pk

if __name__ == "__main__":
	col_name = 'player'
	#col_name = None
	print get_pk_by_name(col_name)
