#!/usr/bin/python
import sys
sys.path.append('../')

from threading import Thread
import time
import json
import logging
logging.basicConfig(filename="StatisticsServer.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - Thread: %(thread)d -\
    %(message)s')
import datetime

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
from CommunicationLibrary.Messages.RequestMessages import *
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.SharedObjects import *


class Statistics Server:
    def __init__(self):
        logging.info('Creating Statistics Server')
        self.comm = CommunicationSubsystem.CommunicationSubsystem()
        self.shouldRun = True

        self.registrationServerAddress = ("192.168.0.23", 50000)
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

    def __handleIncomingMessages(self):
        while self.shouldRun:
            hasMessage, message = self.comm.getMessage()
            if hasMessage:
                self.__processNewMessage(message)

    def __processNewMessage(self, envelope):
        if isinstance(envelope.message, CalcStatisticsRequest):
            self.handleCalcStatisticsRequest(envelope)

    def handleCalcStatisticsRequest(self, envelope):
        data = self.filterData(envelope.message.data, envelope.message.timePeriod)
        stat_type = envelope.message.statsType
        statisticsReport = None
        if stat_type == 'hourly':
            statisticsReport = self.calculateHourly(data)
        if stat_type == 'daily':
            statisticsReport = self.calculateDaily(data)
        if statisticsReport:
            endpoint = envelope.message.clientEndPoint
            message = StatisticsReply(report=statisticsReport)
            envelope = Envelope(endpoint=endpoint, message=message)


    def calculateHourly(self):
        pass

    def calculateDaily(self):
        pass

if __name__ == '__main__':
    StatisticsServer()
