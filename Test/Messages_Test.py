#!/usr/bin/python2
import unittest
import numpy as np
from datetime import datetime
from CommunicationLibrary.Messages.AbstractMessages import *
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *
from CommunicationLibrary.Messages.SharedObjects import *


class TestMessages(unittest.TestCase):

    def testMessageEncodingDecoding(self):
        msg = Message()
        self.assertIsNot(msg, None)
        msg.initConversationIdMessageId(1,2)
        self.assertEqual(msg.conversationId, 1)
        self.assertEqual(msg.messageId, 2)
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertEqual(decodedMsg.conversationId, 1)
        self.assertEqual(decodedMsg.messageId, 2)

    def testReplyMessageEncodingDecoding(self):
        msg = Reply(True)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)
        self.assertEqual(decodedMsg.success, True)


    # def testReplyEncodingDecoding(self):
    #     msg = Reply(True)
    #     processedMsg = msg.encode().decode()
    #     self.assertEqual(msg, processedMsg)
    #     self.assertEqual(msg.success, True)
    #
    # def testRequestEncodingDecoding(self):
    #     msg = Request()
    #     processedMsg = msg.encode().decode()
    #     self.assertEqual(msg, processedMsg)
    #
    # def testAckReplyEncodingDecoding(self):
    #     msg = AckReply(True)
    #     processedMsg = msg.encode().decode()
    #     self.assertEqual(msg, processedMsg)
    #     self.assertEqual(msg.success, True)
    #
    # def testAliveReplyEncodingDecoding(self):
    #     msg = AliveReply(True)
    #     processedMsg = msg.encode().decode()
    #     self.assertEqual(msg, processedMsg)
    #     self.assertEqual(msg.success, True)
    #
    # def testLoginReplyEncodingDecoding(self):
    #     dateTime = datetime.now()
    #     process = Process(1, 'Server', '127.0.0.2:3000', 'Main Server', 'idle', dateTime)
    #     msg = LoginReply(True, process)
    #     processedMsg = msg.encode().decode()
    #     self.assertEqual(msg, processedMsg)
    #     process = processedMsg.process
    #     self.assertEqual(processedMsg.success, True)
    #     self.assertEqual(process.processId, 1)
    #     self.assertEqual(process.type, 'Server')
    #     self.assertEqual(process.endPoint, '127.0.0.2:3000')
    #     self.assertEqual(process.label, 'Main Server')
    #     self.assertEqual(process.status, 'idle')
    #     self.assertEqual(process.aliveTimeStamp, dateTime)
    #
    # def testMotionDetectedReplyEncodingDecoding(self):
    #     msg = MotionDetectedReply(True)
    #     processedMsg = msg.encode().decode()
    #     self.assertEqual(msg, processedMsg)
    #     self.assertEqual(msg.success, True)
    #
    # def testRawQueryReplyEncodingDecoding(self):
    #     picture = np.array([[0, 255], [255, 0]], np.uint8)
    #     timeStamp = datetime.now()
    #     data = PictureInfo(picture, timeStamp, 1, 2)
    #     msg = RawQueryReply(True, data)
    #     processedMsg = msg.encode().decode()
    #     self.assertEqual(msg, processedMsg)
    #     self.assertEqual(msg.success, True)
    #     data = processedMsg.data
    #     self.assertEqual(data.picture, picture)
    #     self.assertEqual(data.timeStamp, timeStamp)
    #     self.assertEqual(data.cameraId, 1)
    #     self.assertEqual(data.clusterId, 2)
    #
    # def testRegisterReplyEncodingDecoding(self):
    #     dateTime = datetime.now()
    #     process = Process(2, 'Server', '127.0.0.3:3020', 'Statistics Server', 'busy', dateTime)
    #     msg = RegisterReply(True, process)
    #     processedMsg = msg.encode().decode()
    #     self.assertEqual(msg, processedMsg)
    #     process = processedMsg.process
    #     self.assertEqual(processedMsg.success, True)
    #     self.assertEqual(process.processId, 2)
    #     self.assertEqual(process.type, 'Server')
    #     self.assertEqual(process.endPoint, '127.0.0.3:3020')
    #     self.assertEqual(process.label, 'Statistics Server')
    #     self.assertEqual(process.status, 'busy')
    #     self.assertEqual(process.aliveTimeStamp, dateTime)

if __name__ == '__main__':
    unittest.main()
