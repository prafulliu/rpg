# -*- coding: utf-8 -*

#当前任务
CURRENT_TASK    = 1
#已接任务
CAN_ACCEPT_TASK = 2

#日常任务最大可接个数
TASK_MAX = 20

#任务状态
STATE_DONE      = 1	#已完成
STATE_UNDONE    = 2 #未完成
STATE_UNDERWAY  = 3 #进行中
STATE_CAN_APPLY = 4 #可接
STATE_SUBMITTED = 5 #已提交

TASK_TYPE =[	#任务类型
	'MAIN'  : 1,	#主线任务
	'BRANCH': 2,	#支线任务
	'DAILY' : 3,	#日常任务
	'LOOP'  : 4,	#循环任务
	'EVENT' : 5   #活动任务
	]

#单次委托任务所需时间
ENTRUST_TIME_NEED = 400