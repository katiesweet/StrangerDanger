import sys
import threading
sys.path.append('../') # Start at root directory for all imports

import logging
logging.basicConfig(filename="Registry.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - Thread: %(thread)d -\
    %(message)s')

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.SharedObjects.Envelope import Envelope

class Registry:
    nextProcessId = 0
    threadLock = threading.Lock()

    def __init__(self):
        logging.info("Creating registry process")
        myEndpoint = ('localhost', 50000)
        self.comm = CommunicationSubsystem.CommunicationSubsystem(myEndpoint)
        self.shouldRun = True
        self.__handleIncomingMessages()
        var = raw_input("Enter something to quit.\n")


    def __handleIncomingMessages(self):
        while self.shouldRun:
            hasMessage, message = self.comm.getMessage()
            if hasMessage:
                message = Envelope(message.endpoint, RegisterReply(True, Registry.getNextProcessId()))
                self.comm.sendMessage(message)
                self.shouldRun = False

    @staticmethod
    def getNextProcessId():
        with Registry.threadLock:
            if Registry.nextProcessId == sys.maxint:
                Registry.nextProcessId = 0
            Registry.nextProcessId += 1
        return Registry.nextProcessId

if __name__ == '__main__':
    Registry()
