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

        if envelopeIsOutgoing:
            self.myOutgoingMessageQueue.put(envelope)
        else:
            self.myIncomingMessageQueue.put(envelope)
        print(self.protocol)
        self.shouldRun = True
        # thread.startNewThread(self.__run)
        thread.start_new_thread(self.__run, ())

    def checkOffMessage(self, index):
        # TODO this is just psuedo code
        self.protocol[index] = True

    def getCurrentMessage(self):
        # TODO this is just psuedo code
        currentType = None
        if False in self.protocol.values();
            for messageType in self.protocol:
                if self.protocol.get(messageType) == False:
                    currentType = self.protocol.messageType
        return currentType, index

    def sendNewMessage(self, envelope):
        """Called from conversation manager for when the application wishes to send a message as a part of the conversation. """
        self.myOutgoingMessageQueue.put(envelope)

    def receivedNewMessage(self, envelope):
        """Called from conversation manager for when a socket receives a message intended for this conversation. """
        # handle the case that it is the last message in the protocol
        # handle the case that it doesn't need to be sent to the application
        # also check that the message matches the protocol
        # if it does
            # handle it by checking if it is the last message
            # handle it by checking that it doesn't need to be sent to the application
            # handle it by sending it ot the application
        self.myIncomingMessageQueue.put(envelope)

    def __run(self):
        while self.shouldRun:
            continue
            # if not self.myOutgoingMessageQueue.empty():
            #     message = self.myOutgoingMessageQueue.get()
            #     self.toSocketQueue.put(message)
            # if not self.myIncomingMessageQueue.empty():
            #     message = self.myIncomingMessageQueue.get()
            #     self.fromConversationQueue.put(message)


# TODO separate out the million conversation classes into folders/files
class RegistrationConversation(BaseConversation):
    initiation_message = RegisterRequest
    protocol = [{RegisterRequest, False},
                {RegisterReply, False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(RegistrationConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

# class InitiatedRegistrationConversation(RegistrationConversation):
#     pass
#
# class ReceivedRegistrationConversation(RegistrationConversation):
#     pass

class SubscribeConversation(BaseConversation):
    initiation_message = SubscribeRequest
    protocol = [{SubscribeRequest, False},
                {AckReply, False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(SubscribeConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

# class InitiatedSubscribeConversation(SubscribeConversation):
#     pass
#
# class ReceivedSubscribeConversation(SubscribeConversation):
#     pass

class RequestStatisticsConversation(BaseConversation):
    initiation_message = StatisticsRequest

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(RequestStatisticsConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

class InitiatedRequestStatisticsConversation(RequestStatisticsConversation):
    protocol = [{StatisticsRequest, False},
                # QUESTION receiving heartbeats here
                {StatisticsReply, False}]

class ReceivedRequestStatisticsConversation(RequestStatisticsConversation):
    protocol = [{StatisticsRequest, False},
                # TODO put in seconds for sending these in loop
                {CalcStatisticsRequest, False}]

class RawDataQueryConversation(BaseConversation):
    initiation_message = RawQueryRequest
    protocol = [{RawQueryRequest, False},
                # QUESTION{AliveRequest/AliveReply/AckReply, False}, # representing state messages?
                {RawQueryReply, False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(RawDataQueryConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

# class InitiatedRawDataQueryConversation(RawDataQueryConversation):
#     pass
#
# class ReceivedRawDataQueryConversation(RawDataQueryConversation):
#     pass

class SyncDataConversation(BaseConversation):
    initiation_message = SyncDataRequest
    protocol = [{SyncDataRequest, False},
                {SyncDataReply, False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(SyncDataConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

# class InitiatedSyncDataConversation(SyncDataConversation):
#     pass
#
# class ReceivedSyncDataConversation(SyncDataConversation):
#     pass

class MainServerListConversation(BaseConversation):
    initiation_message = ServerListRequest

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(MainServerListConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

class InitiatedMainServerListConversation(MainServerListConversation):
    protocol = [{ServerListRequest, False},
                {ServerListReply, False}]

class ReceivedMainServerListConversation(MainServerListConversation):
    protocol = [{ServerListRequest, False},
                # {AliveRequest, False},  # QUESTION represent creation message for a new conversation here?
                {ServerListReply, False}]


class CalculateStatsConversation(BaseConversation):
    initiation_message = CalcStatisticsRequest
    protocol = [{CalcStatisticsRequest, False},
                # QUESTION sending state back to client
                {StatisticsReply, False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(CalculateStatsConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return


class TransferMotionImageConversation(BaseConversation):
    initiation_message = SaveMotionRequest
    protocol = [{SaveMotionRequest, False},
                {MotionDetectedReply, False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(TransferMotionImageConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

# class InitiatedTransferMotionImageConversation(TransferMotionImageConversation):
#     pass
#
# class ReceivedTransferMotionImageConversation(TransferMotionImageConversation):
#     pass

class GetStatusConversation(BaseConversation):
    initiation_message = AliveRequest
    protocol = [{AliveRequest, False},
                {AliveReply, False}]

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        super(GetStatusConversation, self).__init__(envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue)
        return

# class InitiatedGetStatusConversation(TransferMotionImageConversation):
#     pass
#
# class ReceivedGetStatusConversation(TransferMotionImageConversation):
#     pass

class ConversationFactory:
    CONVERSATION_TYPES = [RegistrationConversation, SubscribeConversation,
        RequestStatisticsConversation, RawDataQueryConversation,
        SyncDataConversation, MainServerListConversation,
        CalculateStatsConversation, TransferMotionImageConversation,
        GetStatusConversation, ]
        # TODO add in received/initalized only conversation classes as needed...

    def __init__(self):
        # QUESTION not sure what should go here yet
        return

    def create_conversation(self, envelope, is_outgoing, toSocketQueue, fromConversationQueue):
        class_type = None
        conversation = None
        for convo in self.CONVERSATION_TYPES:
            if convo.initiation_message == type(envelope): #TODO use is_outgoing to distinguish between initialized/received conversation types
                class_type = convo
                break;
        if class_type:
            conversation = class_type(envelope=envelope,
                envelopeIsOutgoing=is_outgoing, toSocketQueue=toSocketQueue,
                fromConversationQueue=fromConversationQueue)
        return conversation
