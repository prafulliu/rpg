# -*- coding: utf-8 -*-
import struct
import gevent
import sys
import uuid

from gevent import socket
from gevent import event
from gevent.queue import Queue
from amfast.decoder import Decoder
from amfast.encoder import Encoder
import config.config as config
from callback import CCallback

#adds = [('localhost', 8888), ('localhost', 8889), ('localhost', 8890)]
#adds_list = [('192.168.16.108', 18001)]
#adds_list = [('localhost', 8888)]
# KEY = 'a780xx'
#CHANNEL_ID = 0
#CHANNEL_NAME = 'player'

class CConn2Center(CCallback):
    def __init__(self, adds, channel_id, channel_name):
        CCallback.__init__(self)
        self._bufer = ''
        self._sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._channel_id = channel_id
        self._channel_name = channel_name
        self._rqstid = {}

        try:
            print 'adds: ', adds
            self._sock.connect(adds)
            self.verify()
        except:
            print "connected failed"
            sys.exit(0)

    def verify(self):
        # [uint32 channel_id][string channel_name][string key]
		print 'channel_name: ', self._channel_name
		KEY = config.KEY
		print 'Key: ', KEY
		fmt = '!II%ssI%ss' % (len(self._channel_name), len(KEY))
		print len(self._channel_name), len(KEY)
		veryfy_string = struct.pack(fmt, self._channel_id, len(self._channel_name), self._channel_name, len(KEY), KEY)
		print 'veryfyString: ', repr(veryfy_string)
		print 'len data: ', len(veryfy_string)
		
		print "------------------------------------------------"
		print "------------------------------------------------"
		print "------------------------------------------------"
		(channel_id, channel_name_len, channel_name, key_len, key) = struct.unpack(fmt, veryfy_string)
		print 'channel_id: ', channel_id
		print 'channel_name_len: ', channel_name_len
		print 'channel_name: ', channel_name
		print 'key_len: ', key_len
		print 'key: ', key
		self._sock.send(veryfy_string)

    def get_sock(self):
        return self._sock

    def parse_head(self, msg):
        print 'msg: >>>>>>>>>>>>>>>>>>', repr(msg)
        (msg_type, channel_id, command_id, data_length) = struct.unpack('BBHI',msg)
        return msg_type, channel_id, command_id, data_length

    def get_data_length(self, msg):
        (msg_type, channel_id, command_id, data_length) = self.parse_head(msg)
        return data_length

    def get_amf3_fmt(self, amf3_data):
        fmt = '!I%ss' % (len(amf3_data))
        return fmt
    
    def forward_msg(self, amf3_data, playerid, rqstid, flag, playerid_list=[]): 
    #def forward_msg(self, flag, playerid_list=[], msg_channel, cmd, amf3_data): 
        #[uint8_t flag][uint32_t targetLen][target_players][uint8_t ch='\0'][uint16_t msg_channel][uint16_t cmd][string amf3_data]
        
        msg_channel = self._rqstid[rqstid]['msg_channel']
        cmd = self._rqstid[rqstid]['cmd']
        target_players = ''
        targetLen = 1
        seperator = '\0'
        playerid_list = []

        if flag == 0:
            _playerid = []
            _playerid.append(playerid)
            playerid_list = list(set(playerid_list).union(_playerid))
            for i in xrange(len(playerid_list)):
                target_players += struct.pack('!I', playerid_list[i])
            print 'len(playerid_list): ', len(playerid_list)
            target_players = struct.pack('!I', len(playerid_list)) + target_players
        elif flag == 1:
            pass
        elif flag == 2:
            pass 
        else:
            return

        print 'target_players: ', repr(target_players)
        targetLen += len(target_players)
        print 'targetLen: ', targetLen
        replyMsg = struct.pack("!BI", flag, targetLen)
        replyMsg += target_players 
        print 'type: ', type(seperator)
        replyMsg += struct.pack("!sHH", seperator, msg_channel, cmd)
        replyMsg += struct.pack(self.get_amf3_fmt(amf3_data), len(amf3_data), amf3_data)
        print 'amf3_data: ', repr(struct.pack(self.get_amf3_fmt(amf3_data),len(amf3_data), amf3_data))
        print 'replyMsg: ', repr(replyMsg)

        print '-------------------------------------------------'
        (flag, targetLen) = struct.unpack("!BI", replyMsg[0:5])
        print 'flag: ', flag 
        print 'targetLen: ', targetLen
        print 'send sock ==================>>>>>>>>>>', self._sock.send(replyMsg)

    def dataReceived(self, data):
        self._bufer = self._bufer + data
        #[uint32_t playerid][uint16_t msg_channel][uint16_t cmd][string amf3_data]

        print 'len data: ', len(data)
        while(len(self._bufer) >= 12):
            (playerid, msg_channel, cmd, amf3_data_len) = struct.unpack("!IHHI", self._bufer[0:12])
            print 'playerid: ', playerid
            print 'msg_channel: ', msg_channel
            print 'cmd: ', cmd
            print 'amf3_data_len: ', amf3_data_len
            print 'type: ', type(amf3_data_len)
            amf3_data_fmt = '!%ss' % (amf3_data_len)
            if (len(self._bufer[12:]) >= amf3_data_len):
                rqstid = uuid.uuid1()
                self._rqstid[rqstid] = {'rqstid':rqstid,
                                        'msg_channel':msg_channel,
                                        'playerid':playerid,
                                        'cmd':cmd}
                (amf3_data,) = struct.unpack(amf3_data_fmt, self._bufer[12:12+amf3_data_len])
                print '>>>>>>>>>>>>>>>>>>>>>>>>>>>> amf3_data: ', repr(amf3_data)
                self._bufer = self._bufer[12+amf3_data_len:]
                #self.forward_msg(amf3_data)
                decoder = Decoder(amf3=True)
                data = decoder.decode(amf3_data)
                print '>>>>>>>>>>>>>>>>>>>>>>>>>>> data: ', data
                callback = self._callback[cmd]
                callback(self, cmd, rqstid, data) 

    def send_rsp(self, cmd, playerid, rqstid, pkt):
        encoder = Encoder(amf3=True)
        amf3_data = encoder.encode(pkt)
        self.forward_msg(amf3_data, playerid, rqstid, flag = 0)

    def start(self):
        print 'called start'
        while 1:
            data, address = self.get_sock().recvfrom(8192)
            print 'data: ', repr(data)
            if data:
                gevent.spawn(self.dataReceived, data)
                print "job's done"
            else:
                self.get_sock().close()
                break 

