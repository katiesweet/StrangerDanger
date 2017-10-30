#!/usr/bin/python2
import unittest
from datetime import datetime
from CommunicationLibrary.Messages.AbstractMessages import *
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *
from CommunicationLibrary.Messages.SharedObjects import *


class TestMessages(unittest.TestCase):

    def testMessageEncodingDecoding(self):
        msg = Message()
        processedMsg = msg.encode().decode()
        self.assertEqual(msg, processedMsg)

    def testReplyEncodingDecoding(self):
        msg = Reply(True)
        processedMsg = msg.encode().decode()
        self.assertEqual(msg, processedMsg)
        self.assertEqual(msg.success, True)

    def testRequestEncodingDecoding(self):
        msg = Request()
        processedMsg = msg.encode().decode()
        self.assertEqual(msg, processedMsg)

    def testAckReplyEncodingDecoding(self):
        msg = AckReply(True)
        processedMsg = msg.encode().decode()
        self.assertEqual(msg, processedMsg)
        self.assertEqual(msg.success, True)

    def testAliveReplyEncodingDecoding(self):
        msg = AliveReply(True)
        processedMsg = msg.encode().decode()
        self.assertEqual(msg, processedMsg)
        self.assertEqual(msg.success, True)

    def testLoginReplyEncodingDecoding(self):
        dateTime = datetime.now()
        process = Process(1, 'Server', '127.0.0.2:3000', 'Main Server', 'idle', dateTime)
        msg = LoginReply(True, process)
        processedMsg = msg.encode().decode()
        self.assertEqual(msg, processedMsg)
        process = processedMsg.process
        self.assertEqual(processedMsg.success, True)
        self.assertEqual(process.processId, 1)
        self.assertEqual(process.type, 'Server')
        self.assertEqual(process.endPoint, '127.0.0.2:3000')
        self.assertEqual(process.label, 'Main Server')
        self.assertEqual(process.status, 'idle')
        self.assertEqual(process.aliveTimeStamp, dateTime)


if __name__ == '__main__':
    unittest.main()
