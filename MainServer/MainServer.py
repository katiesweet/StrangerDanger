#!/usr/bin/python
import sys
sys.path.append('../')

from threading import Thread
import time
import scipy.misc

import logging
logging.basicConfig(filename="MainServer.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - Thread: %(thread)d -\
    %(message)s')

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
from CommunicationLibrary.Messages.RequestMessages import * # AliveRequest
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.SharedObjects import *

class MainServer:
    def __init__(self):
        logging.info('Creating Main Server')
        self.comm = CommunicationSubsystem.CommunicationSubsystem()
        self.shouldRun = True
        self.registrationServerAddress = ("34.209.66.116", 50000)
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
        message = Envelope(self.registrationServerAddress, RegisterRequest(ProcessType.ClientProcess))
        self.comm.sendMessage(message)
        logging.debug("Sending message " + repr(message))

    def sendMotionDetectedReply(self, cameraEndpoint, success):
        message = Envelope(cameraEndpoint, MotionDetectedReply(success)
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

    def handleRegisterReply(self, envelope):
        processId = envelope.message.processId
        LocalProcessInfo.setProcessId(processId)
        logging.info('Got ProcessID: {}'.format(processId))
        self.canStartSending = True

    def handleSaveMotionRequest(self, envelope):
        pictureInfo = envelope.message.pictureInfo
        picture = pictureInfo.picture
        timeStamp = pictureInfo.timeStamp
        cameraName = pictureInfo.cameraName
        print 'Saving picture from {} at {}'.format(cameraName, timeStamp)
        scipy.misc.imsave('{}_{}.jpg'.format(cameraName, timeStamp))
        self.sendMotionDetectedReply(envelope.endpoint, True)

if __name__ == '__main__':
    MainServer()
