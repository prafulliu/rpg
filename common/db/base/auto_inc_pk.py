# -*- coding: utf-8 -*
import pymongo
connection = pymongo.Connection()
db = connection.rpg
collection = db.auto_inc_pk

class CAutoIncPk():
	def __init__(self, table_name, pk=0):
		if self.is_existed(table_name):
			pass
		else:
			self.table_name = table_name
			self.pk         = pk
			collection.insert(vars(self))
			
	def is_existed(self, table_name):
		result = False
		if table_name:
			table = collection.find_one({"table_name":table_name})
			if table:
				result = True
		return result
	
	def get_pk_by_name(self, table_name):
		pk = None
		if table_name:
			table = collection.find_one({"table_name":table_name})
			if table:
				pk =  table["pk"]
				table["pk"] = table["pk"] + 1
				collection.save(table)
		return pk

if __name__ == "__main__":
	table_name = 'item'
	t = AutoIncPk(table_name)
	#print get_pk_by_name(table_name)
