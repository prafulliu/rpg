# -*- coding: utf-8 -*-
import struct
import gevent
import sys
import ctypes

from gevent import socket
from gevent import event
from gevent.queue import Queue
from amfast.decoder import Decoder
from amfast.encoder import Encoder
import db.player.player as player
from log.log import LOG, TYPE
from config.cmd import CMD
from network.conn2center import CConn2Center
from config import config

LOG.setLevel(TYPE.DEBUG)

def create_player(conn, playerid, rqstid, pkt):
	LOG.info("conn: %s, playerid: %s, rqstid: %s, pkt: %s" % (conn, playerid,
														   rqstid, pkt))
	retVal = player.create_player(pkt["name"], pkt["camp"], pkt["occupation"], pkt["passport_id"])
	LOG.info("send data back ----------------->")
	LOG.info("retVal: %s" % (retVal))
	conn.send_rsp(CMD["PLAYER_CREATE_PLAYER_REP"], playerid, rqstid, retVal) 

def get_recommand_player_info(conn, playerid, rqstid, pkt):
	LOG.info("conn: %s, playerid: %s, rqstid: %s, pkt: %s" % (conn, playerid,
														   rqstid, pkt))
	retVal = player.get_recommand_player_info()
	LOG.info("send data back ----------------->")
	LOG.info("retVal: %s" % (retVal))
	conn.send_rsp(CMD["PLAYER_GET_RECOMMAND_PLAYER_INFO_REP"], playerid, rqstid, retVal)

def check_player(conn, playerid, rqstid, pkt):
	LOG.info("conn: %s, playerid: %s, rqstid: %s, pkt: %s" % (conn, playerid,
														   rqstid, pkt))
	retVal = player.check_player(pkt["zone"], pkt["passport_id"], pkt["sitekey"], pkt["sign"])
	LOG.info("send data back ----------------->")
	LOG.info("retVal: %s" % (retVal))
	conn.send_rsp(CMD["PLAYER_CHECK_PLAYER_REP"], playerid, rqstid, retVal)

def reg_cmd(conn):
	conn.hook_command(CMD["PLAYER_CREATE_PLAYER_ACK"], create_player)
	conn.hook_command(CMD["PLAYER_GET_RECOMMAND_PLAYER_INFO_ACK"], get_recommand_player_info)
	conn.hook_command(CMD["PLAYER_CHECK_PLAYER_ACK"], check_player) 

if __name__ == '__main__':
	LOG.info("config.adds: %s, config.CHANNEL_ID: %s, config.CHANNEL_NAME: %s"
		  % (config.adds, config.CHANNEL_ID, config.CHANNEL_NAME))
	conn = CConn2Center(config.adds, config.CHANNEL_ID, config.CHANNEL_NAME)
	reg_cmd(conn)
	conn.start()
