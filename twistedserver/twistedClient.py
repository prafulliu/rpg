#!/usr/bin/evn python
# coding=utf-8
from twisted.internet import protocol, reactor, defer
import struct
import inspect
import time

HOST = 'localhost'
PORT = 10000



class rpgClientProtocol(protocol.Protocol):
	def __init__(self):
		self.__buffer = ''

	def parseHead(self, msg):
		print 'msg: >>>>>>>>>>>>>>>>>>', repr(msg)
		(msg_type, channel_id, command_id, data_length) = struct.unpack('BBHI',msg)
		return msg_type, channel_id, command_id, data_length

	def parseBody(self, msg):
		pass

	def getDataLength(self, msg):
		(msg_type, channel_id, command_id, data_length) = self.parseHead(msg)
		return data_length

	def connectionMade(self):
		self.transport.write('sendmore')

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
			print 'data_length:', data_length
			print 'pack left length: ', len(self.__buffer[8:])
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
