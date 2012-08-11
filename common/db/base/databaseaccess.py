#!/usr/bin/env python
import pymongo
from pymongo import (connection,
		     database,
		     collection)

""" DataBass Access for Mongodb
"""
class DataBaseAccess:
	""" DataBaseAccess Class
            self.Con
            self.Db
	"""
	def __init__(self,Address = None,Port = None,Db = None):
		""" init function, 
		    Address is type of string,Port is type of int,Db is type of string
	        """
		self.Con=connection.Connection(Address,Port)
		
		#print "#print self.Con..."
		#print self.Con
		
		if Db is None:
			self.Db=None
		else:	
			self.Db=database.Database(self.Con,Db)
			#print "#print self.Db..."
			#print self.Db	
		
			#print "#print collection"
			l=self.Db.collection_names()	
			#print l	
 		
	def set_database(self,DbName):
		""" set Database
		    DbName is type of string
		"""
		self.Db=database.Database(self.Con,DbName)
	
	def insert(self,ColName,MongoStrList):
		""" insert data,
		    ColName is Name of Collection
		    MongoStrList is a document or list of document
		"""
		if self.Db is None:
			return 
		Col=collection.Collection(self.Db,ColName)
		
		#print Col
		#print MongoStrList
	        Col.insert(MongoStrList)	
				
	def update(self,ColName,MongoStrList):
		""" update data,
		    ColName is Name of Collection
		    MongoStrList is type of list which contain two dictionary
		"""
		if self.Db is None:
			return
		Col=collection.Collection(self.Db,ColName)
		#print MongoStrList
		Col.update(MongoStrList[0],MongoStrList[1])
		
	def query(self,ColName,MongoStrList):
		""" query documents
		    MongoStrList is type of dictionary
		"""
		if self.Db is None:
			return
		Col=collection.Collection(self.Db,ColName)
		#print MongoStrList
		Result = Col.find(MongoStrList)
		return Result

	def query_one(self,ColName,MongoStrList):	
		""" query single document
		    MongoStrList is type of dictionary
		"""
		if self.Db is None:
			return
		Col=collection.Collection(self.Db,ColName)
		#print MongoStrList
		Result = Col.find_one(MongoStrList)
		return Result

	def remove(self,ColName,MongoStrList):
		""" remove date
		    MongoStrList is type of dictionary 
		"""
		if self.Db is None:
			return
		Col=collection.Collection(self.Db,ColName)
		#print MongoStrList
		#print Col
		Col.remove(MongoStrList)
			
