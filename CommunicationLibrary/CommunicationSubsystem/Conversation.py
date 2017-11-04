# SHOULD BE FACTORY?

import thread

class Conversation:
    def __init__(self, envelope, envelopeIsOutgoing, toSocketQueue, fromConversationQueue):
        self.toSocketQueue = toSocketQueue # Used to send a message
        self.fromConversationQueue = fromConversationQueue # Used to pass a message to the main application

        self.myOutgoingMessageQueue = Queue.Queue()
        self.myIncomingMessageQueue = Queue.Queue()

        if envelopeIsOutgoing:
            self.myOutgoingMessageQueue.put(envelope)
        else:
            self.myIncomingMessageQueue.put(envelope)

        self.shouldRun = True
        thread.startNewThread(self.__run)

    def sendNewMessage(self, envelope):
        """Called from conversation manager for when the application wishes to send a message as a part of the conversation. """
        self.myOutgoingMessageQueue.put(envelope)

    def receivedNewMessage(self, envelope):
        """Called from conversation manager for when a socket receives a message intended for this conversation. """
        self.myIncomingMessageQueue.put(envelope)

    def __run(self):
        while self.shouldRun:
            continue
