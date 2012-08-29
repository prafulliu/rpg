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

TASK_CSV =  CCsvParser("task.csv")

class CTask():
	#创建任务
	def __init__(self, playerid, id):
		_id = CAutoIncPk().get_pk_by_name(COL_TASK)
		self._id					 = _id

		self.playerid				 = playerid
		self.taskid			         = id
		self.state                   = taskconfig.STATE_UNDONE
		self.type                    = int(TASK_CSV.get(id)['type'])
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


def get_num_reward(task_temp):
	num_reward = {}
	if task_temp['r_exp'] != '':
		_num_reward['name'] = '经验值'	
		_num_reward['num']  = task_temp['r_exp']
		num_reward.append(_num_reward)

	if task_temp['r_silver'] != '':
		_num_reward['name'] = '银锭'	
		_num_reward['num']  = task_temp['r_silver']
		num_reward.append(_num_reward)
	
	if task_temp['r_gold'] != '':
		_num_reward['name'] = '金锭'	
		_num_reward['num']  = task_temp['r_gold']
		num_reward.append(_num_reward)

	if task_temp['r_jade'] != '':
		_num_reward['name'] = '玉贝'	
		_num_reward['num']  = task_temp['r_jade']
		num_reward.append(_num_reward)

	if task_temp['r_prestige'] != '':
		_num_reward['name'] = '威望值'	
		_num_reward['num']  = task_temp['r_prestige']
		num_reward.append(_num_reward)

	if task_temp['r_master'] != '':
		_num_reward['name'] = '师徒值'	
		_num_reward['num']  = task_temp['r_master']
		num_reward.append(_num_reward)

	if task_temp['r_conjugal'] != '':
		_num_reward['name'] = '夫妻值'	
		_num_reward['num']  = task_temp['r_conjugal']
		num_reward.append(_num_reward)

	if task_temp['r_integral'] != '':
		_num_reward['name'] = '任务积分'	
		_num_reward['num']  = task_temp['r_integral']
		num_reward.append(_num_reward)

	if task_temp['r_point'] != '':
		_num_reward['name'] = '奖励任务点'	
		_num_reward['num']  = task_temp['r_point']
		num_reward.append(_num_reward)

	return num_reward

def get_item_reward(task_temp):
	item_reward = {}
	print 'task_temp["r_item"]: ',  task_temp['r_item']
	if task_temp['r_item'] != '':
		item_reward['item_tmpl'] = task_temp['r_item']['item_tmpl']	
		item_reward['count']	 = task_temp['r_item']['count']	
		item_reward['icon']	     = task_temp['r_item']['icon']	
		item_reward['name']		 = task_temp['r_item']['name']	
	return item_reward

def get_targetlist(task, task_temp):
    if task['state'] ==  taskconfig.STATE_DONE:
        targetlist = task_temp['task_reward']
    elif task['state'] ==  taskconfig.STATE_UNDONE:
        targetlist = task_temp['task_down']
    elif task['state'] ==  taskconfig.STATE_UNDERWAY:
        targetlist = task_temp['task_down']
    print 'targetlist: ', targetlist
    return targetlist

def get_task_info(task):
	task_info = {}
	task_temp = TASK_CSV.get(task['taskid'])
	task_info['state']		= task['state']	
	task_info['lv']			= task_temp['min_lv']	
	task_info['id']			= task_temp['id']	
	task_info['name']		= task_temp['name']	
	#task_info['desc']		= task_temp['desc']	
	task_info['chapter']	= task_temp['chapter']	
	task_info['targetlist'] = get_targetlist(task, task_temp)
	task_info['num_reward']	= get_num_reward(task_temp)
	task_info['item_reward']= get_item_reward(task_temp)
	print 'task_info: ', task_info

def get_current_tasklist(player):
	tasklist = []
	for i in taskconfig.TASK_TYPE:
		_tasklist = rpg_access.query(COL_TASK, {'playerid':playerid, 'type':i}).sort("type")
		if _tasklist.count() != 0:
			__tasklist = {}
			__tasklist['total_cnt'] = _tasklist.count()
			__tasklist['type'] = i
			__tasklist['succ_cnt'] = 0
			for _task in _tasklist:
				task = []
				if _task['state'] == taskconfig.STATE_DONE:
					__tasklist['succ_cnt'] = __tasklist['succ_cnt'] + 1
				task.append(get_task_info(_task))
			tasklist.append(__tasklist)
	return tasklist

def get_can_accept_tasklist(player):
	tasklist = []
	for i in taskconfig.TASK_TYPE:
		_tasklist = rpg_access.query(COL_TASK, {'playerid':playerid, 'type':i}).sort("type")
		_player_curlv_tasklist = TASK_CSV.find({'min_lv':str(player['lv'])})
		#_player_nextlv_tasklist = TASK_CSV.find({'min_lv':playerid['lv']+1})
	
		print _player_curlv_tasklist
		#print _player_nextlv_tasklist
	#	if _tasklist.count() != 0:
	#		__tasklist = {}
	#		__tasklist['total_cnt'] = _tasklist.count()
	#		__tasklist['type'] = i
	#		__tasklist['succ_cnt'] = 0
	#		for _task in _tasklist:
	#			task = []
	#			if _task['state'] == taskconfig.STATE_DONE:
	#				__tasklist['succ_cnt'] = __tasklist['succ_cnt'] + 1
	#			task.append(get_task_info(_task))
	#		tasklist.append(__tasklist)
	print tasklist


def get_tasklist_board(playerid, model):
	retVal = {}
	player = check_playerid(playerid)
	if player:
		if check_model(model):
			if model == taskconfig.CURRENT_TASK:
				#返回当前任务
				tasklist = get_current_tasklist(player)
				pass
			elif model == taskconfig.CAN_ACCEPT_TASK:
				#返回可接任务
				tasklist = get_can_accept_tasklist(player)
				pass
			retVal['tasklist'] = tasklist
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
	model = 2
	#r = create_task(playerid, id)
	r = get_tasklist_board(playerid, model)
	print r
