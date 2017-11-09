import unittest
import sys
import Queue
sys.path.append("../../")

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem, ConversationManager, UdpConnection
from CommunicationLibrary.Messages.SharedObjects.Envelope import Envelope
from CommunicationLibrary.CommunicationSubsystem.Conversation import *
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *

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

        envelope = Envelope(('localhost', 50000), AliveRequest())
        commSub.fromConversationQueue.put(envelope)
        getMessageResponse = commSub.getMessage()
        self.assertEqual(getMessageResponse[0], True)
        self.assertEqual(getMessageResponse[1], envelope)

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

        class Conversation:
            def __init__(self,):
                pass
            def sendNewMessage(self,envelope):
                self.envelope = envelope

        connMan.conversations["Test"] = Conversation()
        envelope = Envelope(('localhost', 50000), AliveRequest())
        envelope.message.setConversationId("Test")

        connMan.sendMessage(envelope)
        self.assertEqual(connMan.conversations["Test"].envelope, envelope)

    def test_ConversationManager__DeleteConversation(self):
        endpoint = ('localhost', 0)
        fromQueue = Queue.Queue()
        connMan = ConversationManager.ConversationManager(fromQueue, endpoint)

        self.assertEqual(connMan.conversations, {})
        connMan.conversations["Test"] = "TestConversation"
        self.assertEqual(connMan.conversations, {"Test": "TestConversation"})
        connMan.deleteConversation("Test")
        self.assertEqual(connMan.conversations, {})

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


    ######## ConversationFactory #############
    def test_create_conversation(self):
        cf = ConversationFactory()
        r_message = RegisterRequest("test")
        env = Envelope(message=r_message, endpoint='endpoint')
        is_outgoing = True
        convo = cf.create_conversation(env, is_outgoing, Queue.Queue(), Queue.Queue(), None)
        self.assertEqual(type(convo), RegistrationConversation)
        is_outgoing  = False
        convo = cf.create_conversation(env, is_outgoing, Queue.Queue(), Queue.Queue(), None)
        self.assertEqual(type(convo), RegistrationConversation)

    def test_create_incoming_conversation(self):
        cf = ConversationFactory()
        s_message = ServerListRequest()
        env = Envelope(message=s_message, endpoint='endpoint')
        is_outgoing = True
        convo = cf.create_conversation(env, is_outgoing, Queue.Queue(), Queue.Queue(), None)
        self.assertEqual(type(convo), InitiatedMainServerListConversation)

    def test_create_outgoing_conversation(self):
        cf = ConversationFactory()
        s_message = ServerListRequest()
        env = Envelope(message=s_message, endpoint='endpoint')
        is_outgoing = False
        convo = cf.create_conversation(env, is_outgoing, Queue.Queue(), Queue.Queue(), None)
        self.assertEqual(type(convo), ReceivedMainServerListConversation)

    def test_create_conversation_with_invalid_message(self):
        cf = ConversationFactory()
        a_message = AliveReply(True)
        env = Envelope(message=a_message, endpoint='endpoint')
        is_outgoing = False
        convo = cf.create_conversation(env, is_outgoing, Queue.Queue(), Queue.Queue(), None)
        self.assertEqual(convo, None)
        is_outgoing = True
        convo = cf.create_conversation(env, is_outgoing, Queue.Queue(), Queue.Queue(), None)
        self.assertEqual(convo, None)

    ######## Conversations #############

    def test_conversation_creation_updates_protocol(self):
        cf = ConversationFactory()
        r_message = RegisterRequest("test")
        env = Envelope(message=r_message, endpoint='endpoint')
        is_outgoing = True
        convo = cf.create_conversation(env, is_outgoing, Queue.Queue(), Queue.Queue(), None)
        pro = [pro for pro in convo.protocol if pro['type'] == convo.initiation_message]
        self.assertTrue(pro[0]['status'])

    def test_protocol_get_current_message(self):
        cf = ConversationFactory()
        r_message = RegisterRequest("test")
        env = Envelope(message=r_message, endpoint='endpoint')
        is_outgoing = True
        convo = cf.create_conversation(env, is_outgoing, Queue.Queue(), Queue.Queue(), None)
        expected_type = convo.protocol[1]['type']
        expected_is_last = True
        type, is_last = convo.getCurrentMessage()
        self.assertEqual(type, expected_type)
        self.assertEqual(is_last, expected_is_last)

    def test_protocol_updates_on_receive(self):
        cf = ConversationFactory()
        r_message = RegisterRequest("test")
        env = Envelope(message=r_message, endpoint='endpoint')
        is_outgoing = True
        convo = cf.create_conversation(env, is_outgoing, Queue.Queue(), Queue.Queue(), None)
        reply_m = RegisterReply("test", "test")
        env2 = Envelope(message=reply_m, endpoint='endpoint')
        pro = [pro for pro in convo.protocol if pro['type'] == type(reply_m)]
        self.assertFalse(pro[0]['status'])
        convo.receivedNewMessage(env2)
        pro = [pro for pro in convo.protocol if pro['type'] == type(reply_m)]
        self.assertTrue(pro[0]['status'])

    def test_protocol_convo_reieves_invalid_message(self):
        cf = ConversationFactory()
        r_message = RegisterRequest("test")
        env = Envelope(message=r_message, endpoint='endpoint')
        is_outgoing = True
        convo = cf.create_conversation(env, is_outgoing, Queue.Queue(), Queue.Queue(), None)
        reply_s = ServerListRequest()
        env2 = Envelope(message=reply_s, endpoint='endpoint')
        pro = [pro for pro in convo.protocol if pro['status'] == False]
        prev_length = len(pro)
        convo.receivedNewMessage(env2)
        pro2 = [pro for pro in convo.protocol if pro['status'] == False]
        current_length = len(pro2)
        self.assertEqual(prev_length, current_length)

    def test_convo_handles(self):
        cf = ConversationFactory()
        a_message = AliveRequest()
        env = Envelope(message=a_message, endpoint='endpoint')
        is_outgoing = False
        convo = cf.create_conversation(env, is_outgoing, Queue.Queue(), Queue.Queue(), None)
        pro = [pro for pro in convo.protocol if pro['status'] == False]
        self.assertEqual(len(pro), 0)


if __name__ == '__main__':
    unittest.main()
