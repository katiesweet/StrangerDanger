import SocketManager
import Conversation

class ConversationManager:
    """Conversation Level Communication Protocol Manager"""
    def __init__(self, toCommunicatorQueue):

        # Queues used directly by Conversations
        self.fromConversationQueue = fromConversationQueue
        self.toSocketQueue = Queue()

        # Queues used by sockets to return decoded messages
        self.fromSocketQueue = Queue()

        # Socket Manager
        self.socketManager = SocketManager.SocketManager(self.toSocketQueue, self.fromSocketQueue)

        # Conversation Id: Conversation
        self.conversations = {}

        # Thread management
        self.shouldRun = True
        thread.startNewThread(self.__run)

    def __del__(self):
        self.shouldRun = False

    def sendMessage(self, envelope):
        """Called by Communication Protocol when the application layer wants to send a new message."""
        if envelope.conversationId in converations:
            conversation[convoId].sendNewMessage(envelope)
        else:
            self.__createConveration(envelope)

    def __createConversation(self, envelope, envelopeIsOutgoing):
        """Creates a conversation and appends it to the class' known conversations. The Conversation.Conversation() constructor should be a factory that returns the appropriate conversation type. The constructor also handles sending the first message automatically."""
        convoId = envelope.conversationId
        conversations[convoId] = Conversation.Conversation(envelope, envelopeIsOutgoing, self.toSocketQueue, self.fromConversationQueue)

    def __run():
        while self.shouldRun:
            if not self.fromSocketQueue.empty():
                envelope = self.fromSocketQueue.get()
                conversationId = envelope.message.conversationId

                if conversationId in self.conversations:
                    self.conversations[newMessageId].receivedNewMessage(envelope)
                else:
                    self.__createConveration(envelope)
