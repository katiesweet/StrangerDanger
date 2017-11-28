import Queue
import thread
import logging
from threading import Timer
import time

from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *
from CommunicationLibrary.Messages.SharedObjects.Envelope import Envelope

from multiprocessing import Value


class BaseConversation(object):
    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc):
        self.toSocketQueue = toSocketQueue # Used to send a message
        self.fromConversationQueue = fromConversationQueue # Used to pass a message to the main application

        self.destructFunc = destructFunc

        self.myOutgoingMessageQueue = Queue.Queue()
        self.myIncomingMessageQueue = Queue.Queue()

        if envelopeIsOutgoing:
            self.sendNewMessage(envelope)
        else:
            self.receivedNewMessage(envelope)

        # self.waiting = False
        self.waiting = Value('b', False)
        self.missed_waits = 0
        self.max_missed_waits = 5
        self.resent_count = 0
        self.max_resent_count = 3

        self.shouldRun = True
        thread.start_new_thread(self.__run, ())


    def checkOffMessage(self, envelope):
        unfinished_messages = [pro for pro in self.protocol if pro['status'] == False]
        if len(unfinished_messages) > 0:
            message = unfinished_messages[0]
            if message['type'] == type(envelope.message):
                message['status'] = True
                message['envelope'] = envelope
                return True
        return False

    def getCurrentMessage(self):
        messageType = None
        is_last = False
        unfinished_messages = [pro for pro in self.protocol if pro['status'] == False]
        if len(unfinished_messages) > 0:
            messageType = unfinished_messages[0]['type']
        if len(unfinished_messages) == 1:
            is_last = True
        return (messageType, is_last)

    def getLastMessageReceived(self):
        m_type = None
        received_messages = [pro for pro in self.protocol if pro['status'] == True and pro['outgoing'] == False]
        if len(received_messages) > 0:
            m_type = received_messages[len(received_messages)-1]['type']
        return m_type

    def getLastMessageSent(self):
        envelope = None
        sent_messages = [pro for pro in self.protocol if pro['status'] == True and pro['outgoing'] == True]
        if len(sent_messages) > 0:
            envelope = sent_messages[len(sent_messages)-1]['envelope']
        return envelope

    def should_handle(self, m_type, is_last):
        # can be overridden in the subclass or to added to still call super()
        if m_type == AliveRequest:
            return True
        if m_type == AckReply and is_last:
            return True

    def handle(self, m_type, prev_envelope):
        # can be overridden in the subclass or to added to still call super()
        message = None
        if m_type == AliveRequest:
            message = AliveReply(True)
        if message and prev_envelope:
            message.setConversationId(prev_envelope.message.conversationId)
            envelope = Envelope(message=message, endpoint=prev_envelope.endpoint)
            if envelope:
                self.sendNewMessage(envelope)

    def resendMessage(self, envelope):
        envelope = self.getLastMessageSent()
        if envelope:
            self.waiting = True
            self.missed_waits = 0
            self.myOutgoingMessageQueue.put(envelope)
            return True
        return False

    def checkReceived(self):
        while self.waiting:
            time.sleep(1)
            if self.waiting:
                self.missed_waits += 1
                logging.debug("missed message")
                if self.missed_waits >= self.max_missed_waits:
                    self.resent_count += 1
                    if self.resent_count > self.max_resent_count:
                        envelope = self.getLastMessageSent()
                        if envelope and  self.destructFunc:
                            logging.debug("destroying conversation, recipient endpoint not available")
                            self.destructFunc(envelope.message.conversationId)
                        else:
                            self.waiting = False
                    else:
                        logging.info("trying to resend message")
                        self.resendMessage(self.getLastMessageSent())
        logging.debug('...finished waiting...')

    def sendNewMessage(self, envelope):
        # QUESTION allow to send a message while timer is running? Not sure when that should ever happen.
        """Called from conversation manager for when the application wishes to send a message as a part of the conversation. """
        m_type, is_last = self.getCurrentMessage()
        if m_type:
            if isinstance(envelope.message, m_type):
                if self.checkOffMessage(envelope):
                    logging.debug("sending message of {0} type".format(m_type))
                    self.myOutgoingMessageQueue.put(envelope)
                    if is_last and self.destructFunc:
                        self.destructFunc(envelope.message.conversationId)
                    if not is_last:
                        self.waiting = True
                        self.missed_waits = 0
                        self.resent_count = 0
                        thread.start_new_thread(self.checkReceived, ())
                    return True
        return False

    def receivedNewMessage(self, envelope):
        """Called from conversation manager for when a socket receives a message intended for this conversation. """
        m_type, is_last = self.getCurrentMessage()
        if m_type:
            if isinstance(envelope.message, m_type):
                self.waiting = False
                self.missed_waits = 0
                self.resent_count = 0
                if self.checkOffMessage(envelope):
                    logging.debug("received message of {0} type".format(m_type))
                    if self.should_handle(m_type, is_last):
                        self.handle(m_type, envelope)
                    else:
                        self.myIncomingMessageQueue.put(envelope)
                    if is_last and self.destructFunc:
                        self.destructFunc(envelope.message.conversationId)
                    return True
                else:
                    if self.getLastMessageReceived() == m_type:
                        if self.resendMessage():
                            return True
                    # else QUESTION should we do anything else there?
        return False

    def __run(self):
        while self.shouldRun:
            if not self.myOutgoingMessageQueue.empty():
                message = self.myOutgoingMessageQueue.get()
                self.toSocketQueue.put(message)
            if not self.myIncomingMessageQueue.empty():
                message = self.myIncomingMessageQueue.get()
                self.fromConversationQueue.put(message)


