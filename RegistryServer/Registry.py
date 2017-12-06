import sys
from threading import Thread
import datetime
import copy
import time
import json
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

    def __init__(self):
        logging.info("Creating registry process")
        myEndpoint = ('', 52312) # Good for both local and external connections

        self.communicationsLock = threading.Lock()
        self.comm = CommunicationSubsystem.CommunicationSubsystem(myEndpoint)

        self.databaseFile = "RegistryDatabase.json"
        self.databaseLock = threading.Lock()

        self.mainServerLock = threading.Lock()
        self.knownMainServers = self.__loadMainServers()
        #self.knownMainServers = {}

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
        msg = envelope.message
        logging.info("Received new message "+ str(msg.messageId) + " " + str(msg.conversationId))
        if isinstance(msg, RegisterRequest):
            self.__handleRegisterRequest(envelope)
        elif isinstance(msg, ServerListRequest):
            self.__handleProcessListRequest(envelope)
        elif isinstance(msg, AliveReply):
            self.__handleAliveReponseOfMainServer(envelope)

    def __handleRegisterRequest(self, envelope):
        processType = envelope.message.processType
        if processType == ProcessType.MainServer:
            with self.mainServerLock:
                self.knownMainServers[envelope.endpoint] = True
        elif processType == ProcessType.CameraProcess:
            self.__addCameraName(envelope.message.name)

        responseMessage = RegisterReply(True, self.__getNextProcessId())
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

    def __handleProcessListRequest(self, envelope):
        if envelope.message.processType == ProcessType.MainServer:
            self.__handleMainServerRequest(envelope)
        elif envelope.message.processType == ProcessType.CameraProcess:
            self.__handleCameraListRequest(envelope)

    def __handleMainServerRequest(self, envelope):
        knownMainServers = self.__getArrayOfMainServers()
        responseMessage = ServerListReply(True, ProcessType.MainServer, knownMainServers)
        responseMessage.setConversationId(envelope.message.conversationId)
        outEnv = Envelope(envelope.endpoint, responseMessage)
        with self.communicationsLock:
            self.comm.sendMessage(outEnv)

    def __handleCameraListRequest(self, envelope):
        knownCams = self.__getCameraNames()

        responseMessage = ServerListReply(True, ProcessType.CameraProcess, knownCams)
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
            if newTime > previousPingTime + datetime.timedelta(seconds=10):
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
            self.__updateMainServers()

        with self.communicationsLock:
            for envelope in messagesToSend:
                self.comm.sendMessage(envelope)

    def __getNextProcessId(self):
        with self.databaseLock:
            with open(self.databaseFile, "r") as database:
                data = json.load(database)

            nextProcessId = data["nextProcessId"]
            if nextProcessId == sys.maxint:
                data["nextProcessId"] = 0
            data["nextProcessId"] += 1

            with open(self.databaseFile, "w") as database:
                json.dump(data, database)

            return nextProcessId

    def __getCameraNames(self):
        with self.databaseLock:
            with open(self.databaseFile) as database:
                data = json.load(database)
                return data["cameraNames"]

    def __addCameraName(self, name):
        with self.databaseLock:
            with open(self.databaseFile, "r") as database:
                data = json.load(database)

            if not name in data["cameraNames"]:
                data["cameraNames"].append(name)

            with open(self.databaseFile, "w") as database:
                json.dump(data, database)

    def __updateMainServers(self):
        with self.databaseLock:
            with open(self.databaseFile, "r") as database:
                data = json.load(database)

            data["knownMainServers"] = []
            for endpoint in self.knownMainServers:
                data["knownMainServers"].append(endpoint)

            with open(self.databaseFile, "w") as database:
                json.dump(data, database)

    def __loadMainServers(self):
        with self.databaseLock:
            with open(self.databaseFile, "r") as database:
                data = json.load(database)

            servers = {}
            for server in data["knownMainServers"]:
                servers[(server[0], server[1])] = True

            return servers


if __name__ == '__main__':
    Registry()
