
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
import struct
import time

class CParseMsg(Protocol):
    def __init__(self):
        self.count = 0

    def sendData(self):
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        data = '\x00\x00\x00\x00\x01\x00\x00\x00\x00'
        print repr(data)
        print 'No.', self.count
        self.count = self.count + 1
        print '...sending %s' % repr(data)
        self.transport.write(data)

    def connectionMade(self):
        print "Connected from", self.transport.client

    def dataReceived(self, data):
		print 'data', data
		if data == 'received':
			print 'successfully parse a message'
			self.sendData()
		else:
			print 'send more data'
			for i in xrange(10):
				time.sleep(2)
				self.sendData()
			# reactor.stop()

    def connectionLost(self, reason):
        print "Disconnected from", self.transport.client

if __name__ == "__main__":
    factory = Factory()
    factory.protocol = CParseMsg
    reactor.listenTCP(10000, factory)
    reactor.run()
