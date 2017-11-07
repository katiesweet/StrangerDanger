#!/usr/bin/python2
import unittest
import numpy as np
from datetime import datetime, date
import sys
sys.path.append("../")

from CommunicationLibrary.Messages.AbstractMessages import *
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *
from CommunicationLibrary.Messages.SharedObjects import *
from CommunicationLibrary.Messages.SharedObjects.LocalProcessInfo import LocalProcessInfo
from CommunicationLibrary.Messages.SharedObjects.ProcessType import ProcessType
from RegistryServer.Registry import Registry

class TestMessages(unittest.TestCase):

    # runs once for all class tests
    @classmethod
    def setUpClass(cls):
        LocalProcessInfo.setProcessId(5)

    def testLocalProcessInfo(self):
        self.assertEquals(LocalProcessInfo.getProcessId(),5)



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
        self.assertEqual(decodedMsg.data.cameraId, 1)
        self.assertEqual(decodedMsg.data.clusterId, 2)

    def testRegisterReplyEncodingDecoding(self):
        nextProcessId = Registry.getNextProcessId()
        msg = RegisterReply(True, nextProcessId)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.processId, nextProcessId)

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

        self.assertIsNot(decodedMsg.data, None)
        self.assertTrue(np.array_equal(decodedMsg.data[0].picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(decodedMsg.data[0].timeStamp, timeStamp)

        self.assertEqual(decodedMsg.data[0].cameraId, 4)
        self.assertEqual(decodedMsg.data[0].clusterId, 5)

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

    def testRegisterRequestEncodingDecoding(self):
        msg = RegisterRequest(ProcessType.MainServer)
        self.assertIsNot(msg, None)
        self.assertEqual(msg.processType, ProcessType.MainServer)

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

    def testSaveMotionRequestEncodingDecoding(self):
        picture = np.array([[0, 255], [255, 0]], np.uint8)
        timeStamp = datetime.now()
        pictureInfo = PictureInfo(picture, timeStamp, 1, 2)
        msg = SaveMotionRequest(pictureInfo, 'Ya boi Shem')
        self.assertIsNot(msg, None)
        self.assertEqual(msg.cameraName, 'Ya boi Shem')

        self.assertIsNot(msg.pictureInfo, None)
        self.assertTrue(np.array_equal(msg.pictureInfo.picture, np.array([[0, 255], [255, 0]], np.uint8)))
        self.assertEqual(msg.pictureInfo.timeStamp, timeStamp)
        self.assertEqual(msg.pictureInfo.cameraId, 1)
        self.assertEqual(msg.pictureInfo.clusterId, 2)

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
        self.assertEqual(decodedMsg.pictureInfo.cameraId, 1)
        self.assertEqual(decodedMsg.pictureInfo.clusterId, 2)

    def testServerListRequestEncodingDecoding(self):
        msg = ServerListRequest()
        self.assertIsNot(msg, None)

        msgId = msg.messageId
        convId = msg.conversationId
        encodedMsg = msg.encode()
        decodedMsg = Message.decode(encodedMsg)
        self.assertIsNot(decodedMsg, None)
        self.assertTrue(isinstance(decodedMsg, Message))
        self.assertTrue(isinstance(decodedMsg, Request))
        self.assertTrue(isinstance(decodedMsg, ServerListRequest))
        self.assertEqual(decodedMsg.conversationId, convId)
        self.assertEqual(decodedMsg.messageId, msgId)

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
