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
import config.CMD as CMD
CMD = CMD.cmd

#adds = [('localhost', 8888), ('localhost', 8889), ('localhost', 8890)]
#adds_list = [('192.168.16.108', 18001)]
adds_list = [('localhost', 8888)]
KEY = 'a780xx'
CHANNEL_ID = 0
CHANNEL_NAME = 'player'

def creat_player(conn, playerid, pkt):
    retVal = player.creat_player(pkt["name"], pkt["camp"], pkt["occupation"],
                                 pkt["zone"], pkt["passport_id"])
    conn.send_rsp(CMD["PLAYEROUT_CREATEPLAYER_REP"], playerid, retVal) 

def get_recommand_player_info(conn, playerid, pkt):
    retVal = player.get_recommand_player_info()
    conn.send_rsp(CMD["PLAYEROUT_GETRECOMMANDPLAYERINFO_REP"], playerid, retVal)

def check_player(conn, playerid, pkt):
    retVal = player.check_player(pkt["zone"], pkt["passport_id"], pkt["sitekey"], pkt["sign"])
    conn.send_rsp(CMD["PLAYEROUT_CHECKPLAYER_REP"], playerid, retVal)

def reg_cmd():
    conn.hook_command(CMD["PLAYEROUT_CREATEPLAYER_ACK"], creat_player)
    conn.hook_command(CMD["PLAYEROUT_GETRECOMMANDPLAYERINFO_ACK"], get_recommand_player_info)
    conn.hook_command(CMD["PLAYEROUT_CHECKPLAYER_ACK"], check_player) 

if __name__ == '__main__':
    reg_cmd()
