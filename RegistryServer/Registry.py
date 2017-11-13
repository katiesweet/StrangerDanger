import sys
import thread
import threading
import copy
sys.path.append('../') # Start at root directory for all imports

import logging
logging.basicConfig(filename="Registry.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - Thread: %(thread)d -\
    %(message)s')

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *

from CommunicationLibrary.Messages.SharedObjects import *

class Registry:
    nextProcessId = 0
    threadLock = threading.Lock()

    def __init__(self):
        logging.info("Creating registry process")
        myEndpoint = ('', 50000) # Good for both local and external connections
        self.comm = CommunicationSubsystem.CommunicationSubsystem(myEndpoint)
        self.shouldRun = True
        self.knownMainServers = []
        thread.start_new_thread(self.__handleIncomingMessages,())
        var = raw_input("Enter something to quit.\n")
        self.shouldRun = False

    def __handleIncomingMessages(self):
        while self.shouldRun:
            hasMessage, message = self.comm.getMessage()
            if hasMessage:
                self.__processNewMessage(message)

    def __processNewMessage(self, envelope):
        if isinstance(envelope.message, RegisterRequest):
            self.__handleRegisterRequest(envelope)
        elif isinstance(envelope.message, ServerListRequest):
            self.__handleMainServerRequest(envelope)

    def __handleRegisterRequest(self, envelope):
        processType = envelope.message.processType
        if processType == ProcessType.MainServer:
            self.knownMainServers.append(envelope.endpoint)
            print self.knownMainServers

        responseMessage = Envelope(envelope.endpoint, RegisterReply(True, Registry.getNextProcessId()))
        self.comm.sendMessage(responseMessage)

    def __handleMainServerRequest(self, envelope):
        responseMessage = Envelope(envelope.endpoint, ServerListReply(True, copy.deepcopy(self.knownMainServers)))
        self.comm.sendMessage(responseMessage)

    def __handleAliveReponseOfMainServer(self, envelope):
        # TODO: How do we handle this? How do we know when one DOESN'T respond? Probably needs to be addressed in the conversation.
        return

    def __pingMainServersPeriodically(self):
        # TODO: Put lock around the self.knownMainServers array
        return

    @staticmethod
    def getNextProcessId():
        with Registry.threadLock:
            if Registry.nextProcessId == sys.maxint:
                Registry.nextProcessId = 0
            Registry.nextProcessId += 1
        return Registry.nextProcessId

if __name__ == '__main__':
    Registry()
