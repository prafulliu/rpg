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
import db.player.player as player
import config.CMD as CMD
CMD = CMD.cmd
import network.Conn2Center as Conn2Center
Conn2Center = Conn2Center.Conn2Center

# adds = ('localhost', 8888)
# KEY = 'a780xx'
CHANNEL_ID = 0
CHANNEL_NAME = 'player'

def creat_player(conn, playerid, rqstid, pkt):
    retVal = player.creat_player(pkt["name"], pkt["camp"], pkt["occupation"],
                                 pkt["zone"], pkt["passport_id"])
    conn.send_rsp(CMD["PLAYEROUT_CREATEPLAYER_REP"], playerid, rqstid, retVal) 

def get_recommand_player_info(conn, playerid, rqstid, pkt):
    retVal = player.get_recommand_player_info()
    conn.send_rsp(CMD["PLAYEROUT_GETRECOMMANDPLAYERINFO_REP"], playerid,
                  rqstid, retVal)

def check_player(conn, playerid, rqstid, pkt):
    retVal = player.check_player(pkt["zone"], pkt["passport_id"], pkt["sitekey"], pkt["sign"])
    conn.send_rsp(CMD["PLAYEROUT_CHECKPLAYER_REP"], playerid, rqstid, retVal)

def reg_cmd(conn):
    conn.hook_command(CMD["PLAYEROUT_CREATEPLAYER_ACK"], creat_player)
    conn.hook_command(CMD["PLAYEROUT_GETRECOMMANDPLAYERINFO_ACK"], get_recommand_player_info)
    conn.hook_command(CMD["PLAYEROUT_CHECKPLAYER_ACK"], check_player) 

if __name__ == '__main__':
    conn = Conn2Center(config.adds, CHANNEL_ID, CHANNEL_NAME)
    reg_cmd(conn)
    conn.start()
