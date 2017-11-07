import Queue
import ConversationManager
import logging

class CommunicationSubsystem :
    """Application Level Communication Protocol Manager"""
    def __init__(self, myEndpoint = ('localhost', 0)):
        logging.info("Creating communication subsystem with endpoint " + \
            repr(myEndpoint))
        self.fromConversationQueue = Queue.Queue()
        self.conversationManager = ConversationManager.ConversationManager(\
            self.fromConversationQueue, myEndpoint)

    def sendMessage(self, envelope):
        """ Method used by the application to send message """
        logging.info("Sending message to conversation manager " + \
            repr(envelope))
        self.conversationManager.sendMessage(envelope)

    def getMessage(self):
        """ Method used by the application to get a message it (and not the conversation), needs to handle """
        if not self.fromConversationQueue.empty():
            logging.info("Message received for application handling")
            return True, self.fromConversationQueue.get()
        else:
            return False, ""
