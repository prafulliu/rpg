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

rpg_access       = CDataBaseAccess(mongoconf.IP, mongoconf.PORT, mongoconf.DB_RPG)

COL_TASK         = mongoconf.COL_TASK
COL_PLAYER       = mongoconf.COL_PLAYER
COL_ENTRUST_TASK = mongoconf.COL_ENTRUST_TASK
TASK_CSV         =  CCsvParser("task.csv")

class CTask():
	#创建任务
	def __init__(self, playerid, id):
		_id           = CAutoIncPk().get_pk_by_name(COL_TASK)
		self._id      = _id
		self.playerid = playerid
		self.id       = id
		self.state    = taskconfig.STATE_UNDONE
		self.type     = TASK_CSV.get(id)['type']
		self.num      = 0
		rpg_access.insert(COL_TASK, vars(self))

class CEntrustTask(object):
	#新建委托任务
	def __init__(self, playerid, id_list, time_req):
		_id           = CAutoIncPk().get_pk_by_name(COL_ENTRUST_TASK)
		self._id      = _id
		self.playerid = playerid
		self.id_list  = id_list
		self.time_req = time_req
		rpg_access.insert(COL_ENTRUST_TASK, vars(self))
		
def check_playerid(playerid):
	player = rpg_access.query_one(COL_PLAYER, {'_id':playerid})
	return player

def check_id(id):
	task_temp = TASK_CSV.get(id)
	return task_temp

def check_player_task(player, id):
	result = False
	if task_temp:
		#该任务id存在
		if player.lv >= task_temp.min_lv  and player.lv <= task_temp.max_lv:
			task = rpg_access.query_one(COL_TASK, {'playerid':player._id})
			if task:
				#该任务接过
				if task_temp.can_loop == 1 and task.num < task_temp.max_loop:
					result = True
			else:	
				result = True

def create_task(playerid, id):
	retVal = {}
	player = check_playerid(playerid)
	if player:
		if check_player_task(player, id):
			CTask(playerid, id)
			result = 0
		else:
			result = 1
	else:
		result = -1
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

def get_player_daily_task_num(playerid):
	task_count = rpg_access.query(COL_TASK, {'playerid':playerid, 'type':taskconfig.TASK_TYPE['DAILY']}).count()
	return task_count

def get_num_reward(task_temp):
	num_reward = []
	if task_temp['r_exp'] != '':
		_num_reward = {}
		_num_reward['name'] = '经验值'	
		_num_reward['num']  = task_temp['r_exp']
		num_reward.append(_num_reward)

	if task_temp['r_silver'] != '':
		_num_reward = {}
		_num_reward['name'] = '银锭'	
		_num_reward['num']  = task_temp['r_silver']
		num_reward.append(_num_reward)
	
	if task_temp['r_gold'] != '':
		_num_reward = {}
		_num_reward['name'] = '金锭'	
		_num_reward['num']  = task_temp['r_gold']
		num_reward.append(_num_reward)

	if task_temp['r_jade'] != '':
		_num_reward = {}
		_num_reward['name'] = '玉贝'	
		_num_reward['num']  = task_temp['r_jade']
		num_reward.append(_num_reward)

	if task_temp['r_prestige'] != '':
		_num_reward = {}
		_num_reward['name'] = '威望值'	
		_num_reward['num']  = task_temp['r_prestige']
		num_reward.append(_num_reward)

	if task_temp['r_master'] != '':
		_num_reward = {}
		_num_reward['name'] = '师徒值'	
		_num_reward['num']  = task_temp['r_master']
		num_reward.append(_num_reward)

	if task_temp['r_conjugal'] != '':
		_num_reward = {}
		_num_reward['name'] = '夫妻值'	
		_num_reward['num']  = task_temp['r_conjugal']
		num_reward.append(_num_reward)

	if task_temp['r_integral'] != '':
		_num_reward = {}
		_num_reward['name'] = '任务积分'	
		_num_reward['num']  = task_temp['r_integral']
		num_reward.append(_num_reward)

	if task_temp['r_point'] != '':
		_num_reward = {}
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

def get_task_info(task_temp):
	task_info = {}
	task_info['lv']			= task_temp['min_lv']	
	task_info['id']			= task_temp['id']	
	task_info['name']		= task_temp['name']	
	#task_info['desc']		= task_temp['desc']	
	task_info['chapter']	= task_temp['chapter']	
	task_info['num_reward']	= get_num_reward(task_temp)
	task_info['item_reward']= get_item_reward(task_temp)

	print 'task_info: ', task_info

