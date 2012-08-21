#!/usr/bin/evn python
# coding=utf-8
from twisted.internet import protocol, reactor, defer
import struct
import inspect
import time
from amfast.decoder import Decoder
from amfast.encoder import Encoder

def encodeAmf3Data(data):
	encoder = Encoder(amf3=True)
	amf3_data = encoder.encode(data)
	return amf3_data

def decoderAmf3Data(amf3_data):
	decoder = Decoder(amf3=True)
	data = decoder.decode(amf3_data)
	return data


HOST = 'localhost'
PORT = 8888

MSG_TYPE = 1
CHANNEL_ID = 2
CMD = 0x00001
DATA = {'a':1, 'b':2}

AMF3_DATA = encodeAmf3Data(DATA)

class rpgClientProtocol(protocol.Protocol):
	def __init__(self):
		self.__buffer		   = ''
		self._msg_type		   = 0
		self._channel_id	   = 0
		self._command_id	   = 0
		self._amf3_data = ''

	def getData(self, msg_type = MSG_TYPE, channel_id = CHANNEL_ID, command_id
			 = CMD, amf3_data = AMF3_DATA):
		self._msg_type		= msg_type
		self._channel_id	= channel_id
		self._command_id	= command_id
		self._amf3_data		= amf3_data

	def parseHead(self, msg):
		print 'msg: >>>>>>>>>>>>>>>>>>', repr(msg)
		(msg_type, channel_id, command_id, data_length) = struct.unpack('BBHI',msg)
		return msg_type, channel_id, command_id, data_length

	def parseBody(self, msg):
		data = decoderAmf3Data(msg)
		print data

	def getDataLength(self, msg):
		(msg_type, channel_id, command_id, data_length) = self.parseHead(msg)
		return data_length

	def connectionMade(self):
		self.sendData()

	def get_amf3_fmt(self):
		fmt = '!I%ss' % (len(self._amf3_data))
		return fmt
 
	def packData(self):
		self.getData()
		fmt = self.get_amf3_fmt()
		data = struct.pack('BBH', self._msg_type, self._channel_id,\
					 self._command_id) + struct.pack(fmt, len(self._amf3_data),self._amf3_data)
		print self._msg_type
		print self._channel_id
		print self._command_id
		print self._amf3_data
		print 'data send to server: ', repr(data)
		print 'len data send to server: ', len(data)
		return data
		
	def sendData(self):
		data = self.packData()
		self.transport.write(data)

	def parseData(self):
		msg_head = self.__buffer[0:8]
		print 'msg_head: ***************** ', repr(msg_head)
		#获取消息头 
		data_length = self.getDataLength(msg_head)
		#获取消息体长度
		print data_length
		print len(self.__buffer[8:])
		while len(self.__buffer) >= 8:
			msg_head = self.__buffer[0:8]
			data_length = self.getDataLength(msg_head)
			if (data_length <= len(self.__buffer[8:])):
				self.__buffer = self.__buffer[8:]
				body = self.__buffer[0:data_length]
				print 'body: ', repr(body)
				self.parseBody(body)
				self.__buffer = self.__buffer[data_length:]
				print 'parse successfully'
				# self.transport.write('received')
			else:
				print 'Pack length not enough, wait for next receive'
				# self.transport.write('sendmore')
				break
		print 'Buffer length:', len(self.__buffer)	
	
	def dataReceived(self, data):
		self.__buffer = self.__buffer + data
		self.factory.deferred.callback(self)

class rpgClientFactory(protocol.ClientFactory):
	protocol = rpgClientProtocol
	
	def __init__(self):
		self.deferred = defer.Deferred()
		
	def clientConnectionLost(self, connector, reason):
		self.deferred.errback(reason)
		
	def clientConnectionFailed(self, connector, reason):
		self.deferred.errback(reason)


def conn2Server(host, port):
	rpgFactory = rpgClientFactory()
	reactor.connectTCP(host, port, rpgFactory)
	return rpgFactory.deferred
	
def handleReceivedData(s):
	s.parseData()
	
def handleFailure(failure, host, port):
	print "Error connecting to host: %s :port %i, due to: %s" % (host, port, failure.getErrorMessage())
	reactor.stop()
	
if __name__ == '__main__':
	conn = conn2Server(HOST, PORT)
	conn.addCallback(handleReceivedData)
	conn.addErrback(handleFailure, HOST, PORT)
	reactor.run()
