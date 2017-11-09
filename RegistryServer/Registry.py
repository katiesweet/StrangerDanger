import sys
import thread
import threading
sys.path.append('../') # Start at root directory for all imports

import logging
logging.basicConfig(filename="Registry.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - Thread: %(thread)d -\
    %(message)s')

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *

from CommunicationLibrary.Messages.SharedObjects.Envelope import Envelope

class Registry:
    nextProcessId = 0
    threadLock = threading.Lock()

    def __init__(self):
        logging.info("Creating registry process")
        myEndpoint = ('', 50000)
        self.comm = CommunicationSubsystem.CommunicationSubsystem(myEndpoint)
        self.shouldRun = True
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
            self.__sendRegisterResponseMessage(envelope)

    def __sendRegisterResponseMessage(self, envelope):
        message = Envelope(envelope.endpoint, RegisterReply(True, Registry.getNextProcessId()))
        self.comm.sendMessage(message)

    @staticmethod
    def getNextProcessId():
        with Registry.threadLock:
            if Registry.nextProcessId == sys.maxint:
                Registry.nextProcessId = 0
            Registry.nextProcessId += 1
        return Registry.nextProcessId

if __name__ == '__main__':
    Registry()
