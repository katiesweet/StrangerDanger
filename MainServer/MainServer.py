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
        #self.registrationServerAddress = ("34.209.66.116", 50000)
        #self.registrationServerAddress = ("144.39.254.27", 50000)
        #self.registrationServerAddress = ("192.168.0.23", 50000)
        self.registrationServerAddress = ("localhost", 52312)
        self.canStartSending = False
        self.sendRegisterRequest()
        t1 = Thread(target=self.__handleIncomingMessages,args=())
        t2 = Thread(target=self.__handleInput,args=())
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def __handleInput(self):
        var = raw_input("Enter something to quit.\n")
        self.shouldRun = False

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

    def handleRegisterReply(self, envelope):
        processId = envelope.message.processId
        LocalProcessInfo.setProcessId(processId)
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

        img = cv2.imread(picLocation)
        msg = GetPictureReply(True, img)
        msg.setConversationId(envelope.message.conversationId)
        self.comm.sendMessage(Envelope(envelope.endpoint, msg))

if __name__ == '__main__':
    MainServer()
