# -*- coding: utf-8 -*- 
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
import struct
import time

from amfast.decoder import Decoder
from amfast.encoder import Encoder

encoder = Encoder(amf3=True)
decoder = Decoder(amf3=True)

KEY = 'a780'
CHANNEL_ID = 0
CHANNEL_NAME = 'player'
fmt = '!II%ssI%ss' % (len(CHANNEL_NAME), len(KEY))



#MAX VALUE = 65025*65025
	   #4228250625
PLAYER_ID = 1000000000

#MAX VALUE	= 65025
#  'H' format requires 0 <= number <= 65535
MSG_CHANNEL = 55555

#CMD		= 0x00000001
CMD	 = 0x00000002
#CMD	 = 0x00000003 

data = {"zone":0, "passport_id":'2', "sitekey":0, "sign":0}
data = {}
#data = {"name":"james", "camp":2, "occupation":1, "passport_id":"lpf"}

AMF3_DATA = encoder.encode(data)

send_fmt = '!IHHI%ss' % (len(AMF3_DATA ))

def get_send_fmt(amf3_data):
	send_fmt = '!IHHI%ss' % (len(amf3_data))
	return send_fmt

class pythonServer(Protocol):
	def __init__(self):
		self.count = 0
		self._isReg = False
		self._buffer = ''

	def packData(self, amf3_data, PLAYER_ID, MSG_CHANNEL, CMD):
		send_fmt = get_send_fmt(amf3_data)
		data = struct.pack(send_fmt, PLAYER_ID, MSG_CHANNEL, CMD, len(amf3_data), amf3_data)
		return data
	
	def sendData(self, data): 
		print '...sending %s' % repr(data)
		self.transport.write(data)
	
	def connectionMade(self):
		print "Connected from", self.transport.client
		#self.sendData()
	
	def verify(self, verifyString):
		#[uint32 channel_id][string channel_name][string key]
		print 'len data: ', len(verifyString)
		print 'data: ', repr(verifyString)
		(channel_id, channel_name_len, channel_name, key_len, key) = struct.unpack(fmt, verifyString)
		print 'channel_id: ', channel_id
		print 'channel_name_len: ', channel_name_len
		print 'channel_name: ', channel_name
		print 'key_len: ', key_len
		print 'key: ', key
		print 'KEY: ', KEY
		if (key == KEY):
			"called true"
			result = True
		else:
			"called false"
			result = False
		print "result: ", result
		return result
	
	def dataReceived(self, data):
		print 'self._isReg: ', self._isReg
		if self._isReg:
			self._buffer = self._buffer + data
			print 'data: ', repr(data)
	 #[uint8_t flag][uint32_t targetLen][target_players][uint8_t ch='\0'][uint16_t msg_channel][uint16_t cmd][string amf3_data]
			if (len(self._buffer) > 5):
				(flag, targetLen) = struct.unpack("!BI", self._buffer[0:5])
				print 'flag: ', flag
				print 'targetLen: ', targetLen
				if flag == 0:
					if (len(self._buffer[5:])>= len(self._buffer[5:5+targetLen])):
						target_players = self._buffer[5:5+targetLen]
					#	(count,) = struct.unpack('!I', self._buffer[5:5+4])
						count = (targetLen-1)/4
						print 'count: ', count
						if(len(self._buffer[9:])>=len(self._buffer[5:5+count*4])):
							player_id_list=[]
							for i in xrange(count):
								print 'i: ', i
								(player_id,) =struct.unpack("!I",self._buffer[5+4*i:5+4*(i+1)]) 
								player_id_list.append(player_id)
								print 'player_id %s %s' % (i,player_id)
								print 'len 1: ', len(self._buffer[5+count*4:])
								print 'len 2: ', len(self._buffer[5+count*4:5+count*4+1+4+4]) 
								print repr(self._buffer[5+count*4:])
								print repr(self._buffer[5+count*4:5+count*4+1+4+4]) 
							if len(self._buffer[9+count*4:])>=len(self._buffer[5+count*4:5+count*4+1+4+4]):
								(seprator, cmd, amf3_data_len) = struct.unpack("!sII", self._buffer[5+count*4:5+count*4+1+4+4])
								print 'seprator: ', repr(seprator)
								print '--------------------------cmd: ', cmd
								print 'amf3_data_len: ', amf3_data_len
								print 'total len :', len(self._buffer)
								#print 'len :', 9+count*4+1+4+4+amf3_data_len
								#print 'len1 :', len(self._buffer[9+count*4+1+4+4:])
								#print 'len2 :',len(self._buffer[9+count*4+1+4+4:9+count*4+1+4+4+amf3_data_len]) 
								if len(self._buffer[5+count*4+1+4+4:])>=len(self._buffer[5+count*4+1+4+4:9+count*4+1+4+4+amf3_data_len]):
									amf3_data_fmt = '%ss' % (amf3_data_len)
									(amf3_data,) = struct.unpack(amf3_data_fmt, self._buffer[5+count*4+1+4+4:5+count*4+1+4+4+amf3_data_len])
									#print repr( amf3_data)
									data = decoder.decode(amf3_data)
									print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
									print 'message received: ', data
								
				elif flag == 2:
					pass
				
			"""
			if data == 'received':
				print 'successfully parse a message'
				reactor.stop()
				self.sendData()
			else:
				print 'send more data'
				self.sendData()
			"""
		else:
			"called ....................... isReg false"
			result = self.verify(data)
			print "xxxxxxxxxxxxxxxxxxx		   result: ", result
			if (result == True):
			#if self.verify(data):
				"verify...................... true"
				self._isReg = True
				#for i in xrange(10):
				amf3_data = self.packData(AMF3_DATA, PLAYER_ID, MSG_CHANNEL, CMD)
				print 'amf3_data: ', repr(amf3_data)
				self.sendData(amf3_data)
				#time.sleep(10)
				#amf3_data = self.packData(AMF3_DATA_2, PLAYER_ID, MSG_CHANNEL, CMD2)
				#self.sendData(amf3_data)
			else:
				"verify...................... false"
	
	def connectionLost(self, reason):
		print "Disconnected from", self.transport.client
	
if __name__ == "__main__":
	factory = Factory()
	factory.protocol = pythonServer
	reactor.listenTCP(8888, factory)
	#reactor.listenTCP(8889, factory)
	#reactor.listenTCP(8890, factory)
	reactor.run()
