#!/usr/bin/python
import sys
sys.path.append('../')

from threading import Thread
import time

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
        self.registrationServerAddress = ("34.209.66.116", 50000)
        self.canStartSending = False
        self.sendRegisterRequest()
        t1 = Thread(target=self.__handleIncomingMessages,args=())
        t1.start()
        t1.join()

    def sendRegisterRequest(self):
        message = Envelope(self.registrationServerAddress, RegisterRequest(ProcessType.ClientProcess))
        self.comm.sendMessage(message)
        logging.debug("Sending message " + repr(message))

    def __handleIncomingMessages(self):
        while True:
            hasMessage, message = self.comm.getMessage()
            if hasMessage:
                self.__processNewMessage(message)
            else:
                time.sleep(0.1)

    def __processNewMessage(self, envelope):
        if isinstance(envelope.message, RegisterReply):
            self.handleRegisterReply(envelope)

    def handleRegisterReply(self, envelope):
        processId = envelope.message.processId
        LocalProcessInfo.setProcessId(processId)
        logging.info('Got ProcessID: {}'.format(processId))
        self.canStartSending = True

if __name__ == '__main__':
    MainServer()
