#!/usr/bin/python2
import unittest
import numpy as np
import math
from datetime import datetime, date
import sys
sys.path.append("../")

from CommunicationLibrary.Messages.AbstractMessages import *
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *
from CommunicationLibrary.Messages.SharedObjects import *
from CommunicationLibrary.Messages.SharedObjects.LocalProcessInfo import LocalProcessInfo
from CommunicationLibrary.Messages.SharedObjects.ProcessType import ProcessType
from CommunicationLibrary.Messages.SharedObjects.KeyManager import KeyManager
from CommunicationLibrary.Messages.SharedObjects.KeyGenerator import KeyGenerator
from RegistryServer.Registry import Registry

class TestMessages(unittest.TestCase):

    # runs once for all class tests
    @classmethod
    def setUpClass(cls):
        LocalProcessInfo.setProcessId(5)

    ########## Abstract Messages #############
    def testMessageEncodingDecoding(self):
        msg = Message()
        self.assertIsNot(msg, None)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

    def testMessageEncodingDecodingShouldFail(self):
        msg = Message()
        self.assertIsNot(msg, None)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testReplyMessageEncodingDecoding(self):
        msg = Reply(True)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.success, True)

    def testReplyMessageEncodingDecodingShouldFail(self):
        msg = Reply(True)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testRequestMessageEncodingDecoding(self):
        msg = Request()
        self.assertIsNot(msg, None)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

    def testRequestMessageEncodingDecodingShouldFail(self):
        msg = Request()
        self.assertIsNot(msg, None)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    ########## Reply Messages #############
    def testAckReplyEncodingDecoding(self):
        msg = AckReply(False)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, False)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, AckReply))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.success, False)

    def testAckReplyEncodingDecodingShouldFail(self):
        msg = AckReply(False)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, False)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testAliveReplyEncodingDecoding(self):
        msg = AliveReply(False)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, False)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, AliveReply))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.success, False)

    def testAliveReplyEncodingDecodingShouldFail(self):
        msg = AliveReply(False)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, False)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testMotionDetectedReplyEncodingDecoding(self):
        msg = MotionDetectedReply(True)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, MotionDetectedReply))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.success, True)

    def testMotionDetectedReplyEncodingDecodingShouldFail(self):
        msg = MotionDetectedReply(True)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testRawQueryReplyEncodingDecoding(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        data = PictureInfo(picture, timeStamp, 'Church of Sundberg')
        msg = RawQueryReply(True, data)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)

        self.assertIsNot(msg.data, None)
        self.assertTrue(np.array_equal(msg.data.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.data.timeStamp, timeStamp)
        self.assertEqual(msg.data.cameraName, 'Church of Sundberg')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, RawQueryReply))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.success, True)

        self.assertIsNot(decodedMsg.data, None)
        self.assertTrue(np.array_equal(decodedMsg.data.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(decodedMsg.data.timeStamp, timeStamp)
        self.assertEqual(decodedMsg.data.cameraName, 'Church of Sundberg')

    def testRawQueryReplyEncodingDecodingShouldFail(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        data = PictureInfo(picture, timeStamp, 'Church of Sundberg')
        msg = RawQueryReply(True, data)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)

        self.assertIsNot(msg.data, None)
        self.assertTrue(np.array_equal(msg.data.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.data.timeStamp, timeStamp)
        self.assertEqual(msg.data.cameraName, 'Church of Sundberg')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testRegisterReplyEncodingDecoding(self):
        key = KeyGenerator.generateKeyPair()
        public_key = key.publickey()
        nextProcessId = 6
        msg = RegisterReply(True, nextProcessId, public_key)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.processId, nextProcessId)
        self.assertEqual(msg.key, public_key)

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, RegisterReply))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.success, True)

        self.assertEqual(decodedMsg.processId, nextProcessId)
        self.assertEqual(decodedMsg.key, public_key)

    def testRegisterReplyEncodingDecodingShouldFail(self):
        key = KeyGenerator.generateKeyPair()
        public_key = key.publickey()
        nextProcessId = 6
        msg = RegisterReply(True, nextProcessId, public_key)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.processId, nextProcessId)
        self.assertEqual(msg.key, public_key)

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testSavePictureInfoReplyEncodingDecoding(self):
        msg = SavePictureInfoReply(True)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, SavePictureInfoReply))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.success, True)

    def testSavePictureInfoReplyEncodingDecodingShouldFail(self):
        msg = SavePictureInfoReply(True)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testSavePicturePartReplyEncodingDecoding(self):
        msg = SavePicturePartReply(True, 20)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        self.assertEqual(msg.partNumber, 20)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, SavePicturePartReply))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.success, True)
        self.assertEqual(decodedMsg.partNumber, 20)

    def testSavePicturePartReplyEncodingDecodingShouldFail(self):
        msg = SavePicturePartReply(True, 20)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        self.assertEqual(msg.partNumber, 20)
        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testServerListReplyEncodingDecoding(self):
        servers = [
            PublicEndPoint('127.0.0.3', '4000'),
            PublicEndPoint('127.0.0.5', '4060'),
        ]
        msg = ServerListReply(True, ProcessType.MainServer, servers)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)

        self.assertIsNot(msg.servers, None)
        self.assertEqual(msg.servers[0].host, '127.0.0.3')
        self.assertEqual(msg.servers[0].port, '4000')
        self.assertEqual(msg.servers[1].host, '127.0.0.5')
        self.assertEqual(msg.servers[1].port, '4060')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, ServerListReply))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.success, True)

        self.assertIsNot(decodedMsg.servers, None)
        self.assertEqual(decodedMsg.processType, ProcessType.MainServer)
        self.assertEqual(decodedMsg.servers[0].host, '127.0.0.3')
        self.assertEqual(decodedMsg.servers[0].port, '4000')
        self.assertEqual(decodedMsg.servers[1].host, '127.0.0.5')
        self.assertEqual(decodedMsg.servers[1].port, '4060')

    def testServerListReplyEncodingDecodingShouldFail(self):
        servers = [
            PublicEndPoint('127.0.0.3', '4000'),
            PublicEndPoint('127.0.0.5', '4060'),
        ]
        msg = ServerListReply(True, ProcessType.MainServer, servers)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)

        self.assertIsNot(msg.servers, None)
        self.assertEqual(msg.servers[0].host, '127.0.0.3')
        self.assertEqual(msg.servers[0].port, '4000')
        self.assertEqual(msg.servers[1].host, '127.0.0.5')
        self.assertEqual(msg.servers[1].port, '4060')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testStatisticsReplyEncodingDecoding(self):
        report = ActivityReport(5, 2)
        msg = StatisticsReply(True, report)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)

        self.assertIsNot(msg.report, None)
        self.assertEqual(msg.report.weeklyMotionEvents, 5)
        self.assertEqual(msg.report.dailyMotionEvents, 2)

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, StatisticsReply))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.success, True)

        self.assertIsNot(decodedMsg.report, None)
        self.assertEqual(decodedMsg.report.weeklyMotionEvents, 5)
        self.assertEqual(decodedMsg.report.dailyMotionEvents, 2)

    def testStatisticsReplyEncodingDecodingShouldFail(self):
        report = ActivityReport(5, 2)
        msg = StatisticsReply(True, report)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)

        self.assertIsNot(msg.report, None)
        self.assertEqual(msg.report.weeklyMotionEvents, 5)
        self.assertEqual(msg.report.dailyMotionEvents, 2)

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testSyncDataReplyEncodingDecoding(self):
        msg = SyncDataReply(True)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)

        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, SyncDataReply))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.success, True)

    def testSyncDataReplyEncodingDecodingShouldFail(self):
        msg = SyncDataReply(True)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)

        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testGetPictureReplyEncodingDecoding(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        msg = GetPictureReply(True, picture)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        self.assertTrue(np.array_equal(msg.picture, picture))

        msgId = msg.messageId
        convId= msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Reply))
        self.assertTrue(isinstance(decodedMsg, GetPictureReply))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.success, True)
        self.assertTrue(np.array_equal(decodedMsg.picture, picture))

    def testGetPictureReplyEncodingDecodingShouldFail(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        msg = GetPictureReply(True, picture)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.success, True)
        self.assertTrue(np.array_equal(msg.picture, picture))

        msgId = msg.messageId
        convId= msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    ######### Request Messages #########
    def testAliveRequestEncodingDecoding(self):
        msg = AliveRequest()
        self.assertIsNot(msg, None)

        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, AliveRequest))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

    def testAliveRequestEncodingDecodingShouldFail(self):
        msg = AliveRequest()
        self.assertIsNot(msg, None)

        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testCalcStatisticsRequestEncodingDecoding(self):
        timePeriod = DateRange(date(2017,10,31),date(2017,9,1))
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        data = [
            PictureInfo(picture, timeStamp, 'Bacon')
        ]
        clientEndpoint = ('192.168.0.4',3200)

        msg = CalcStatisticsRequest(timePeriod, 'Daily', data, clientEndpoint)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.timePeriod, timePeriod)
        self.assertEqual(msg.statsType, 'Daily')
        self.assertEqual(msg.clientEndpoint, clientEndpoint)

        self.assertIsNot(msg.data, None)
        self.assertTrue(np.array_equal(msg.data[0].picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.data[0].timeStamp, timeStamp)
        self.assertEqual(msg.data[0].cameraName, 'Bacon')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, CalcStatisticsRequest))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

        self.assertEqual(decodedMsg.timePeriod.startDate.year, timePeriod.startDate.year)
        self.assertEqual(decodedMsg.timePeriod.startDate.month, timePeriod.startDate.month)
        self.assertEqual(decodedMsg.timePeriod.startDate.day, timePeriod.startDate.day)
        self.assertEqual(decodedMsg.timePeriod.endDate.year, timePeriod.endDate.year)
        self.assertEqual(decodedMsg.timePeriod.endDate.month, timePeriod.endDate.month)
        self.assertEqual(decodedMsg.timePeriod.endDate.day, timePeriod.endDate.day)
        self.assertEqual(decodedMsg.statsType, 'Daily')
        self.assertEqual(decodedMsg.clientEndpoint, clientEndpoint)

        self.assertIsNot(decodedMsg.data, None)
        self.assertTrue(np.array_equal(decodedMsg.data[0].picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(decodedMsg.data[0].timeStamp, timeStamp)
        self.assertEqual(decodedMsg.data[0].cameraName, 'Bacon')

    def testCalcStatisticsRequestEncodingDecodingShouldFail(self):
        timePeriod = DateRange(date(2017,10,31),date(2017,9,1))
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        data = [
            PictureInfo(picture, timeStamp, 'Bacon')
        ]
        clientEndpoint = ('192.168.0.4',3200)

        msg = CalcStatisticsRequest(timePeriod, 'Daily', data, clientEndpoint)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.timePeriod, timePeriod)
        self.assertEqual(msg.statsType, 'Daily')
        self.assertEqual(msg.clientEndpoint, clientEndpoint)

        self.assertIsNot(msg.data, None)
        self.assertTrue(np.array_equal(msg.data[0].picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.data[0].timeStamp, timeStamp)
        self.assertEqual(msg.data[0].cameraName, 'Bacon')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testRawQueryRequestEncodingDecoding(self):
        isMostRecent = False
        timePeriod = DateRange(date(2017, 5, 25), date(2017, 6, 30))
        cameras = ['1', '126', '6']
        msg = RawQueryRequest(False, timePeriod, cameras)
        self.assertIsNot(msg, None)

        self.assertEqual(msg.mostRecent, isMostRecent)
        self.assertEqual(msg.timePeriod.startDate, timePeriod.startDate)
        self.assertEqual(msg.timePeriod.endDate, timePeriod.endDate)

        self.assertIsNot(msg.cameras, None)
        self.assertEqual(msg.cameras[0], '1')
        self.assertEqual(msg.cameras[1], '126')
        self.assertEqual(msg.cameras[2], '6')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, RawQueryRequest))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

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

    def testRawQueryRequestEncodingDecodingShouldFail(self):
        isMostRecent = False
        timePeriod = DateRange(date(2017, 5, 25), date(2017, 6, 30))
        cameras = ['1', '126', '6']
        msg = RawQueryRequest(False, timePeriod, cameras)
        self.assertIsNot(msg, None)

        self.assertEqual(msg.mostRecent, isMostRecent)
        self.assertEqual(msg.timePeriod.startDate, timePeriod.startDate)
        self.assertEqual(msg.timePeriod.endDate, timePeriod.endDate)

        self.assertIsNot(msg.cameras, None)
        self.assertEqual(msg.cameras[0], '1')
        self.assertEqual(msg.cameras[1], '126')
        self.assertEqual(msg.cameras[2], '6')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testRegisterRequestEncodingDecoding(self):
        key = KeyGenerator.generateKeyPair()
        public_key = key.publickey()
        msg = RegisterRequest(ProcessType.MainServer, public_key)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.processType, ProcessType.MainServer)
        self.assertEqual(msg.key, public_key)

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, RegisterRequest))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.processType, ProcessType.MainServer)
        self.assertEqual(decodedMsg.key, public_key)

    def testRegisterRequestEncodingDecodingShouldFail(self):
        key = KeyGenerator.generateKeyPair()
        public_key = key.publickey()
        msg = RegisterRequest(ProcessType.MainServer, public_key)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.processType, ProcessType.MainServer)
        self.assertEqual(msg.key, public_key)

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testSaveCombinedPictureRequest(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        pictureInfo = PictureInfo(picture, timeStamp, 'ShemCam')
        msg = SaveCombinedPictureRequest(pictureInfo)
        self.assertIsNot(msg, None)

        self.assertIsNot(msg.pictureInfo, None)
        self.assertTrue(np.array_equal(msg.pictureInfo.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.pictureInfo.timeStamp, timeStamp)
        self.assertEqual(msg.pictureInfo.cameraName, 'ShemCam')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, SaveCombinedPictureRequest))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

        self.assertIsNot(decodedMsg.pictureInfo, None)
        self.assertTrue(np.array_equal(decodedMsg.pictureInfo.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(decodedMsg.pictureInfo.timeStamp, timeStamp)
        self.assertEqual(decodedMsg.pictureInfo.cameraName, 'ShemCam')

    def testSaveCombinedPictureRequestShouldFail(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        pictureInfo = PictureInfo(picture, timeStamp, 'ShemCam')
        msg = SaveCombinedPictureRequest(pictureInfo)
        self.assertIsNot(msg, None)

        self.assertIsNot(msg.pictureInfo, None)
        self.assertTrue(np.array_equal(msg.pictureInfo.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.pictureInfo.timeStamp, timeStamp)
        self.assertEqual(msg.pictureInfo.cameraName, 'ShemCam')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testSaveMotionRequestEncodingDecoding(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        pictureInfo = PictureInfo(picture, timeStamp, 'Ya boi Shem')
        msg = SaveMotionRequest(pictureInfo)
        self.assertIsNot(msg, None)

        self.assertIsNot(msg.pictureInfo, None)
        self.assertTrue(np.array_equal(msg.pictureInfo.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.pictureInfo.timeStamp, timeStamp)
        self.assertEqual(msg.pictureInfo.cameraName, 'Ya boi Shem')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, SaveMotionRequest))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

        self.assertIsNot(decodedMsg.pictureInfo, None)
        self.assertTrue(np.array_equal(decodedMsg.pictureInfo.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(decodedMsg.pictureInfo.timeStamp, timeStamp)
        self.assertEqual(decodedMsg.pictureInfo.cameraName, 'Ya boi Shem')

    def testSaveMotionRequestEncodingDecodingShouldFail(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        pictureInfo = PictureInfo(picture, timeStamp, 'Ya boi Shem')
        msg = SaveMotionRequest(pictureInfo)
        self.assertIsNot(msg, None)

        self.assertIsNot(msg.pictureInfo, None)
        self.assertTrue(np.array_equal(msg.pictureInfo.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.pictureInfo.timeStamp, timeStamp)
        self.assertEqual(msg.pictureInfo.cameraName, 'Ya boi Shem')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testSavePictureInfoRequestEncodingDecoding(self):
        timeStamp = datetime.now()
        msg = SavePictureInfoRequest(30, timeStamp, 'KatieCam')
        self.assertIsNot(msg, None)

        self.assertEqual(msg.numberOfParts, 30)
        self.assertEqual(msg.timeStamp, timeStamp)
        self.assertEqual(msg.cameraName, 'KatieCam')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, SavePictureInfoRequest))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

        self.assertEqual(decodedMsg.numberOfParts, 30)
        self.assertEqual(decodedMsg.timeStamp, timeStamp)
        self.assertEqual(decodedMsg.cameraName, 'KatieCam')

    def testSavePictureInfoRequestEncodingDecodingShouldFail(self):
        timeStamp = datetime.now()
        msg = SavePictureInfoRequest(30, timeStamp, 'KatieCam')
        self.assertIsNot(msg, None)

        self.assertEqual(msg.numberOfParts, 30)
        self.assertEqual(msg.timeStamp, timeStamp)
        self.assertEqual(msg.cameraName, 'KatieCam')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testSavePicturePartRequestEncodingDecoding(self):
        part = np.array([[0, 255], [255, 0]], np.uint8)
        picturePart = PicturePart(part, 7, 'SarahCam')
        msg = SavePicturePartRequest(picturePart)
        self.assertIsNot(msg, None)

        self.assertIsNot(msg.picturePart, None)
        self.assertTrue(np.array_equal(msg.picturePart.picturePart, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.picturePart.partNumber, 7)
        self.assertEqual(msg.picturePart.cameraName, 'SarahCam')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, SavePicturePartRequest))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

        self.assertIsNot(decodedMsg.picturePart, None)
        self.assertTrue(np.array_equal(decodedMsg.picturePart.picturePart, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(decodedMsg.picturePart.partNumber, 7)
        self.assertEqual(decodedMsg.picturePart.cameraName, 'SarahCam')

    def testSavePicturePartRequestEncodingDecodingShouldFail(self):
        part = np.array([[0, 255], [255, 0]], np.uint8)
        picturePart = PicturePart(part, 7, 'SarahCam')
        msg = SavePicturePartRequest(picturePart)
        self.assertIsNot(msg, None)

        self.assertIsNot(msg.picturePart, None)
        self.assertTrue(np.array_equal(msg.picturePart.picturePart, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.picturePart.partNumber, 7)
        self.assertEqual(msg.picturePart.cameraName, 'SarahCam')

        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testServerListRequestEncodingDecoding(self):
        msg = ServerListRequest(ProcessType.CameraProcess)
        self.assertIsNot(msg, None)

        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, ServerListRequest))
        self.assertEqual(decodedMsg.processType, ProcessType.CameraProcess)
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

    def testServerListRequestEncodingDecodingShouldFail(self):
        msg = ServerListRequest(ProcessType.CameraProcess)
        self.assertIsNot(msg, None)

        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

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


        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, StatisticsRequest))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

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

    def testStatisticsRequestEncodingDecodingShouldFail(self):
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


        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testSubscribeRequestEncodingDecoding(self):
        msg = SubscribeRequest(42)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.clusterId, 42)

        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, SubscribeRequest))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.clusterId, 42)

    def testSubscribeRequestEncodingDecodingShouldFail(self):
        msg = SubscribeRequest(42)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.clusterId, 42)

        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testSyncDataRequestEncodingDecoding(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        data =  [
            PictureInfo(picture, timeStamp, 'Cat Cam')
        ]
        msg = SyncDataRequest(data)
        self.assertIsNot(msg, None)

        self.assertIsNot(msg.data, None)
        self.assertTrue(np.array_equal(msg.data[0].picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.data[0].timeStamp, timeStamp)
        self.assertEqual(msg.data[0].cameraName, 'Cat Cam')


        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)

        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, SyncDataRequest))

        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

        self.assertIsNot(decodedMsg.data, None)
        self.assertTrue(np.array_equal(decodedMsg.data[0].picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(decodedMsg.data[0].timeStamp, timeStamp)
        self.assertEqual(decodedMsg.data[0].cameraName, 'Cat Cam')

    def testSyncDataRequestEncodingDecodingShouldFail(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        data =  [
            PictureInfo(picture, timeStamp, 'Cat Cam')
        ]
        msg = SyncDataRequest(data)
        self.assertIsNot(msg, None)

        self.assertIsNot(msg.data, None)
        self.assertTrue(np.array_equal(msg.data[0].picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.data[0].timeStamp, timeStamp)
        self.assertEqual(msg.data[0].cameraName, 'Cat Cam')


        msgId = msg.messageId
        convId = msg.conversationId

        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

    def testGetPictureRequestEncodingDecoding(self):
        picLocation = 'someFolder/somePic.jpg'

        msg = GetPictureRequest(picLocation)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.picLocation, picLocation)

        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, GetPictureRequest))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)
        self.assertEqual(decodedMsg.picLocation, picLocation)

    def testGetPictureRequestEncodingDecodingShouldFail(self):
        picLocation = 'someFolder/somePic.jpg'

        msg = GetPictureRequest(picLocation)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.picLocation, picLocation)

        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        alteredMsg = encodedMsg[:20] + 'asdfasdfasdfasdf' + encodedMsg[20:]
        self.assertFalse(alteredMsg is encodedMsg)
        self.assertRaises(Exception, Message.decode, alteredMsg)

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

    def testEnvelope(self):
        endpoint = ('localhost', 50000)
        msg = AckReply(True)
        envelope = Envelope(endpoint, msg)
        self.assertIsNot(envelope, None)
        self.assertEqual(envelope.endpoint, endpoint)
        self.assertEqual(envelope.message, msg)

    def testLocalProcessInfo(self):
        self.assertEquals(LocalProcessInfo.getProcessId(),5)
        LocalProcessInfo.setProcessId(16)
        self.assertEquals(LocalProcessInfo.getProcessId(),16)

    def testMessageId(self):
        messageId = MessageId()
        self.assertIsNot(messageId, None)
        seqNum = messageId.sequenceNumber
        nextSeqNum = MessageId.getNextSequenceNumber()
        self.assertGreaterEqual(nextSeqNum, seqNum+1)

    def testPictureInfo(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        data = PictureInfo(picture, timeStamp, 'Most Original Camera Name')

        self.assertIsNot(data, None)
        self.assertTrue(np.array_equal(data.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(data.timeStamp, timeStamp)
        self.assertEqual(data.cameraName, 'Most Original Camera Name')

    def testPictureManagerSmallPic(self):
        frame = np.arange(320*288).reshape(320,288).astype('uint8')
    	splitFrames, numberOfParts = PictureManager.splitPicture(frame)
        for index,picPiece in enumerate(splitFrames):
            picturePart = PicturePart(picPiece, index, "ShemCam")
            partMsg = SavePicturePartRequest(picturePart)
            encodedMsg = partMsg.encode()
            msgSize = len(encodedMsg)
            self.assertGreaterEqual(32000, msgSize)
    	self.assertEqual(len(splitFrames), numberOfParts)
    	combinedFrame = PictureManager.combinePicture(splitFrames)
    	self.assertTrue(np.array_equal(frame, combinedFrame))

    def testPictureManagerLargePic(self):
    	frame = np.arange(640*480).reshape(640,480).astype('uint8')
    	splitFrames, numberOfParts = PictureManager.splitPicture(frame)
        for index,picPiece in enumerate(splitFrames):
            picturePart = PicturePart(picPiece, index, "ShemCam")
            partMsg = SavePicturePartRequest(picturePart)
            msgSize = len(partMsg.encode())
            self.assertGreaterEqual(32000, msgSize)
    	self.assertEqual(len(splitFrames), numberOfParts)
    	combinedFrame = PictureManager.combinePicture(splitFrames)
    	self.assertTrue(np.array_equal(frame, combinedFrame))

    def testPicturePart(self):
        part = np.arange(200).reshape(20,10)
        partNumber = 8
        cameraName = 'Bob Ross'
        picturePart = PicturePart(part, partNumber, cameraName)
        self.assertIsNot(picturePart, None)
        self.assertTrue(np.array_equal(picturePart.picturePart, np.arange(200).reshape(20,10)))
        self.assertEqual(picturePart.partNumber, partNumber)
        self.assertEqual(picturePart.cameraName, cameraName)

    def testProcessType(self):
        self.assertEqual(ProcessType.Registry.value, 1)
        self.assertEqual(ProcessType.MainServer.value, 2)
        self.assertEqual(ProcessType.StatisticsServer.value, 3)
        self.assertEqual(ProcessType.ClientProcess.value, 4)
        self.assertEqual(ProcessType.CameraProcess.value, 5)

    def testPublicEndPoint(self):
        endpoint = PublicEndPoint('127.0.0.3', '4000')
        self.assertIsNot(endpoint, None)
        self.assertEqual(endpoint.host, '127.0.0.3')
        self.assertEqual(endpoint.port, '4000')

    def testEncryptionDecryptionSmall(self):
        key = KeyGenerator.generateKeyPair()
        public_key = key.publickey()
        testString = 'abc123asfasdfasdfasdfasdfasfasdfasdafasdfasdfasdfasdfas' \
            'fasdfasdfasdfasdfasdfasdfasdfasdfasdfasdasdfasdfasdfasdfasdfasdf'
        encryptedString = KeyManager.encryptMessage(public_key, testString)

        decryptedString = KeyManager.decryptMessage(key, encryptedString)
        self.assertEqual(testString, decryptedString)

    def testEncryptionDecryptionLarge(self):
        key = KeyGenerator.generateKeyPair()
        public_key = key.publickey()
        testString = 'ThisShouldBeTheBeginningfasfasdfasdafasdfasdfasdfasdfa2' \
            '340192835102938123ishdaosinv.sknvl9w8rhqirqkj3r23rh98fhqd80s9d8v' \
            '8d709nflknasldkjs8j4p9qnoaudc9a8whwfoaiwnlafkdhoa98csjelfaehfali' \
            'licsuna8rj9p8qt9er8w0987t209348htoisgfdlvs8ernlonrlosnrvosirpet8' \
            'ojv;oisre983ghweufvno3iurfn38jrmbv3oijnsvdriuvlsdirvn;soitvnslkd' \
            'lijrnwivuhrfpwierpowiefvl;kn;oeibsesirogj;eroisje;slknfdlkdfjgs;' \
            ';osidrj;osidrj;sdifvs;oidrn;idj;ois;fn;oidjgs;dlrgndflknd;lfkdfa' \
            'sdfasdfasdfasdfasdfasdfasdfasdfasdasdfasdfasdfasdfasdfaaasdfasdf' \
            'fasdfasdfasdfasdfsdfasdfasdfThisShouldBeTheEnd'
        encryptedString = KeyManager.encryptMessage(public_key, testString)

        decryptedString = KeyManager.decryptMessage(key, encryptedString)
        self.assertEqual(testString, decryptedString)

    def testEncryptionDecryptionRegisterRequest(self):
        key = KeyManager.loadKey('RegistryPrivateKey.pem')
        public_key = KeyManager.loadKey('RegistryPublicKey.pem')
        process_key = KeyGenerator.generateKeyPair()
        process_public_key = process_key.publickey()
        msg = RegisterRequest(ProcessType.MainServer, key=process_public_key)
        encodedMsg = msg.encode()
        encryptedMsg = KeyManager.encryptMessage(public_key, encodedMsg)
        encryptedMsg = 'encryptedRequest{}'.format(encryptedMsg)
        self.assertEqual(encryptedMsg[0:16], 'encryptedRequest')
        decryptedMsg = KeyManager.decryptMessage(key, encryptedMsg[16:])
        self.assertEqual(decryptedMsg, encodedMsg)
        decodedMsg = Message.decode(decryptedMsg)
        self.assertEqual(msg.processType, decodedMsg.processType)
        self.assertEqual(msg.key, decodedMsg.key)

    def testEncryptionDecryptionRegisterReply(self):
        process_key = KeyGenerator.generateKeyPair()
        process_public_key = process_key.publickey()
        msg = RegisterReply(True, 6, process_public_key)
        encodedMsg = msg.encode()
        encryptedMsg = KeyManager.encryptMessage(msg.key, encodedMsg)
        encryptedMsg = 'encryptedReply{}'.format(encryptedMsg)
        self.assertEqual(encryptedMsg[0:14], 'encryptedReply')
        decryptedMsg = KeyManager.decryptMessage(process_key, encryptedMsg[14:])
        self.assertEqual(decryptedMsg, encodedMsg)
        decodedMsg = Message.decode(decryptedMsg)
        self.assertEqual(msg.processId, decodedMsg.processId)

    def testEncryptionDecryptionRegisterRequestReply(self):
        # request
        key = KeyManager.loadKey('RegistryPrivateKey.pem')
        public_key = KeyManager.loadKey('RegistryPublicKey.pem')
        msg = RegisterRequest(ProcessType.MainServer)
        process_key = KeyGenerator.generateKeyPair()
        process_public_key = process_key.publickey()
        msg.key = process_public_key
        encodedMsg = msg.encode()
        encryptedMsg = KeyManager.encryptMessage(public_key, encodedMsg)
        encryptedMsg = 'encryptedRequest{}'.format(encryptedMsg)
        self.assertEqual(encryptedMsg[0:16], 'encryptedRequest')
        decryptedMsg = KeyManager.decryptMessage(key, encryptedMsg[16:])
        self.assertEqual(decryptedMsg, encodedMsg)
        decodedMsg = Message.decode(decryptedMsg)
        self.assertEqual(msg.processType, decodedMsg.processType)
        self.assertEqual(msg.key, decodedMsg.key)

        # reply
        msg = RegisterReply(True, 6, decodedMsg.key)
        encodedMsg = msg.encode()
        encryptedMsg = KeyManager.encryptMessage(msg.key, encodedMsg)
        encryptedMsg = 'encryptedReply{}'.format(encryptedMsg)
        self.assertEqual(encryptedMsg[0:14], 'encryptedReply')
        decryptedMsg = KeyManager.decryptMessage(process_key, encryptedMsg[14:])
        self.assertEqual(decryptedMsg, encodedMsg)
        decodedMsg = Message.decode(decryptedMsg)
        self.assertEqual(msg.processId, decodedMsg.processId)


if __name__ == '__main__':
    unittest.main()