def get_current_tasklist(player):
	tasklist = []
	for i in (taskconfig.TASK_TYPE):
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
				task_temp = TASK_CSV.get(task['id'])
				task_info['taskid']		= task['_id']	
				task_info['state']		= task['state']	
				task_info['targetlist'] = get_targetlist(task, task_temp)
				_task_info = get_task_info(task_tmp)
				task.append(_task_info)
			tasklist.append(__tasklist)
	return tasklist

def get_can_accept_tasklist(player):
	tasklist = []
	for type in xrange(1, len(taskconfig.TASK_TYPE)+1):
		#_tasklist = rpg_access.query(COL_TASK, {'playerid':playerid, 'type':i+1}).sort("type")
		_player_curlv_tasklist = TASK_CSV.find({'min_lv':player['lv'],\
										  'type':type})
		_player_nextlv_tasklist = TASK_CSV.find({'min_lv':(player['lv']+1),
										   'type':type})
		_tasklist = _player_curlv_tasklist.copy()
		_tasklist.update(_player_nextlv_tasklist)
		
		#print '_player_curlv_tasklist result: ', len(_player_curlv_tasklist)
		#print '_player_nextlv_tasklist  result: ', len(_player_nextlv_tasklist )
		#print '_player_tasklist  result: ', len(_player_tasklist )

		if _tasklist != {}:
			__tasklist = {}
			__tasklist['type'] = type
			for _key, _task in _tasklist.iteritems():
				_task_info = get_task_info(_task)
				_task_info['state']		= get_task_state()
				task.append(_task_info)
			tasklist.append(__tasklist)
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
	
def accept(playerid, id):
	retVal = {}
	player = check_playerid(playerid)
	if player:
		result = create_task(playerid, id)
	else:
		result = -1
	retVal['result'] = result
	return retVal

def is_accept(playerid, taksid):
	result = False;
	task = rpg_access.query_one(COL_TASK, {'_id':taksid, 'playerid':playerid})
	if task:
		if task.state != taskconfig.STATE_SUBMITTED:
			result = True

def drop(playerid, taksid):
	retVal = {}
	player = check_playerid(playerid)
	if player:
		if is_accept(playerid, taksid):
			rpg_access.remove(COL_TASK, {'_id':taksid})
			result = 0
		else:
			result = 1
	else:
		result = -1
	retVal['result'] = result
	return retVal

def is_done(playerid, taskid):
	result = False;
	task = rpg_access.query_one(COL_TASK, {'_id':taksid, 'playerid':playerid})
	if task:
		if task.state == taskconfig.STATE_DONE:
			result = True

def is_submitted(playerid, taskid):
	result = False;
	task = rpg_access.query_one(COL_TASK, {'_id':taksid, 'playerid':playerid})
	if task:
		if task.state == taskconfig.STATE_SUBMITTED:
			result = True


def deliver_reward(player, id):
	task_temp = TASK_CSV.find(id)


def accomplish(playerid, taskid, item_tmpl_list):
	retVal = {}
	player = check_playerid(playerid)
	if player:
		if is_done(playerid, taksid):
			task = rpg_access.query_one(COL_TASK, {'_id':taksid})
			if check_item_tmpl_list(item_tmpl_list):
				if deliver_reward(player, task['id']):
					task.state = taskconfig.STATE_SUBMITTED
					result = 0
				else:
					result = 3
			else:
				result = 2
		else:
			result = 1		
	else:
		result = -1
	retVal['result'] = result
	return retVal

def is_daily_task_full(playerid):
	result = True
	if get_player_daily_task_num(playerid) < taskconfig.TASK_MAX:
		result = False
	return result

def get_time_req(id_list):
	return taskconfig.ENTRUST_TIME_NEED * len(id_list)

def create_entrust_task(playerid, id_list):
	time_req = get_time_req(id_list)
	CEntrustTask(playerid, id_list, time_req)
	return time_req

def is_entrusting(playerid):
	return rpg_access.query_one(COL_ENTRUST_TASK, {'playerid':playerid})


def post_entrust_tasklist(playerid, id_list):
	retVal = {}
	player = check_playerid(playerid)
	if player:
		if check_id_list(id_list):
			if not is_daily_task_full(playerid):
				if is_entrusting(playerid):
					time_req = create_entrust_task(playerid)
					retVal['time_req'] = time_req
					result = 0					
				else:
					result = 3
			else:
				result = 2
		else:
			result = 1
	else:
		result = -1
	retVal['result'] = result
	return retVal

def get_entrust_time_left(playerid):
	retVal = {}
	player = check_playerid(playerid)
	if player:
		task = is_entrusting(playerid)
		if task:
			time_diff = time.time() - task.time_start

			if time_diff >= task.time_req:
				time_left = 0
			else:
				time_left = task.time_req - time_diff
			retVal['time_left'] = time_left
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
	#print r
