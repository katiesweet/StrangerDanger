import unittest
import sys
import Queue
sys.path.append("../../")

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem, ConversationManager, UdpConnection
from CommunicationLibrary.Messages.SharedObjects.Envelope import Envelope

class CommunicationSubsystem_Test(unittest.TestCase):

    ############ Communication Subsystem Class ##############
    def test_CommunicationSubsystem_Constructor(self):
        commSub = CommunicationSubsystem.CommunicationSubsystem()
        self.assertIsNot(commSub, None)

    def test_CommunicationSubsystem_GetMessage(self):
        commSub = CommunicationSubsystem.CommunicationSubsystem()
        self.assertIsNot(commSub, None)

        getMessageResponse = commSub.getMessage()
        self.assertEqual(getMessageResponse[0], False)
        self.assertEqual(getMessageResponse[1], "")

        commSub.fromConversationQueue.put("TestMessage")
        getMessageResponse = commSub.getMessage()
        self.assertEqual(getMessageResponse[0], True)
        self.assertEqual(getMessageResponse[1], "TestMessage")

        getMessageResponse = commSub.getMessage()
        self.assertEqual(getMessageResponse[0], False)
        self.assertEqual(getMessageResponse[1], "")

    ########### ConversationManager ############
    def test_ConversationManager__ConstructorRunning(self):
        endpoint = ('localhost', 0)
        fromQueue = Queue.Queue()

        connMan = ConversationManager.ConversationManager(fromQueue, endpoint)
        self.assertIsNot(connMan, None)
        self.assertIs(connMan.fromConversationQueue, fromQueue)
        self.assertEqual(connMan.conversations, {})
        self.assertTrue(connMan.shouldRun)

    def test_ConversationManager__ConstructorNotRunning(self):
        endpoint = ('localhost', 0)
        fromQueue = Queue.Queue()

        connMan = ConversationManager.ConversationManager(fromQueue, endpoint, False)
        self.assertIs(connMan.fromConversationQueue, fromQueue)
        self.assertEqual(connMan.conversations, {})
        self.assertFalse(connMan.shouldRun)

    def test_ConversationManager__SendMessage(self):
        endpoint = ('localhost', 0)
        fromQueue = Queue.Queue()

        connMan = ConversationManager.ConversationManager(fromQueue, endpoint, False)
        envelope = Envelope(('localhost', 50000), "TestMessage")
        connMan.sendMessage(envelope)
        self.assertEqual(connMan.toSocketQueue.qsize(), 1)

    ######## UdpConnection #############
    def test_UdpConnection_Constructor(self):
        outQueue = Queue.Queue()
        inQueue = Queue.Queue()
        endpoint = ('localhost', 0)

        socket = UdpConnection.UdpConnection(outQueue, inQueue, endpoint)
        self.assertIsNot(socket, None)
        self.assertIs(socket.outgoingMessageQueue, outQueue)
        self.assertIs(socket.incomingMessageQueue, inQueue)
        self.assertTrue(socket.shouldListen)


if __name__ == '__main__':
    unittest.main()
