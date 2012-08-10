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
import config.config as config
import db.player as player
import config.cmd as cmd
cmd = cmd.cmd
import network.conn2center as conn2center
conn2center = conn2center.conn2center

# adds = ('localhost', 8888)
# KEY = 'a780xx'
CHANNEL_ID = 0
CHANNEL_NAME = 'player'

def creat_player(conn, playerid, rqstid, pkt):
    retVal = player.creat_player(pkt["name"], pkt["camp"], pkt["occupation"],
                                 pkt["zone"], pkt["passport_id"])
    conn.send_rsp(cmd["PLAYEROUT_CREATE_PLAYER_REP"], playerid, rqstid, retVal) 

def get_recommand_player_info(conn, playerid, rqstid, pkt):
    retVal = player.get_recommand_player_info()
    conn.send_rsp(cmd["PLAYEROUT_GET_RECOMMAND_PLAYER_INFO_REP"], playerid,
                  rqstid, retVal)

def check_player(conn, playerid, rqstid, pkt):
    retVal = player.check_player(pkt["zone"], pkt["passport_id"], pkt["sitekey"], pkt["sign"])
    conn.send_rsp(cmd["PLAYEROUT_CHECK_PLAYER_REP"], playerid, rqstid, retVal)

def reg_cmd(conn):
    print cmd
    conn.hook_command(cmd["PLAYEROUT_CREATE_PLAYER_ACK"], creat_player)
    conn.hook_command(cmd["PLAYEROUT_GET_RECOMMAND_PLAYER_INFO_ACK"], get_recommand_player_info)
    conn.hook_command(cmd["PLAYEROUT_CHECK_PLAYER_ACK"], check_player) 

if __name__ == '__main__':
    conn = conn2center(config.adds, CHANNEL_ID, CHANNEL_NAME)
    reg_cmd(conn)
    conn.start()
