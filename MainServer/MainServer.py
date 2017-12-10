#!/usr/bin/python
import sys
sys.path.append('../')

from threading import Thread
import time
import scipy.misc
import json
import logging
logging.basicConfig(filename="MainServer.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - Thread: %(thread)d -\
    %(message)s')
import cv2
import datetime
import Queue

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
from CommunicationLibrary.Messages.RequestMessages import * # AliveRequest
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.SharedObjects import *

class MainServer:
    def __init__(self):
        logging.info('Creating Main Server')
        self.comm = CommunicationSubsystem.CommunicationSubsystem()
        self.shouldRun = True
        self.databaseFile = "PhotoDatabase.json"
        self.registrationServerAddress = ("54.71.0.209", 52000)
        #self.registrationServerAddress = ("192.168.0.16", 52000)
        #self.registrationServerAddress = ("localhost", 52000)
        self.statisticsServerAddress = ("localhost", 52500)
        self.canStartSending = False
        self.sendRegisterRequest()
        self.picturesNeededToGet = Queue.Queue()
        self.currentRequestedPicture = None
        t1 = Thread(target=self.__handleIncomingMessages,args=())
        t2 = Thread(target=self.__handleInput,args=())
        t3 = Thread(target=self.__syncPeriodically,args=())
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()

    def __handleInput(self):
        var = raw_input("Enter something to quit.\n")
        self.shouldRun = False

    def __syncPeriodically(self):
        previousPingTime = datetime.datetime.now()
        while self.shouldRun:
            newTime = datetime.datetime.now()

            # if we haven't pinged in over an hour
            if newTime > previousPingTime + datetime.timedelta(seconds=60):
            #if newTime > previousPingTime + datetime.timedelta(seconds=60):
                previousPingTime = newTime
                self.__startSyncProtocol()

            # Sleep for a minute
            #time.sleep(60)
            time.sleep(5)

    def __startSyncProtocol(self):
        # Request list of other main servers from registry
        envelope = Envelope(self.registrationServerAddress, ServerListRequest(ProcessType.MainServer))
        logging.debug("Requesting other main servers")
        self.comm.sendMessage(envelope)

    def handleServerListReply(self, envelope):
        mainServers = envelope.message.servers
        with open(self.databaseFile, "r") as database:
            data = json.load(database)

        for server in mainServers:
            print "Syncing with server ", server
            envelope = Envelope(server, SyncDataRequest(data))
            self.comm.sendMessage(envelope)

    def handleSyncDataRequest(self, envelope):
        theirData = envelope.message.data["pictures"]

        # Respond to them
        msg = SyncDataReply(True)
        msg.setConversationId(envelope.message.conversationId)
        outEnv = Envelope(envelope.endpoint, msg)
        self.comm.sendMessage(outEnv)

        # Get my data
        with open(self.databaseFile, "r") as database:
            myData = json.load(database)["pictures"]

        # Put all the items in their dictionary and not in mine on the queue
        for theirCam in theirData:
            inMyDict = False
            for myCam in myData:
                if theirCam == myCam:
                    inMyDict = True
                    break
            if not inMyDict:
                self.picturesNeededToGet.put((envelope.endpoint, theirCam))

        self.getPictureFromQueue()

    def getPictureFromQueue(self):
        if not self.picturesNeededToGet.empty():
            try:
                endpoint, self.currentRequestedPicture = self.picturesNeededToGet.get(False)
            except:
                return
            picLocation = self.currentRequestedPicture["picLocation"]
            envelope = Envelope(endpoint, GetPictureRequest(picLocation))
            self.comm.sendMessage(envelope)

    def handleGetPictureReply(self, envelope):
        picInfo = self.currentRequestedPicture
        picture = envelope.message.picture
        # Save picture
        scipy.misc.imsave(picInfo["picLocation"], picture)
        self.writeDatabaseEntry(picInfo["camName"], picInfo["timeStamp"], picInfo["picLocation"])

        # Request next picture
        self.getPictureFromQueue()

    def sendRegisterRequest(self):
        message = Envelope(self.registrationServerAddress, RegisterRequest(ProcessType.MainServer))
        self.comm.sendMessage(message)
        logging.debug("Sending message " + repr(message))

    def sendMotionDetectedReply(self, cameraEndpoint, success, convoId):
        reply = MotionDetectedReply(success)
        reply.setConversationId(convoId)
        message = Envelope(cameraEndpoint, reply)
        self.comm.sendMessage(message)
        logging.debug("Sending MotionDetectedReply message " + repr(message))

    def __handleIncomingMessages(self):
        while self.shouldRun:
            hasMessage, message = self.comm.getMessage()
            if hasMessage:
                self.__processNewMessage(message)

    def __processNewMessage(self, envelope):
        if isinstance(envelope.message, RegisterReply):
            self.handleRegisterReply(envelope)
        elif isinstance(envelope.message, SaveMotionRequest):
            self.handleSaveMotionRequest(envelope)
    	elif isinstance(envelope.message, SaveCombinedPictureRequest):
    	    self.handleSaveMotionRequest(envelope)
        elif isinstance(envelope.message, RawQueryRequest):
            self.handleRawQueryRequest(envelope)
        elif isinstance(envelope.message, GetPictureRequest):
            self.handleGetPictureRequest(envelope)
        elif isinstance(envelope.message, StatisticsRequest):
            self.handleStatisticsRequest(envelope)
        elif isinstance(envelope.message, ServerListReply):
            self.handleServerListReply(envelope)
        elif isinstance(envelope.message, SyncDataRequest):
            self.handleSyncDataRequest(envelope)
        elif isinstance(envelope.message, GetPictureReply):
            self.handleGetPictureReply(envelope)

    def handleRegisterReply(self, envelope):
        processId = envelope.message.processId
        LocalProcessInfo.setProcessId(processId)
        print 'Got ProcessID: {}'.format(processId)
        logging.info('Got ProcessID: {}'.format(processId))
        self.canStartSending = True

    def writeDatabaseEntry(self, cameraName, timestamp, photoStorageLocation):
        with open(self.databaseFile, "r") as database:
            data = json.load(database)
        jsonObject = {"camName" : cameraName, "timeStamp" : str(timestamp), "picLocation" : photoStorageLocation}
        data["pictures"].append(jsonObject)
        with open(self.databaseFile, "w") as database:
            json.dump(data, database)

    def handleSaveMotionRequest(self, envelope):
        pictureInfo = envelope.message.pictureInfo
        convoId = envelope.message.conversationId
        picture = pictureInfo.picture
        timeStamp = pictureInfo.timeStamp
        cameraName = pictureInfo.cameraName

        rawFileName = '{}_{}'.format(cameraName, timeStamp)
        rawFileName = rawFileName.replace(" ", "_")
        rawFileName = rawFileName.replace(".", ":")
        photoStorageLocation = 'PhotoDatabase/{}.jpg'.format(rawFileName)
        print 'Saving picture from {} at {}'.format(cameraName, timeStamp)
        scipy.misc.imsave(photoStorageLocation, picture)
        self.writeDatabaseEntry(cameraName, timeStamp, photoStorageLocation)
        self.sendMotionDetectedReply(envelope.endpoint, True, convoId)

    def handleRawQueryRequest(self, envelope):
        with open(self.databaseFile, "r") as database:
            camData = json.load(database)["pictures"]
        if envelope.message.mostRecent:
            self.handleMostRecentDataRequest(envelope, camData)
        else:
            self.handleDataRangeRequest(envelope, camData)

    def handleMostRecentDataRequest(self, envelope, camData):
        #print "Handling most recent request"
        validCams = envelope.message.cameras
        mostRecentTime = None

        responseData = []
        mostRecentEntry = None
        for data in camData:
            if data["camName"] in validCams:
                time = datetime.datetime.strptime(data["timeStamp"], "%Y-%m-%d %H:%M:%S.%f")
                if not mostRecentTime or time > mostRecentTime:
                    mostRecentTime = time
                    mostRecentEntry = data
        responseData.append(mostRecentEntry)
        msg = RawQueryReply(True, responseData)
        msg.setConversationId(envelope.message.conversationId)
        self.comm.sendMessage(Envelope(envelope.endpoint, msg))

    def handleDataRangeRequest(self, envelope, camData):
        validCams = envelope.message.cameras
        timePeriod = envelope.message.timePeriod
        startTime = datetime.datetime.strptime(timePeriod.startDate, "%Y-%m-%d %H:%M:%S")
        endTime = datetime.datetime.strptime(timePeriod.endDate, "%Y-%m-%d %H:%M:%S")

        responseData = []
        for data in camData:
            if data["camName"] in validCams:
                time = datetime.datetime.strptime(data["timeStamp"], "%Y-%m-%d %H:%M:%S.%f")
                if startTime <= time and time <= endTime:
                    responseData.append(data)

        msg = RawQueryReply(True, responseData)
        msg.setConversationId(envelope.message.conversationId)
        self.comm.sendMessage(Envelope(envelope.endpoint, msg))

    def handleGetPictureRequest(self, envelope):
        picLocation = envelope.message.picLocation
        img = cv2.imread(picLocation, 0)
        msg = GetPictureReply(True, img)
        msg.setConversationId(envelope.message.conversationId)
        self.comm.sendMessage(Envelope(envelope.endpoint, msg))

    def getDataForCameras(self, validCams):
        with open(self.databaseFile, "r") as database:
            camData = json.load(database)["pictures"]

        filteredCameras = []
        for data in camData:
            if data["camName"] in validCams:
                filteredCameras.append(data)

        return filteredCameras

    def handleStatisticsRequest(self, envelope):
        timePeriod = envelope.message.timePeriod
        statsType = envelope.message.statsType
        cameras = envelope.message.cameras
        data = self.getDataForCameras(cameras)
        clientEndpoint = envelope.endpoint

        msg = CalcStatisticsRequest(timePeriod, statsType, data, clientEndpoint)
        msg.setConversationId(envelope.message.conversationId)
        self.comm.sendMessage(Envelope(self.statisticsServerAddress, msg))


if __name__ == '__main__':
    MainServer()
