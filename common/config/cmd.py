# -*- coding: utf-8 -*-
import util.pattern as pattern



CAT = {\
	   "PLAYER" : 0x00000000,
	   "TASK"   : 0x02000000
	   }

CMD = {}

def cmd(mod, name, val):
	ACK  = "%s_%s_ACK" % (mod, name)
	REP  = "%s_%s_REP" % (mod, name)
	NOTI = "%s_%s_NOTI" % (mod, name)
	
	mod = CAT[mod]
	CMD[mod] = mod
	ack_val   = CMD[mod] + val
	rep_val   = ack_val + 0x00010000
	noti_val  = ack_val + 0x00020000 
		
	CMD[ACK]  = ack_val
	CMD[REP]  = rep_val
	#CMD[NOTI] = noti_val


cmd("PLAYER", "CHECK_PLAYER", 				1)
cmd("PLAYER", "GET_RECOMMAND_PLAYER_INFO",	2)
cmd("PLAYER", "CREATE_PLAYER", 				3)
	
cmd("TASK", "GET_TASKLIST_BOARD",			1)
cmd("TASK", "GET_TASKLIST_TRACE",			2) 
cmd("TASK", "GET_ENTRUST_TASKLIST",         3)
cmd("TASK", "ACCEPT",						4)
cmd("TASK", "DROP",							5)
cmd("TASK", "ACCOMPLISH",					6)
cmd("TASK", "GET_NPC_TALK",					7)
cmd("TASK", "GET_ENTRUST_TIME_LEFT",		8)
cmd("TASK", "POST_ENTRUST_TASKLIST",		9)
cmd("TASK", "GET_TASK_REWARD",			   10)

if __name__ == "__main__":
	for key in CMD:
		print key, pattern.to_hex(CMD[key])
	pass
