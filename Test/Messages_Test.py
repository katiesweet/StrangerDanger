#!/usr/bin/python2
import unittest
import numpy as np
from datetime import datetime
from CommunicationLibrary.Messages.AbstractMessages import *
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *
from CommunicationLibrary.Messages.SharedObjects import *


class TestMessages(unittest.TestCase):

    ########## Abstract Messages #############
    def testMessageEncodingDecoding(self):
        msg = Message()
        self.assertIsNot(msg, None)
        msg.initConversationIdMessageId(1,2)
        self.assertEqual(msg.conversationId, 1)
        self.assertEqual(msg.messageId, 2)
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
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
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)
        self.assertEqual(decodedMsg.success, True)

    def testRequestMessageEncodingDecoding(self):
        msg = Request()
        self.assertIsNot(msg, None)
        msg.initConversationIdMessageId(1,2)
        self.assertEqual(msg.conversationId, 1)
        self.assertEqual(msg.messageId, 2)
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertEqual(decodedMsg.conversationId, 1)
        self.assertEqual(decodedMsg.messageId, 2)

    ########## Reply Messages #############
    def testAckReplyEncodingDecoding(self):
        msg = AckReply(False)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, False)
        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, AckReply))
        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)
        self.assertEqual(decodedMsg.success, False)

    def testAliveReplyEncodingDecoding(self):
        msg = AliveReply(False)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, False)
        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, AliveReply))
        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)
        self.assertEqual(decodedMsg.success, False)

    def testLoginReplyEncodingDecoding(self):
        dateTime = datetime.now()
        process = ProcessInfo(1, 'MainServer', '127.0.0.2:3000', 'Info about Process', 'idle', dateTime)
        msg = LoginReply(True, process)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        self.assertIsNot(msg.process, None)
        self.assertEqual(msg.process.processId, 1)
        self.assertEqual(msg.process.processType, 'MainServer')
        self.assertEqual(msg.process.endPoint, '127.0.0.2:3000')
        self.assertEqual(msg.process.label, 'Info about Process')
        self.assertEqual(msg.process.status, 'idle')
        self.assertEqual(msg.process.aliveTimeStamp, dateTime)

        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, LoginReply))

        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)
        self.assertEqual(decodedMsg.success, True)

        self.assertIsNot(decodedMsg.process, None)
        self.assertEqual(decodedMsg.process.processId, 1)
        self.assertEqual(decodedMsg.process.processType, 'MainServer')
        self.assertEqual(decodedMsg.process.endPoint, '127.0.0.2:3000')
        self.assertEqual(decodedMsg.process.label, 'Info about Process')
        self.assertEqual(decodedMsg.process.status, 'idle')
        self.assertEqual(decodedMsg.process.aliveTimeStamp, dateTime)

    def testMotionDetectedReplyEncodingDecoding(self):
        msg = MotionDetectedReply(True)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, MotionDetectedReply))
        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)
        self.assertEqual(decodedMsg.success, True)

    def testRawQueryReplyEncodingDecoding(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        data = PictureInfo(picture, timeStamp, 1, 2)
        msg = RawQueryReply(True, data)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)

        self.assertIsNot(msg.data, None)
        self.assertTrue(np.array_equal(msg.data.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.data.timeStamp, timeStamp)
        self.assertEqual(msg.data.cameraId, 1)
        self.assertEqual(msg.data.clusterId, 2)

        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, RawQueryReply))

        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)
        self.assertEqual(decodedMsg.success, True)

        self.assertIsNot(decodedMsg.data, None)
        self.assertTrue(np.array_equal(decodedMsg.data.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(decodedMsg.data.timeStamp, timeStamp)
        self.assertEqual(decodedMsg.data.cameraId, 1)
        self.assertEqual(decodedMsg.data.clusterId, 2)

    def testRegisterReplyEncodingDecoding(self):
        dateTime = datetime.now()
        process = ProcessInfo(1, 'ClientProcess', '127.0.0.3:3200', 'Info about Process', 'idle', dateTime)
        msg = RegisterReply(True, process)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        self.assertIsNot(msg.process, None)
        self.assertEqual(msg.process.processId, 1)
        self.assertEqual(msg.process.processType, 'ClientProcess')
        self.assertEqual(msg.process.endPoint, '127.0.0.3:3200')
        self.assertEqual(msg.process.label, 'Info about Process')
        self.assertEqual(msg.process.status, 'idle')
        self.assertEqual(msg.process.aliveTimeStamp, dateTime)

        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, RegisterReply))

        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)
        self.assertEqual(decodedMsg.success, True)

        self.assertIsNot(decodedMsg.process, None)
        self.assertEqual(decodedMsg.process.processId, 1)
        self.assertEqual(decodedMsg.process.processType, 'ClientProcess')
        self.assertEqual(decodedMsg.process.endPoint, '127.0.0.3:3200')
        self.assertEqual(decodedMsg.process.label, 'Info about Process')
        self.assertEqual(decodedMsg.process.status, 'idle')
        self.assertEqual(decodedMsg.process.aliveTimeStamp, dateTime)

    def testServerListReplyEncodingDecoding(self):
        servers = [
            PublicEndPoint('127.0.0.3', '4000'),
            PublicEndPoint('127.0.0.5', '4060'),
        ]
        msg = ServerListReply(True, servers)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)

        self.assertIsNot(msg.servers, None)
        self.assertEqual(msg.servers[0].host, '127.0.0.3')
        self.assertEqual(msg.servers[0].port, '4000')
        self.assertEqual(msg.servers[1].host, '127.0.0.5')
        self.assertEqual(msg.servers[1].port, '4060')

        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, ServerListReply))

        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)
        self.assertEqual(decodedMsg.success, True)

        self.assertIsNot(decodedMsg.servers, None)
        self.assertEqual(decodedMsg.servers[0].host, '127.0.0.3')
        self.assertEqual(decodedMsg.servers[0].port, '4000')
        self.assertEqual(decodedMsg.servers[1].host, '127.0.0.5')
        self.assertEqual(decodedMsg.servers[1].port, '4060')

    def testStatisticsReplyEncodingDecoding(self):
        report = ActivityReport(5, 2)
        msg = StatisticsReply(True, report)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)

        self.assertIsNot(msg.report, None)
        self.assertEqual(msg.report.weeklyMotionEvents, 5)
        self.assertEqual(msg.report.dailyMotionEvents, 2)

        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, StatisticsReply))

        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)
        self.assertEqual(decodedMsg.success, True)

        self.assertIsNot(decodedMsg.report, None)
        self.assertEqual(decodedMsg.report.weeklyMotionEvents, 5)
        self.assertEqual(decodedMsg.report.dailyMotionEvents, 2)

    def testSyncDataReplyEncodingDecoding(self):
        msg = SyncDataReply(True)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, SyncDataReply))
        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)
        self.assertEqual(decodedMsg.success, True)


if __name__ == '__main__':
    unittest.main()
