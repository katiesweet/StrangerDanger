import sys
from threading import Thread
import datetime
import copy
import time
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
        #myEndpoint = ('', 50000) # Good for both local and external connections
        myEndpoint = ('localhost', 50003)

        self.communicationsLock = threading.Lock()
        self.comm = CommunicationSubsystem.CommunicationSubsystem(myEndpoint)

        self.mainServerLock = threading.Lock()
        self.knownMainServers = {}

        self.shouldRun = True
        t1 = Thread(target=self.__handleIncomingMessages,args=())
        t2 = Thread(target=self.__handleInput,args=())
        t3 = Thread(target=self.__pingMainServersPeriodically, args=())
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()

    def __handleInput(self):
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
        elif isinstance(envelope.message, AliveReply):
            self.__handleAliveReponseOfMainServer(envelope)
        #elif isinstance(envelope.message, )

    def __handleRegisterRequest(self, envelope):
        processType = envelope.message.processType
        if processType == ProcessType.MainServer:
            with self.mainServerLock:
                self.knownMainServers[envelope.endpoint] = True

        responseMessage = RegisterReply(True, Registry.getNextProcessId())
        responseMessage.setConversationId(envelope.message.conversationId)

        outEnv = Envelope(envelope.endpoint, responseMessage)
        with self.communicationsLock:
            self.comm.sendMessage(outEnv)

    def __getArrayOfMainServers(self):
        with self.mainServerLock:
            knownServers = copy.deepcopy(self.knownMainServers)

        arrayServers = []
        for endpoint in knownServers:
            if knownServers[endpoint] == True:
                arrayServers.append(endpoint)
        return arrayServers

    def __handleMainServerRequest(self, envelope):
        knownMainServers = self.__getArrayOfMainServers()
        responseMessage = ServerListReply(True, knownMainServers)
        responseMessage.setConversationId(envelope.message.conversationId)
        outEnv = Envelope(envelope.endpoint, responseMessage)
        with self.communicationsLock:
            self.comm.sendMessage(outEnv)

    def __handleAliveReponseOfMainServer(self, envelope):
        with self.mainServerLock:
            self.knownMainServers[envelope.endpoint] = True

    def __pingMainServersPeriodically(self):
        previousPingTime = datetime.datetime.now()
        while self.shouldRun:
            newTime = datetime.datetime.now()
            # if we haven't pinged in over 10 minutes
            if newTime > previousPingTime + datetime.timedelta(seconds=600):
                previousPingTime = newTime
                self.__pingMainServers()

            # Sleep for 5 seconds
            time.sleep(5)

    def __pingMainServers(self):
        messagesToSend = []

        with self.mainServerLock:
            for endpoint, isAlive in self.knownMainServers.items():
                if not isAlive:
                    # Purge all servers that didn't respond since last ping
                    self.knownMainServers.pop(endpoint)
                else:
                    # Create messages to send to servers that were alive
                    self.knownMainServers[endpoint] = False
                    messagesToSend.append(Envelope(endpoint, AliveRequest()))

        with self.communicationsLock:
            for message in messagesToSend:
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
