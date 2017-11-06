from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *

# TODO use template pattern for specialization out of super class methods
class BaseConversation(object):

    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        self.toSocketQueue = toSocketQueue # Used to send a message
        self.fromConversationQueue = fromConversationQueue # Used to pass a message to the main application

        self.myOutgoingMessageQueue = Queue()
        self.myIncomingMessageQueue = Queue()

        if envelopeIsOutgoing:
            self.myOutgoingMessageQueue.append(envelope)
        else:
            self.myIncomingMessageQueue.append(envelope)

        self.shouldRun = True
        thread.startNewThread(self.__run)

    def sendNewMessage(self, envelope):
        """Called from conversation manager for when the application wishes to send a message as a part of the conversation. """
        self.myOutgoingMessageQueue.append(envelope)

    def receivedNewMessage(self, envelope):
        """Called from conversation manager for when a socket receives a message intended for this conversation. """
        self.myIncomingMessageQueue.append(envelope)


    def __run(self):
        while self.shouldRun:
            continue

# TODO separate out the million conversation classes into folders/files

class RegistrationConversation(BaseConversation):
    initiation_message = RegisterRequest
    protocol = {}
    # protocol = {}; #  a dictionary {bool, MessageType} that represents the protocol of the conversation
    # take care of this in the init, but set default in base

    # TODO this is unnecessary unless something other than calling the super init
    # method is happening here
    def __init__(self, message):
        super(RegistrationConversation, self).__init__(message)
        return

# class InitiatedRegistrationConversation(RegistrationConversation):
#     pass
#
# class ReceivedRegistrationConversation(RegistrationConversation):
#     pass

class SubscribeConversation(BaseConversation):
    initiation_message = SubscribeRequest
    protocol = {}

    def __init__(self, message):
        super(SubscribeConversation, self).__init__(message)
        return

# class InitiatedSubscribeConversation(SubscribeConversation):
#     pass
#
# class ReceivedSubscribeConversation(SubscribeConversation):
#     pass

class RequestStatisticsConversation(BaseConversation):
    initiation_message = StatisticsRequest
    protocol = {}

    def __init__(self, message):
        super(RequestStatisticsConversation, self).__init__(message)
        return

# class InitiatedRequestStatisticsConversation(RequestStatisticsConversation):
#     pass
#
# class ReceivedRequestStatisticsConversation(RequestStatisticsConversation):
#     pass

class RawDataQueryConversation(BaseConversation):
    initiation_message = RawQueryRequest
    protocol = {}

    def __init__(self, message):
        super(RawDataQueryConversation, self).__init__(message)
        return

# class InitiatedRawDataQueryConversation(RawDataQueryConversation):
#     pass
#
# class ReceivedRawDataQueryConversation(RawDataQueryConversation):
#     pass

class SyncDataConversation(BaseConversation):
    initiation_message = SyncDataRequest
    protocol = {}

    def __init__(self, message):
        super(SyncDataConversation, self).__init__(message)
        return

# class InitiatedSyncDataConversation(SyncDataConversation):
#     pass
#
# class ReceivedSyncDataConversation(SyncDataConversation):
#     pass

class MainServerListConversation(BaseConversation):
    initiation_message = ServerListRequest
    protocol = {}

    def __init__(self, message):
        super(MainServerListConversation, self).__init__(message)
        return

# class InitiatedMainServerListConversation(MainServerListConversation):
#     pass
#
# class ReceivedMainServerListConversation(MainServerListConversation):
#     pass

class CalculateStatsConversation(BaseConversation):
    initiation_message = CalcStatisticsRequest
    protocol = {}

    def __init__(self, message):
        super(CalculateStatsConversation, self).__init__(message)
        return

# class InitiatedCalculateStatsConversation(CalculateStatsConversation):
#     pass
#
# class ReceivedCalculateStatsConversation(CalculateStatsConversation):
#     pass

class TransferMotionImageConversation(BaseConversation):
    initiation_message = SaveMotionRequest
    protocol = {}

    def __init__(self, message):
        super(TransferMotionImageConversation, self).__init__(message)
        return

# class InitiatedTransferMotionImageConversation(TransferMotionImageConversation):
#     pass
#
# class ReceivedTransferMotionImageConversation(TransferMotionImageConversation):
#     pass

class GetStatusConversation(BaseConversation):
    initiation_message = AliveRequest
    protocol = {}

    def __init__(self, message):
        super(GetStatusConversation, self).__init__(message)
        return

# class InitiatedGetStatusConversation(TransferMotionImageConversation):
#     pass
#
# class ReceivedGetStatusConversation(TransferMotionImageConversation):
#     pass

class ConversationFactory:
    CONVERSATIONS = [RegistrationConversation, SubscribeConversation,
        RequestStatisticsConversation, RawDataQueryConversation,
        SyncDataConversation, MainServerListConversation,
        CalculateStatsConversation, TransferMotionImageConversation,
        GetStatusConversation, ]

    def __init__(self):
        # TODO not sure what should go here yet
        return

    #TODO make all conversations, create mapping to each one based on initialization message, write out protocols per each conversation

    def create_conversation(self, message, is_incoming):
        # message = Message object, is_incoming specifies whether the
        # the message was recieved (or sent)

        # based on message and is_incoming, map to a Conversation class type
        # and instantiate (and update any state) and pass back
        return
