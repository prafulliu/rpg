# -*- coding: utf-8 -*
#
# created by: liup Pengfei
import os
import time
import config.playerconfig as playerconfig
import db.base.mongoconf as mongoconf
import config.mapconfig as mapconfig
from db.base.databaseaccess import CDataBaseAccess
from db.base.autoincpk import CAutoIncPk
from log.log import LOG, TYPE

rpg_access = CDataBaseAccess(mongoconf.IP, mongoconf.PORT,
							mongoconf.DB_RPG)
COL_TASK = mongoconf.COL_TASK

class CTask():
	#创建角色
	def __init__(self, playerid, taskid):
		_id = CAutoIncPk().get_pk_by_name(COL_TASK)
		self._id					 = _id

		self.playerid				 = playerid
		self.taskid			         = taskid
		rpg_access.insert(COL_TASK, vars(self))

def check_playerid(playerid):
	player = rpg_access.query_one(COL_PLAYER, {'playerid':playerid})
	return player

def check_taskid(taskid):
	
def crate_task(playerid, task):
	retVal = {}
	if check_playerid(playerid):
		result = 0
	else:
		result = 1

	retVal['result'] = result
	return result

if __name__ == "__main__":
	pass
