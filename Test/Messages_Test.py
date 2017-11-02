#!/usr/bin/python2
import unittest
import numpy as np
from datetime import datetime, date
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

    ######### Request Messages #########
    def testAliveRequestEncodingDecoding(self):
        msg = AliveRequest()
        self.assertIsNot(msg, None)
        msg.initConversationIdMessageId(1,2)
        self.assertEqual(msg.conversationId, 1)
        self.assertEqual(msg.messageId, 2)
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, AliveRequest))
        self.assertEqual(decodedMsg.conversationId, 1)
        self.assertEqual(decodedMsg.messageId, 2)

    def testCalcStatisticsRequestEncodingDecoding(self):
        timePeriod = DateRange(date(2017,10,31),date(2017,9,1))
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        data = [
            PictureInfo(picture, timeStamp, 4, 5)
        ]

        msg = CalcStatisticsRequest(timePeriod, 'Daily', data)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.timePeriod, timePeriod)
        self.assertEqual(msg.statsType, 'Daily')

        self.assertIsNot(msg.data, None)
        self.assertTrue(np.array_equal(msg.data[0].picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.data[0].timeStamp, timeStamp)
        self.assertEqual(msg.data[0].cameraId, 4)
        self.assertEqual(msg.data[0].clusterId, 5)

        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, CalcStatisticsRequest))

        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)

        self.assertEqual(decodedMsg.timePeriod.startDate.year, timePeriod.startDate.year)
        self.assertEqual(decodedMsg.timePeriod.startDate.month, timePeriod.startDate.month)
        self.assertEqual(decodedMsg.timePeriod.startDate.day, timePeriod.startDate.day)
        self.assertEqual(decodedMsg.timePeriod.endDate.year, timePeriod.endDate.year)
        self.assertEqual(decodedMsg.timePeriod.endDate.month, timePeriod.endDate.month)
        self.assertEqual(decodedMsg.timePeriod.endDate.day, timePeriod.endDate.day)
        self.assertEqual(decodedMsg.statsType, 'Daily')

        self.assertIsNot(decodedMsg.data, None)
        self.assertTrue(np.array_equal(decodedMsg.data[0].picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(decodedMsg.data[0].timeStamp, timeStamp)

        self.assertEqual(decodedMsg.data[0].cameraId, 4)
        self.assertEqual(decodedMsg.data[0].clusterId, 5)

    def testCameraLoginRequestEncodingDecoding(self):
        msg = CameraLoginRequest('CameraProcess','label','camMac','homeCam',15,'password123')
        self.assertIsNot(msg, None)
        self.assertEqual(msg.processType, 'CameraProcess')
        self.assertEqual(msg.processLabel, 'label')
        self.assertEqual(msg.identity, 'camMac')
        self.assertEqual(msg.name, 'homeCam')
        self.assertEqual(msg.clusterId, 15)
        self.assertEqual(msg.clusterIdPassword, 'password123')

        msg.initConversationIdMessageId(1,2)
        self.assertEqual(msg.conversationId, 1)
        self.assertEqual(msg.messageId, 2)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, LoginRequest))
        self.assertTrue(isinstance(decodedMsg, CameraLoginRequest))

        self.assertEqual(decodedMsg.conversationId, 1)
        self.assertEqual(decodedMsg.messageId, 2)

        self.assertEqual(decodedMsg.processType, 'CameraProcess')
        self.assertEqual(decodedMsg.processLabel, 'label')
        self.assertEqual(decodedMsg.identity, 'camMac')
        self.assertEqual(decodedMsg.name, 'homeCam')
        self.assertEqual(decodedMsg.clusterId, 15)
        self.assertEqual(decodedMsg.clusterIdPassword, 'password123')

    def testClientLoginRequestEncodingDecoding(self):
        msg = ClientLoginRequest('ClientProcess','label','clientId','shemarama','password123')
        self.assertIsNot(msg, None)
        self.assertEqual(msg.processType, 'ClientProcess')
        self.assertEqual(msg.processLabel, 'label')
        self.assertEqual(msg.identity, 'clientId')
        self.assertEqual(msg.username, 'shemarama')
        self.assertEqual(msg.password, 'password123')

        msg.initConversationIdMessageId(1,2)
        self.assertEqual(msg.conversationId, 1)
        self.assertEqual(msg.messageId, 2)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, LoginRequest))
        self.assertTrue(isinstance(decodedMsg, ClientLoginRequest))

        self.assertEqual(decodedMsg.conversationId, 1)
        self.assertEqual(decodedMsg.messageId, 2)

        self.assertEqual(decodedMsg.processType, 'ClientProcess')
        self.assertEqual(decodedMsg.processLabel, 'label')
        self.assertEqual(decodedMsg.identity, 'clientId')
        self.assertEqual(decodedMsg.username, 'shemarama')
        self.assertEqual(decodedMsg.password, 'password123')

    def testLoginRequestEncodingDecoding(self):
        msg = LoginRequest('StatisticsServer','label','someId')
        self.assertIsNot(msg, None)
        self.assertEqual(msg.processType, 'StatisticsServer')
        self.assertEqual(msg.processLabel, 'label')
        self.assertEqual(msg.identity, 'someId')

        msg.initConversationIdMessageId(1,2)
        self.assertEqual(msg.conversationId, 1)
        self.assertEqual(msg.messageId, 2)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, LoginRequest))

        self.assertEqual(decodedMsg.conversationId, 1)
        self.assertEqual(decodedMsg.messageId, 2)

        self.assertEqual(decodedMsg.processType, 'StatisticsServer')
        self.assertEqual(decodedMsg.processLabel, 'label')
        self.assertEqual(decodedMsg.identity, 'someId')

    def testRawQueryRequestEncodingDecoding(self):
        timePeriod = DateRange(date(2017, 5, 25), date(2017, 6, 30))
        cameras = ['1', '126', '6']
        msg = RawQueryRequest(timePeriod, cameras)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.timePeriod, timePeriod)

        self.assertIsNot(msg.cameras, None)
        self.assertEqual(msg.cameras[0], '1')
        self.assertEqual(msg.cameras[1], '126')
        self.assertEqual(msg.cameras[2], '6')

        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, RawQueryRequest))

        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)

        self.assertEqual(decodedMsg.timePeriod.startDate.year, timePeriod.startDate.year)
        self.assertEqual(decodedMsg.timePeriod.startDate.month, timePeriod.startDate.month)
        self.assertEqual(decodedMsg.timePeriod.startDate.day, timePeriod.startDate.day)
        self.assertEqual(decodedMsg.timePeriod.endDate.year, timePeriod.endDate.year)
        self.assertEqual(decodedMsg.timePeriod.endDate.month, timePeriod.endDate.month)
        self.assertEqual(decodedMsg.timePeriod.endDate.day, timePeriod.endDate.day)

        self.assertIsNot(decodedMsg.cameras, None)
        self.assertEqual(decodedMsg.cameras[0], '1')
        self.assertEqual(decodedMsg.cameras[1], '126')
        self.assertEqual(decodedMsg.cameras[2], '6')

    def testRegisterRequestEncodingDecoding(self):
        msg = RegisterRequest('someId')
        self.assertIsNot(msg, None)
        self.assertEqual(msg.identity, 'someId')

        msg.initConversationIdMessageId(1,2)
        self.assertEqual(msg.conversationId, 1)
        self.assertEqual(msg.messageId, 2)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, RegisterRequest))

        self.assertEqual(decodedMsg.conversationId, 1)
        self.assertEqual(decodedMsg.messageId, 2)
        self.assertEqual(decodedMsg.identity, 'someId')

    def testSaveMotionRequestEncodingDecoding(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        pictureInfo = PictureInfo(picture, timeStamp, 1, 2)
        msg = SaveMotionRequest(pictureInfo)
        self.assertIsNot(msg, None)

        self.assertIsNot(msg.pictureInfo, None)
        self.assertTrue(np.array_equal(msg.pictureInfo.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.pictureInfo.timeStamp, timeStamp)
        self.assertEqual(msg.pictureInfo.cameraId, 1)
        self.assertEqual(msg.pictureInfo.clusterId, 2)

        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, SaveMotionRequest))

        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)

        self.assertIsNot(decodedMsg.pictureInfo, None)
        self.assertTrue(np.array_equal(decodedMsg.pictureInfo.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(decodedMsg.pictureInfo.timeStamp, timeStamp)
        self.assertEqual(decodedMsg.pictureInfo.cameraId, 1)
        self.assertEqual(decodedMsg.pictureInfo.clusterId, 2)

    def testServerListRequestEncodingDecoding(self):
        msg = ServerListRequest()
        self.assertIsNot(msg, None)
        msg.initConversationIdMessageId(1,2)
        self.assertEqual(msg.conversationId, 1)
        self.assertEqual(msg.messageId, 2)
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, ServerListRequest))
        self.assertEqual(decodedMsg.conversationId, 1)
        self.assertEqual(decodedMsg.messageId, 2)

    def testServerLoginRequestEncodingDecoding(self):
        msg = ServerLoginRequest('MainServer','label','someId')
        self.assertIsNot(msg, None)
        self.assertEqual(msg.processType, 'MainServer')
        self.assertEqual(msg.processLabel, 'label')
        self.assertEqual(msg.identity, 'someId')

        msg.initConversationIdMessageId(1,2)
        self.assertEqual(msg.conversationId, 1)
        self.assertEqual(msg.messageId, 2)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, LoginRequest))
        self.assertTrue(isinstance(decodedMsg, ServerLoginRequest))

        self.assertEqual(decodedMsg.conversationId, 1)
        self.assertEqual(decodedMsg.messageId, 2)

        self.assertEqual(decodedMsg.processType, 'MainServer')
        self.assertEqual(decodedMsg.processLabel, 'label')
        self.assertEqual(decodedMsg.identity, 'someId')

    def testStatisticsRequestEncodingDecoding(self):
        timePeriod = DateRange(date(2017,1,31),date(2017,9,1))
        cameras = ['25', '65', '69']
        msg = StatisticsRequest(timePeriod, 'Weekly', cameras)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.timePeriod, timePeriod)
        self.assertEqual(msg.statsType, 'Weekly')

        self.assertIsNot(msg.cameras, None)
        self.assertEqual(msg.cameras[0], '25')
        self.assertEqual(msg.cameras[1], '65')
        self.assertEqual(msg.cameras[2], '69')

        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, StatisticsRequest))

        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)

        self.assertEqual(decodedMsg.timePeriod.startDate.year, timePeriod.startDate.year)
        self.assertEqual(decodedMsg.timePeriod.startDate.month, timePeriod.startDate.month)
        self.assertEqual(decodedMsg.timePeriod.startDate.day, timePeriod.startDate.day)
        self.assertEqual(decodedMsg.timePeriod.endDate.year, timePeriod.endDate.year)
        self.assertEqual(decodedMsg.timePeriod.endDate.month, timePeriod.endDate.month)
        self.assertEqual(decodedMsg.timePeriod.endDate.day, timePeriod.endDate.day)
        self.assertEqual(decodedMsg.statsType, 'Weekly')

        self.assertIsNot(decodedMsg.cameras, None)
        self.assertEqual(decodedMsg.cameras[0], '25')
        self.assertEqual(decodedMsg.cameras[1], '65')
        self.assertEqual(decodedMsg.cameras[2], '69')

    def testSubscribeRequestEncodingDecoding(self):
        msg = SubscribeRequest(42)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.clusterId, 42)
        msg.initConversationIdMessageId(1,2)
        self.assertEqual(msg.conversationId, 1)
        self.assertEqual(msg.messageId, 2)
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, SubscribeRequest))
        self.assertEqual(decodedMsg.conversationId, 1)
        self.assertEqual(decodedMsg.messageId, 2)
        self.assertEqual(decodedMsg.clusterId, 42)

    def testSyncDataRequestEncodingDecoding(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        data =  [
            PictureInfo(picture, timeStamp, 1, 2)
        ]
        msg = SyncDataRequest(data)
        self.assertIsNot(msg, None)

        self.assertIsNot(msg.data, None)
        self.assertTrue(np.array_equal(msg.data[0].picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.data[0].timeStamp, timeStamp)
        self.assertEqual(msg.data[0].cameraId, 1)
        self.assertEqual(msg.data[0].clusterId, 2)

        msg.initConversationIdMessageId(2,3)
        self.assertEqual(msg.conversationId, 2)
        self.assertEqual(msg.messageId, 3)

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, SyncDataRequest))

        self.assertEqual(decodedMsg.conversationId, 2)
        self.assertEqual(decodedMsg.messageId, 3)

        self.assertIsNot(decodedMsg.data, None)
        self.assertTrue(np.array_equal(decodedMsg.data[0].picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(decodedMsg.data[0].timeStamp, timeStamp)
        self.assertEqual(decodedMsg.data[0].cameraId, 1)
        self.assertEqual(decodedMsg.data[0].clusterId, 2)

    ########## SharedObjects ############
    def testActivityReport(self):
        report = ActivityReport(5, 2)
        self.assertIsNot(report, None)
        self.assertEqual(report.weeklyMotionEvents, 5)
        self.assertEqual(report.dailyMotionEvents, 2)

    def testDateRange(self):
        timePeriod = DateRange(date(2017,10,31),date(2017,9,1))
        self.assertIsNot(timePeriod, None)
        self.assertEqual(timePeriod.startDate.year, 2017)
        self.assertEqual(timePeriod.startDate.month, 10)
        self.assertEqual(timePeriod.startDate.day, 31)
        self.assertEqual(timePeriod.endDate.year, 2017)
        self.assertEqual(timePeriod.endDate.month, 9)
        self.assertEqual(timePeriod.endDate.day, 1)

    def testMessageNumber(self):
        messageNumber = MessageNumber(2, 5)
        self.assertIsNot(messageNumber, None)
        self.assertEqual(messageNumber.processId, 2)
        self.assertEqual(messageNumber.seqNumber, 5)

    def testPictureInfo(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        data = PictureInfo(picture, timeStamp, 1, 2)

        self.assertIsNot(data, None)
        self.assertTrue(np.array_equal(data.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(data.timeStamp, timeStamp)
        self.assertEqual(data.cameraId, 1)
        self.assertEqual(data.clusterId, 2)

    def testProcessInfo(self):
        dateTime = datetime.now()
        process = ProcessInfo(1, 'ClientProcess', '127.0.0.3:3200', 'Info about Process', 'idle', dateTime)
        self.assertIsNot(process, None)
        self.assertEqual(process.processId, 1)
        self.assertEqual(process.processType, 'ClientProcess')
        self.assertEqual(process.endPoint, '127.0.0.3:3200')
        self.assertEqual(process.label, 'Info about Process')
        self.assertEqual(process.status, 'idle')
        self.assertEqual(process.aliveTimeStamp, dateTime)

    def testPublicEndPoint(self):
        endpoint = PublicEndPoint('127.0.0.3', '4000')
        self.assertIsNot(endpoint, None)
        self.assertEqual(endpoint.host, '127.0.0.3')
        self.assertEqual(endpoint.port, '4000')

if __name__ == '__main__':
    unittest.main()
