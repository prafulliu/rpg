# -*- coding: utf-8 -*-

CAT_PLAYER = 0x00000001





CMD = {}
def cmd(mod, name, val):
	ACK  = "%s_%s_ACK" % (mod, name)
	REP  = "%s_%s_REP" % (mod, name)
	NOTI = "%s_%s_NOTI" % (mod, name)
	
	mod = "CAT_%s" % (mod) 
	CMD[mod] = 0x00000000
	ack_val   = CMD[mod] + val
	rep_val   = ack_val + 0x00010000
	noti_val  = ack_val + 0x00020000 
	
	CMD[ACK]  = ack_val
	CMD[REP]  = rep_val
	CMD[NOTI] = noti_val


if __name__ == "config.cmd":
#if __name__ == "common.config.CMD":
#if __name__ == "__main__":
	cmd("PLAYER", "CHECK_PLAYER", 				1)
	cmd("PLAYER", "GET_RECOMMAND_PLAYER_INFO",	2)
	cmd("PLAYER", "CREATE_PLAYER", 				3)
