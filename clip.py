"""
        print 'data: ********************* ', repr(data)
        msg_head = self._bufer[0:8]
        print 'msg_head: ***************** ', repr(msg_head)
        #获取消息头
        data_length = self.getDataLength(msg_head)
        #获取消息体长度
        print data_length
        print len(self._bufer[8:])
        while len(self._bufer) >= 8:
            msg_head = self._bufer[0:8]
            data_length = self.getDataLength(msg_head)
            print 'data_length:', data_length
            print 'pack left length: ', len(self._bufer[8:])
            if (data_length <= len(self._bufer[8:])):
                self._bufer = self._bufer[8:]
                body = self._bufer[0:data_length]
                print 'body: ', repr(body)
                self.parseBody(body)
                self._bufer = self._bufer[data_length:]
                self._sock.send('received')
            else:
                print 'Pack length not enough, wait for next receive'
                self._sock.send('sendmore')
                break

        print 'Buffer length:', len(self._bufer)
"""