# TODO separate out the million conversation classes into folders/files
class RegistrationConversation(BaseConversation):
    initiation_message = RegisterRequest
    initiated = None
    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc):
        self.protocol = self.createProtocol(envelopeIsOutgoing)
        super(RegistrationConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc)
        logging.info("created RegistrationConversation")
        return

    def createProtocol(self, is_outgoing):
        protocol = [{'type': RegisterRequest, 'envelope': None, 'outgoing': is_outgoing, 'status': False},
                    {'type': RegisterReply, 'envelope': None, 'outgoing': (not is_outgoing), 'status': False}]
        return protocol

    def __str__(self):
        return 'RegistrationConversation'
# class InitiatedRegistrationConversation(RegistrationConversation):
#     pass
#
# class ReceivedRegistrationConversation(RegistrationConversation):
#     pass


class SubscribeConversation(BaseConversation):
    initiation_message = SubscribeRequest
    initiated = None

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc):
        self.protocol = self.createProtocol(envelopeIsOutgoing)
        super(SubscribeConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc)
        logging.info("created SubscribeConversation")
        return

    def createProtocol(self, is_outgoing):
        protocol = [{'type': SubscribeRequest, 'envelope': None, 'outgoing': is_outgoing, 'status': False},
                    {'type': AckReply, 'envelope': None, 'outgoing': (not is_outgoing), 'status': False}]
        return protocol

    def __str__(self):
        return 'SubscribeConversation'
# class InitiatedSubscribeConversation(SubscribeConversation):
#     pass
#
# class ReceivedSubscribeConversation(SubscribeConversation):
#     pass


class RequestStatisticsConversation(BaseConversation):
    initiation_message = StatisticsRequest
    initiated = None

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc):
        self.protocol = self.createProtocol()
        super(RequestStatisticsConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc)
        logging.info("created RequestStatisticsConversation")
        return

    def __str__(self):
        return 'RequestStatisticsConversation'

class InitiatedRequestStatisticsConversation(RequestStatisticsConversation):
    initiated = True

    def createProtocol(self):
        protocol = [{'type': StatisticsRequest, 'envelope': None, 'outgoing': True, 'status': False},
                    {'type': StatisticsReply, 'envelope': None, 'outgoing': False, 'status': False}]
        return protocol

    def __str__(self):
        return 'InitiatedRequestStatisticsConversation'

class ReceivedRequestStatisticsConversation(RequestStatisticsConversation):
    initiated = False

    def createProtocol(self):
        protocol = [{'type': StatisticsRequest, 'envelope': None, 'outgoing': False, 'status': False},
                    # heartbeats
                    {'type': CalcStatisticsRequest, 'envelope': None, 'outgoing': True, 'status': False}]
        return protocol

    def __str__(self):
        return 'ReceivedRequestStatisticsConversation'


class RawDataQueryConversation(BaseConversation):
    initiation_message = RawQueryRequest
    initiated = None

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc):
        self.protocol = self.createProtocol(envelopeIsOutgoing)
        super(RawDataQueryConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc)
        logging.info("created RawDataQueryConversation")
        return

    def createProtocol(self, is_outgoing):
        protocol = [{'type': RawQueryRequest, 'envelope': None, 'outgoing': is_outgoing, 'status': False},
                    # hearbeats
                    {'type': RawQueryReply, 'envelope': None, 'outgoing': (not is_outgoing), 'status': False}]
        return protocol

    def __str__(self):
        return 'RawDataQueryConversation'
# class InitiatedRawDataQueryConversation(RawDataQueryConversation):
#     pass
#
# class ReceivedRawDataQueryConversation(RawDataQueryConversation):
#     pass


class SyncDataConversation(BaseConversation):
    initiation_message = SyncDataRequest
    initiated = None

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc):
        self.protocol = self.createProtocol(envelopeIsOutgoing)
        super(SyncDataConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc)
        logging.info("created SyncDataConversation")
        return

    def createProtocol(self, is_outgoing):
        protocol = [{'type': SyncDataRequest, 'envelope': None, 'outgoing': is_outgoing, 'status': False},
                    {'type': SyncDataReply, 'envelope': None, 'outgoing': (not is_outgoing), 'status': False}]
        return protocol

    def __str__(self):
        return 'SyncDataConversation'
