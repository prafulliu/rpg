#!/usr/bin/env python
# -*- coding: utf-8 -*
import pymongo
from pymongo import (connection,
					database,
					collection)
class CDataBaseAccess:
	def __init__(self,ip=None, port=None,db = None):
		self.con=connection.Connection(ip, port)
		if db is None:
			self.db=None
		else:
			self.db=database.Database(self.con, db)
		l=self.db.collection_names()

	def set_database(self,db_name):
		self.db=database.Database(self.con,db_name)

	def insert(self,col_name,record):
		if self.db is None:
			return
		col=collection.Collection(self.db,col_name)
		col.insert(record)

	def update(self,col_name,record):
		if self.db is None:
			return
		col=collection.Collection(self.db,col_name)
		print record
		col.update(record[0],record[1])

	def query(self,col_name,record):
		if self.db is None:
			return
		col=collection.Collection(self.db,col_name)
		print record
		result = col.find(record)
		return result

	def query_one(self,col_name,record):	
		if self.db is None:
			return
		col=collection.Collection(self.db,col_name)
		print record
		result = col.find_one(record)
		return result

	def remove(self,col_name,record):
		if self.db is None:
			return
		col=collection.Collection(self.db,col_name)
		print record
		print col
		col.remove(record)

	def save(self,col_name, record):
		if self.db is None:
			return
		col=collection.Collection(self.db, col_name)
		col.save(record)
