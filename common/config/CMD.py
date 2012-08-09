# -*- coding: utf-8 -*-

CAT_PLAYER = 0x00000001


def CMD(mod, name, val):
    ACK  = "%s_%s_ACK" % (mod, name)
    REP  = "%s_%s_REP" % (mod, name)
    NOTI = "%s_%s_NOTI" % (mod, name)
    
    mod = "CAT_%s" % (mod) 
    cmd[mod] = 0x00000000
    ack_val   = cmd[mod] + val
    rep_val   = ack_val + 0x00010000
    noti_val  = ack_val + 0x00020000 
    
    cmd[ACK]  = ack_val
    cmd[REP]  = rep_val
    cmd[NOTI] = noti_val

cmd = {}

if __name__ == "config.CMD":
#if __name__ == "common.config.CMD":
#if __name__ == "__main__":
    
    CMD("PLAYEROUT", "CHECK_PLAYER", 				1)
    CMD("PLAYEROUT", "GET_RECOMMAND_PLAYER_INFO",	2)
    CMD("PLAYEROUT", "CREATE_PLAYER", 				3)
