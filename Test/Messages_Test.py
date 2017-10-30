#!/usr/bin/python2
import unittest
from CommunicationLibrary.Messages.AbstractMessages import *
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *


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


if __name__ == '__main__':
    unittest.main()
