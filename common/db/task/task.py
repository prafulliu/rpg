# -*- coding: utf-8 -*
#
# created by: liup Pengfei
import os
import time
import config.playerconfig as playerconfig
import config.taskconfig as taskconfig
import db.base.mongoconf as mongoconf
import config.mapconfig as mapconfig
from util.csvparser import CCsvParser
from db.base.databaseaccess import CDataBaseAccess
from db.base.autoincpk import CAutoIncPk
from log.log import LOG, TYPE

rpg_access = CDataBaseAccess(mongoconf.IP, mongoconf.PORT,
							mongoconf.DB_RPG)

COL_TASK = mongoconf.COL_TASK
COL_PLAYER  = mongoconf.COL_PLAYER

TASK_CSV =  CCsvParser.parse("task.csv")

class CTask():
	#创建任务
	def __init__(self, playerid, id):
		_id = CAutoIncPk().get_pk_by_name(COL_TASK)
		self._id					 = _id

		self.playerid				 = playerid
		self.taskid			         = id
		rpg_access.insert(COL_TASK, vars(self))

def check_playerid(playerid):
	player = rpg_access.query_one(COL_PLAYER, {'_id':playerid})
	return player

def check_taskid(taskid):
	pass	

def create_task(playerid, id):
	retVal = {}
	player = check_playerid(playerid)
	if player:
		CTask(playerid, id)
		result = 0
	else:
		result = 1
	retVal['result'] = result
	return result

def check_model(model):
	if model in [1, 2]:
		result = True
	else:
		result = False
	return result

def get_player_cur_task_num(playerid):
	task_count = rpg_access.query(COL_TASK, {'playerid':playerid}).count()
	return task_count

def get_can_accept_tasklist(playerid):
	pass

def get_current_tasklist(playerid):
	pass

def get_tasklist_board(playerid, model):
	retVal = {}
	player = check_playerid(playerid)
	if player:
		if check_model(model):
			if model == taskconfig.CURRENT_TASK:
				pass
			elif model == taskconfig.CAN_ACCEPT_TASK:
				pass
			retVal['max'] = taskconfig.TASK_MAX
			retVal['now'] = get_player_cur_task_num(playerid);
			result = 0
		else:
			result = 1	
	else:
		result = -1
	retVal['result'] = result
	return retVal




if __name__ == "__main__":
	playerid = 28
	id = '10001'
	model = 1
	#print create_task(playerid, id)
	r = get_tasklist_board(playerid, model)
	print r
