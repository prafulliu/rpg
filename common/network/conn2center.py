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
import util.pattern as pattern
import util.check as check
from log.log import LOG, TYPE

class CConn2Center(CCallback):
	def __init__(self, adds, channel_id, channel_name):
		CCallback.__init__(self)
		self._bufer = ''
		self._sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self._channel_id = channel_id
		self._channel_name = channel_name
		self._rqstid = {}

		self._sock.connect(adds)
		self.verify()

	#	try:
	#		self._sock.connect(adds)
	#		self.verify()
	#	except:
	#		LOG.info("connected failed")
	#		sys.exit(0)

	def verify(self):
		# [uint32 channel_id][string channel_name][string key]
		LOG.info("channel_id: %s, channel_name_len: %s, channel_name: %s, config.KEY:\
			%s" % (self._channel_id, len(self._channel_name), self._channel_name, config.KEY))
		fmt = '!II%ssI%ss' % (len(self._channel_name), len(config.KEY))
		veryfy_string = struct.pack(fmt, self._channel_id,\
			len(self._channel_name), self._channel_name, len(config.KEY), config.KEY)
		LOG.info('veryfyString: %s' % (repr(veryfy_string)))
		self._sock.send(veryfy_string)

	def get_sock(self):
		return self._sock

	def parse_head(self, msg):
		(msg_type, channel_id, command_id, data_length) = struct.unpack('BBHI',msg)
		return msg_type, channel_id, command_id, data_length

	def get_data_length(self, msg):
		(msg_type, channel_id, command_id, data_length) = self.parse_head(msg)
		return data_length

	def get_amf3_fmt(self, amf3_data):
		fmt = '!I%ss' % (len(amf3_data))
		return fmt
	
	def forward_msg(self, cmd, amf3_data, playerid, rqstid, flag, playerid_list=[]): 
		#[uint8_t flag][uint32_t targetLen][target_players][uint8_t ch='\0']\
		#[uint16_t msg_channel][uint16_t cmd][string amf3_data]
		msg_channel = self._rqstid[rqstid]['msg_channel']
		LOG.info("cmd: %s, amf3_data: %s, playerid: %s, rqstid: %s, flag: %s,\
			playerid_list: %s" % (pattern.to_hex(cmd), repr(amf3_data), playerid,\
			rqstid, flag, playerid_list))
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
			LOG.info('len(playerid_list): %s' % (len(playerid_list)))
		elif flag == 1:
			pass
		elif flag == 2:
			pass
		else:
			return
		
		LOG.debug('target_players: %s' % (repr(target_players)))
		targetLen += len(target_players)
		LOG.debug('targetLen: %s' % (targetLen))
		replyMsg = struct.pack("!BI", flag, targetLen)
		replyMsg += target_players
		replyMsg += struct.pack("!sI", seperator, cmd)
		replyMsg += struct.pack(self.get_amf3_fmt(amf3_data), len(amf3_data), amf3_data)
		LOG.info('len(amf3_data): %s' % (len(amf3_data)))
		LOG.info('amf3_data: %s' %
		(repr(struct.pack(self.get_amf3_fmt(amf3_data),len(amf3_data),
		amf3_data))))
		LOG.info('replyMsg: %s' % (repr(replyMsg)))
		data_count = self._sock.send(replyMsg)
		LOG.info('send %s data' % (data_count))

	def dataReceived(self, data):
		self._bufer = self._bufer + data
		#[uint32_t playerid][uint16_t msg_channel][uint16_t cmd][string amf3_data]

		LOG.info('len data: %s' % (len(data)))
		while(len(self._bufer) >= 12):
			(playerid, msg_channel, cmd, amf3_data_len) = struct.unpack("!IHHI", self._bufer[0:12])
			LOG.info("playerid: %s, msg_channel: %s, cmd: %s, amf3_data_len:\
				%s" % (playerid, msg_channel, pattern.to_hex(cmd), amf3_data_len,))
			amf3_data_fmt = '!%ss' % (amf3_data_len)
			if (len(self._bufer[12:]) >= amf3_data_len):
				rqstid = uuid.uuid1()
				self._rqstid[rqstid] = {'rqstid':rqstid,
										'msg_channel':msg_channel,
										'playerid':playerid,
										'cmd':cmd}
				(amf3_data,) = struct.unpack(amf3_data_fmt, self._bufer[12:12+amf3_data_len])
				LOG.info("amf3_data: %s" % repr(amf3_data))
				self._bufer = self._bufer[12+amf3_data_len:]
				decoder = Decoder(amf3=True)
				data = decoder.decode(amf3_data)
				LOG.info("data: %s" % (data))
				try:
					callback = self._callback[cmd]
					callback(self, playerid, rqstid, data) 
				except KeyError:
					LOG.ERROR("CMD error, The CMD: %s can not be handled" %
					(pattern.to_hex(cmd)))
					break

	def send_rsp(self, cmd, playerid, rqstid, pkt):
		encoder = Encoder(amf3=True)
		amf3_data = encoder.encode(pkt)
		self.forward_msg(cmd, amf3_data, playerid, rqstid, flag = 0)

	def start(self):
		LOG.info("conn2center start...")
		while 1:
			data, address = self.get_sock().recvfrom(8192)
			LOG.debug("data received: %s" % (repr(data)))
			if data:
				gevent.spawn(self.dataReceived, data)
				LOG.info("job's done")
			else:
				self.get_sock().close()
				break 