# class InitiatedSyncDataConversation(SyncDataConversation):
#     pass
#
# class ReceivedSyncDataConversation(SyncDataConversation):
#     pass


class MainServerListConversation(BaseConversation):
    initiation_message = ServerListRequest
    initiated = None

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc):
        self.protocol = self.createProtocol()
        super(MainServerListConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc)
        logging.info("created MainServerListConversation")
        return

    def __str__(self):
        return 'MainServerListConversation'

class InitiatedMainServerListConversation(MainServerListConversation):
    initiated = True

    def createProtocol(self):
        protocol = [{'type': ServerListRequest, 'envelope': None, 'outgoing': True, 'status': False},
                    {'type': ServerListReply, 'envelope': None, 'outgoing': False, 'status': False}]
        return protocol

    def __str__(self):
        return 'InitiatedMainServerListConversation'

class ReceivedMainServerListConversation(MainServerListConversation):
    initiated = False

    def createProtocol(self):
        protocol = [{'type': ServerListRequest, 'envelope': None, 'outgoing': False, 'status': False},
                    {'type': ServerListReply, 'envelope': None, 'outgoing': True, 'status': False}]
        return protocol

    def __str__(self):
        return 'ReceivedMainServerListConversation'


class CalculateStatsConversation(BaseConversation):
    initiation_message = CalcStatisticsRequest
    initiated = None # this conversation will only ever be received however

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc):
        self.protocol = self.createProtocol(envelopeIsOutgoing)
        super(CalculateStatsConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc)
        logging.info("created CalculateStatsConversation")
        return

    def createProtocol(self, is_outgoing):
        protocol = [{'type': CalcStatisticsRequest, 'envelope': None, 'outgoing': is_outgoing, 'status': False},
                    # heartbeats
                    {'type': StatisticsReply, 'envelope': None, 'outgoing': (not is_outgoing), 'status': False}]
        return protocol

    def __str__(self):
        return 'CalculateStatsConversation'


class TransferMotionImageConversation(BaseConversation):
    initiation_message = SaveMotionRequest
    initiated = None

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc):
        self.protocol = self.createProtocol(envelopeIsOutgoing)
        super(TransferMotionImageConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc)
        logging.info("created TransferMotionImageConversation")
        return

    def createProtocol(self, is_outgoing):
        protocol = [{'type': SaveMotionRequest, 'envelope': None, 'outgoing': is_outgoing, 'status': False},
                    {'type': MotionDetectedReply, 'envelope': None, 'outgoing': (not is_outgoing), 'status': False}]
        return protocol

    def __str__(self):
        return 'TransferMotionImageConversation'
# class InitiatedTransferMotionImageConversation(TransferMotionImageConversation):
#     pass
#
# class ReceivedTransferMotionImageConversation(TransferMotionImageConversation):
#     pass


class GetStatusConversation(BaseConversation):
    initiation_message = AliveRequest
    initiated = None

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc):
        self.protocol = self.createProtocol(envelopeIsOutgoing)
        super(GetStatusConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue, destructFunc)
        logging.info("created GetStatusConversation")
        return

    def createProtocol(self, is_outgoing):
        protocol = [{'type': AliveRequest, 'envelope': None, 'outgoing': is_outgoing, 'status': False},
                    {'type': AliveReply, 'envelope': None, 'outgoing': (not is_outgoing), 'status': False}]
        return protocol

    def __str__(self):
        return 'GetStatusConversation'
# class InitiatedGetStatusConversation(TransferMotionImageConversation):
#     pass
#
# class ReceivedGetStatusConversation(TransferMotionImageConversation):
#     pass


class ConversationFactory:
    CONVERSATION_TYPES = [RegistrationConversation, SubscribeConversation,
        RawDataQueryConversation, ReceivedRequestStatisticsConversation,
        InitiatedRequestStatisticsConversation, SyncDataConversation,
        ReceivedMainServerListConversation, InitiatedMainServerListConversation,
        CalculateStatsConversation, TransferMotionImageConversation,
        GetStatusConversation, ]

    def __init__(self):
        return

    def __str__(self):
        return 'Conversation Factory'

    def create_conversation(self, envelope, is_outgoing, toSocketQueue, fromConversationQueue, destructFunc):
        class_type = None
        conversation = None
        for convo in self.CONVERSATION_TYPES:
            if convo.initiated == True:
                if convo.initiation_message == type(envelope.message) and is_outgoing:
                    class_type = convo
                    break;
            elif convo.initiated == False:
                if convo.initiation_message == type(envelope.message) and not is_outgoing:
                    class_type = convo
                    break;
            elif convo.initiated == None:
                if convo.initiation_message == type(envelope.message):
                    class_type = convo
                    break;
        if class_type:
            conversation = class_type(envelope=envelope,
                envelopeIsOutgoing=is_outgoing, toSocketQueue=toSocketQueue,
                fromConversationQueue=fromConversationQueue, destructFunc=destructFunc)
        return conversation
