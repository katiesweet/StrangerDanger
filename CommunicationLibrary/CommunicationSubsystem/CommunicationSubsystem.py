import Queue
import ConversationManager

class CommunicationSubsystem :
    """Application Level Communication Protocol Manager"""
    def __init__(self):
        self.fromConversationQueue = Queue()
        self.conversationManager = ConversationManager.ConversationManager(fromConversationQueue)

    def sendMessage(self, envelope):
        """ Method used by the application to send message """
        self.conversationManager.sendMessage(envelope)

    def getMessage(self, envelope):
        """ Method used by the application to get a message it (and not the conversation), needs to handle """
        if not self.fromConversationQueue.empty():
            return True, self.fromConversationQueue.get()
        else:
            return False, ""
