import Queue
import Conversation
import UdpConnection
import thread

class ConversationManager:
    """Conversation Level Communication Protocol Manager"""
    def __init__(self, fromConversationQueue):

        self.fromConversationQueue = fromConversationQueue # Messages for app
        self.toSocketQueue = Queue.Queue() # Messages to be sent by socket
        self.fromSocketQueue = Queue.Queue() # Messages received by socket

        self.udpSocket = UdpConnection.UdpConnection(self.toSocketQueue, self.fromSocketQueue)

        # Conversation Id: Conversation
        self.conversations = {}

        # Thread management
        self.shouldRun = True
        thread.start_new_thread(self.__run, ())

    def __del__(self):
        self.shouldRun = False

    def sendMessage(self, envelope):
        """Called by Communication Protocol when the application layer wants to send a new message."""
        self.toSocketQueue.put(envelope)
        # if envelope.conversationId in converations:
        #     conversation[convoId].sendNewMessage(envelope)
        # else:
        #     self.__createConveration(envelope, envelopeIsOutgoing=True)

    def __createConversation(self, envelope, envelopeIsOutgoing):
        """Creates a conversation and appends it to the class' known conversations. The Conversation.Conversation() constructor should be a factory that returns the appropriate conversation type. The constructor also handles sending the first message automatically."""
        convoId = envelope.conversationId
        conversations[convoId] = Conversation.Conversation(envelope, envelopeIsOutgoing, self.toSocketQueue, self.fromConversationQueue)

    def __run(self):
        while self.shouldRun:
            if not self.fromSocketQueue.empty():
                print "Received envelope"
                envelope = self.fromSocketQueue.get()
                print "Message Id:", envelope.message.messageId

                #conversationId = envelope.message.conversationId
                #if conversationId in self.conversations:
                #    self.conversations[newMessageId].receivedNewMessage(envelope)
                #else:
                #    self.__createConveration(envelope, envelopeIsOutgoing=False)
