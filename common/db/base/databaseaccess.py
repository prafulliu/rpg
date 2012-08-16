#!/usr/bin/env python
import pymongo
from log.log import LOG, TYPE
from pymongo import (connection,
		     database,
		     collection)

""" data_base access for mongodb
"""
class CDataBaseAccess:
	""" databaseaccess Class
            self.con
            self.db
	"""
	def __init__(self,address = None,port = None,db = None):
		""" init function, 
		    address is type of string,port is type of int,db is type of string
	        """
		self.con=connection.Connection(address,port)
		
		LOG.info("self.con: %s" % (self.con))
		
		if db is None:
			self.db=None
		else:	
			self.db=database.Database(self.con,db)
			LOG.info("self.db: %s" % (self.con))
			LOG.info("collection: %s" % (self.db.collection_names()))
 		
	def set_database(self,db_name):
		""" set Database
		    db_name is type of string
		"""
		self.db=database.Database(self.con,db_name)
	
	def insert(self,col_name,record):
		""" insert data,
		    col_name is Name of collection
		    record is a document or list of document
		"""
		if self.db is None:
			return
		col=collection.Collection(self.db,col_name)
		LOG.info("col:: %s" % (col))
		LOG.info("record: %s" % (record))
		try:
	        	ret = col.insert(record,safe = True)
			LOG.info("ret is :%s" % (ret))
		except:
			return False
		return True	
				
	def update(self,col_name,record):
		""" update data,
		    col_name is Name of collection
		    record is type of list which contain two dictionary
		"""
		result = True
		if self.db is None:
			result = False
		col=collection.Collection(self.db,col_name)
		LOG.info("record: %s" % (record))
		try:
			ret = col.update(record[0],record[1],safe=True)
			LOG.info("ret: %s" % (ret))
			if ret['update_existing'] == True:
                                result = True
                        else:
                                result = False
		except:
			result = False
		return result
	
	def update_enhance(self,col_name,id_dict,operate_str,mongo_str_dict):
		""" update data with operate_str,
                    col_name is name of collection
		    operate_str (e.g. "$set","$inc")
                    record is type of list which contain two dictionary
                """
		result = True
                if self.db is None:
                        result = False
                col=collection.Collection(self.db,col_name)
		
		set_value_dict={}
		set_value_dict[operate_str] = mongo_str_dict
		
		record = []
		record.append(id_dict)
		record.append(set_value_dict)
		LOG.info("record: %s" % (record))
		
		try:
			ret = col.update(record[0],record[1],safe=True)			
			LOG.info("ret: %s" % (ret))
			if ret['update_existing'] == False:
				result = False
		except:
			result = False
		return result
		
	def query(self,col_name,record,skip_num = None,limit_num = None,fields = None,sort = None):
		""" query documents
		    record is type of dictionary
		"""
		if self.db is None:
			return
		col=collection.Collection(self.db,col_name)
		LOG.info("record: %s" % (record))
		
		if skip_num != None and limit_num != None:
                        result = col.find(record,skip=skip_num,limit=limit_num,fields=fields,sort=sort)
                elif skip_num != None:
                        result = col.find(record,skip=skip_num,fields=fields,sort=sort)
                elif limit_num != None:
                        result = col.find(record,limit=limit_num,fields=fields,sort=sort)
                else:
                        result = col.find(record,fields=fields,sort=sort)
		return result

	def query_one(self,col_name,record,fields=None):	
		""" query single document
		    record is type of dictionary
		"""
		if self.db is None:
			return
		col=collection.Collection(self.db,col_name)
		LOG.info("record: %s" % (record))
		result = col.find_one(record,fields=fields)
		LOG.info("result: %s" % (result))
		return result

	def remove(self,col_name,record):
		""" remove date
		    record is type of dictionary 
		"""
		result = True
		if self.db is None:
			result = False
		col=collection.Collection(self.db,col_name)
		LOG.info("record: %s" % (record))
		LOG.info("col: %s" % (col))
		try:
			ret = col.remove(record,safe=True)
			LOG.info("ret is :%s" % (ret))
			if ret["n"] == 0L:
				result = False
			
		except:
			result = False
		return result

	def save(self,col_name, record):
		if self.db is None:
			return
		col=collection.Collection(self.db, col_name)
		col.save(record)
