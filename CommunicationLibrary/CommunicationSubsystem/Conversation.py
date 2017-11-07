import Queue
import thread

from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *

class BaseConversation(object):
    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        self.toSocketQueue = toSocketQueue # Used to send a message
        self.fromConversationQueue = fromConversationQueue # Used to pass a message to the main application

        self.myOutgoingMessageQueue = Queue.Queue()
        self.myIncomingMessageQueue = Queue.Queue()

        self.checkOffMessage(self.initiation_message)
        if envelopeIsOutgoing:
            self.myOutgoingMessageQueue.put(envelope)
        else:
            self.myIncomingMessageQueue.put(envelope)

        self.shouldRun = True
        thread.start_new_thread(self.__run, ())

    def checkOffMessage(self, m_type):
        unfinished_messages = [pro for pro in self.protocol if pro['status'] == False]
        if len(unfinished_messages) > 0:
            message = unfinished_messages[0]
            if message['type'] == m_type:
                message['status'] = True
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

    def should_handle(self, m_type, is_last):
        # can be overridden in the subclass or to added to still call super()
        if m_type == AliveRequest:
            return True
        if m_type == AckReply and is_last:
            return True

    def handle(self, m_type):
        # can be overridden in the subclass or to added to still call super()
        message = None
        if m_type == AliveRequest:
            message = AliveReply(True)
            # construct an envelope, where do I get my endpoint from? or create an envelope?
        # if message:
            # put message on socket's queue

    def sendNewMessage(self, envelope):
        """Called from conversation manager for when the application wishes to send a message as a part of the conversation. """
        # QUESTION am I guaranteed an envelope here or should I check for one and construct one if they don't have one?
        m_type, is_last = self.getCurrentMessage
        if isinstance(envelope.message, m_type):
            if self.checkOffMessage(m_type):
                self.myOutgoingMessageQueue.put(message)
                # if is_last:
                    # self destruct on is_last or archive or something?
                return True
        return False

    def receivedNewMessage(self, envelope):
        """Called from conversation manager for when a socket receives a message intended for this conversation. """
        m_type, is_last = self.getCurrentMessage()
        if isinstance(envelope.message, m_type):
            if self.checkOffMessage(m_type):
                if self.should_handle(m_type, is_last):
                    self.handle(m_type)
                else:
                    self.myIncomingMessageQueue.put(envelope)
                # if is_last:
                    # self destruct on last or archive?
                return True
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
    protocol = [{'type': RegisterRequest, 'status': False},
                {'type': RegisterReply, 'status': False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(RegistrationConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

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
    protocol = [{'type': SubscribeRequest, 'status': False},
                {'type': AckReply, 'status': False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(SubscribeConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

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

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(RequestStatisticsConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

    def __str__(self):
        return 'RequestStatisticsConversation'


class InitiatedRequestStatisticsConversation(RequestStatisticsConversation):
    initiated = True
    protocol = [{'type': StatisticsRequest, 'status': False},
                {'type': StatisticsReply, 'status': False}]

    def __str__(self):
        return 'InitiatedRequestStatisticsConversation'

class ReceivedRequestStatisticsConversation(RequestStatisticsConversation):
    initiated = False
    protocol = [{'type': StatisticsRequest, 'status': False},
                # heartbeats
                {'type': CalcStatisticsRequest, 'status': False}]

    def __str__(self):
        return 'ReceivedRequestStatisticsConversation'


class RawDataQueryConversation(BaseConversation):
    initiation_message = RawQueryRequest
    initiated = None
    protocol = [{'type': RawQueryRequest, 'status': False},
                # hearbeats
                {'type': RawQueryReply, 'status': False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(RawDataQueryConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

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
    protocol = [{'type': SyncDataRequest, 'status': False},
                {'type': SyncDataReply, 'status': False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(SyncDataConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

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

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(MainServerListConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

    def __str__(self):
        return 'MainServerListConversation'

class InitiatedMainServerListConversation(MainServerListConversation):
    initiated = True
    protocol = [{'type': ServerListRequest, 'status': False},
                {'type': ServerListReply, 'status': False}]

    def __str__(self):
        return 'InitiatedMainServerListConversation'

class ReceivedMainServerListConversation(MainServerListConversation):
    initiated = False
    protocol = [{'type': ServerListRequest, 'status': False},
                {'type': ServerListReply, 'status': False}]

    def __str__(self):
        return 'ReceivedMainServerListConversation'

class CalculateStatsConversation(BaseConversation):
    initiation_message = CalcStatisticsRequest
    initiated = None # this conversation will only ever be received however
    protocol = [{'type': CalcStatisticsRequest, 'status': False},
                # heartbeats
                {'type': StatisticsReply, 'status': False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(CalculateStatsConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

    def __str__(self):
        return 'CalculateStatsConversation'

class TransferMotionImageConversation(BaseConversation):
    initiation_message = SaveMotionRequest
    initiated = None
    protocol = [{'type': SaveMotionRequest, 'status': False},
                {'type': MotionDetectedReply, 'status': False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(TransferMotionImageConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

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
    protocol = [{'type': AliveRequest, 'status': False},
                {'type': AliveReply, 'status': False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(GetStatusConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

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

    def create_conversation(self, envelope, is_outgoing, toSocketQueue, fromConversationQueue):
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
                fromConversationQueue=fromConversationQueue)
        return conversation
