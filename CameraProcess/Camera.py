#!/usr/bin/python

#############################################
#
# Credit for the motion detection algorithm
# and opencv utils to Adrian Rosebrock
# at www.pyimagesearch.com
#
#############################################

from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
import cv2
import time
from threading import Thread
import sys
sys.path.append('../')

import logging
logging.basicConfig(filename="Camera.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - Thread: %(thread)d -\
    %(message)s')

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
from CommunicationLibrary.Messages.RequestMessages import *
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.SharedObjects import *

class Camera():
    def __init__(self):
        logging.info("Creating camera process")
        self.shouldRun = True
        self.videoStream = PiVideoStream(resolution=(480,320))
        self.comm = CommunicationSubsystem.CommunicationSubsystem()
        self.registrationServerAddress = ("192.168.0.5", 50000)
        #self.registrationServerAddress = ("34.209.72.192", 50000)
        self.mainServerAddress = (None, None)
        self.canStartSending = False

        self.sendRegisterRequest()
        Thread(target=self.checkForMessagesPeriodically,args=()).start()
        Thread(target=self.runVideoStream,args=()).start()
        while self.shouldRun:
            pass

    def sendRegisterRequest(self):
        message = Envelope(self.registrationServerAddress, RegisterRequest(ProcessType.CameraProcess))
        self.comm.sendMessage(message)
        logging.debug("Sending Register Request message " + repr(message))

    def sendSaveMotionRequest(self, endpoint, frame):
        message = Envelope(endpoint, SaveMotionRequest(frame))
        self.comm.sendMessage(message)
        logging.debug("Sending Save Motion Request message " + repr(message))

    def runVideoStream(self):
        self.videoStream.start()
        time.sleep(2.0)
        self.previousFrame = None

        while self.shouldRun:
            frame = self.videoStream.read()
            processedFrame = self.processFrame(frame)
            cv2.imshow("Video Stream", processedFrame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                self.videoStream.stop()
                self.shouldRun = False

        cv2.destroyAllWindows()


    def processFrame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if not self.previousFrame is None:
            pass

        self.previousFrame = gray
        return gray        


    def checkForMessagesPeriodically(self):
        while self.shouldRun:
            try:
                haveMessage, envelope = self.comm.getMessage()
                if haveMessage:
                    logging.info('Handling new message')
                    self.processNewMessage(envelope)
            except:
                pass

    def processNewMessage(self, envelope):
        if isinstance(envelope.message, RegisterReply):
            logging.info('Handling Register Reply')
            self.handleRegisterReply(envelope)

    def handleRegisterReply(self, envelope):
        processId = envelope.message.processId

        LocalProcessInfo.setProcessId(processId)
        logging.info('Received ProcessID: {}'.format(LocalProcessInfo.getProcessId()))
        self.canStartSending = True
            


if __name__ == '__main__':
    Camera()
