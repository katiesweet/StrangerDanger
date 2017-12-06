import Queue
import Conversation
import UdpConnection
import thread
import logging

class ConversationManager:
    """Conversation Level Communication Protocol Manager"""
    def __init__(self, fromConversationQueue, myEndpoint, shouldRun = True):

        self.fromConversationQueue = fromConversationQueue # Messages for app
        self.toSocketQueue = Queue.Queue() # Messages to be sent by socket
        self.fromSocketQueue = Queue.Queue() # Messages received by socket

        self.udpSocket = UdpConnection.UdpConnection(self.toSocketQueue, self.fromSocketQueue, myEndpoint)

        self.conversationFactory = Conversation.ConversationFactory()

        # Conversation Id: Conversation
        self.conversations = {}

        # Thread management
        self.shouldRun = shouldRun
        thread.start_new_thread(self.__run, ())

    def __del__(self):
        # TODO: This destructor isn't getting called.
        logging.info("Destroying UDP Socket")
        self.shouldRun = False

    def sendMessage(self, envelope):
        """Called by Communication Protocol when the application layer wants to send a new message."""
        convoId = str(envelope.message.conversationId)
        if convoId in self.conversations:
            self.conversations[convoId].sendNewMessage(envelope)
        else:
            self.__createConversation(envelope, envelopeIsOutgoing=True)

    def __createConversation(self, envelope, envelopeIsOutgoing):
        """Creates a conversation and appends it to the class' known conversations. The Conversation.Conversation() constructor should be a factory that returns the appropriate conversation type. The constructor also handles sending the first message automatically."""
        convoId = str(envelope.message.conversationId)
        logging.debug("Creating conversation with conversationId " + \
            repr(convoId))
        self.conversations[convoId] = self.conversationFactory.create_conversation(envelope, envelopeIsOutgoing, self.toSocketQueue, self.fromConversationQueue, self.deleteConversation)

    def deleteConversation(self, conversationId):
        if str(conversationId) in self.conversations:
            logging.info("deleting conversation {0}".format(conversationId))
            try:
                self.conversations.pop(str(conversationId))
            except:
                logging.error("Cannot delete conversation " + str(conversationId) + ". Does not exist.")

    def __run(self):
        while self.shouldRun:
            if not self.fromSocketQueue.empty():
                envelope = self.fromSocketQueue.get()
                logging.debug("Received envelope from socket with messageId " \
                    +  str(envelope.message.messageId))

                conversationId = str(envelope.message.conversationId)
                if conversationId in self.conversations:
                   self.conversations[conversationId].receivedNewMessage(envelope)
                else:
                   self.__createConversation(envelope, envelopeIsOutgoing=False)
