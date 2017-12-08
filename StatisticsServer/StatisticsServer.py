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
from datetime import datetime, timedelta

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
from CommunicationLibrary.Messages.RequestMessages import *
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.SharedObjects import *


class StatisticsServer:
    def __init__(self):
        logging.info('Creating Statistics Server')
        myEndpoint = ('', 52500) # Good for both local and external connections
        self.comm = CommunicationSubsystem.CommunicationSubsystem(myEndpoint)
        self.shouldRun = True

        #self.registrationServerAddress = ("192.168.0.23", 50000)
        self.registrationServerAddress = ("localhost", 52000)
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
        message = Envelope(self.registrationServerAddress, RegisterRequest(ProcessType.StatisticsServer))
        self.comm.sendMessage(message)
        logging.debug("Sending message " + repr(message))

    def __handleIncomingMessages(self):
        while self.shouldRun:
            hasMessage, message = self.comm.getMessage()
            if hasMessage:
                logging.debug("Received new message")
                self.__processNewMessage(message)

    def __processNewMessage(self, envelope):
        if isinstance(envelope.message, CalcStatisticsRequest):
            logging.debug("Handling CalcStatisticsRequest message")
            self.handleCalcStatisticsRequest(envelope)

    def handleCalcStatisticsRequest(self, envelope):
        data = self.filterData(envelope.message.data, envelope.message.timePeriod)
        stat_type = envelope.message.statsType
        statisticsReport = {}
        if 'hourly' in stat_type:
            logging.debug("Generating hourly report")
            statisticsReport['hourly'] = self.calculateHourly(data)
        if 'daily' in stat_type:
            logging.debug("Generating daily report")
            statisticsReport['daily'] = self.calculateDaily(data)
        if statisticsReport:
            logging.info("Sending Statistics Reply with report")
            endpoint = envelope.message.clientEndpoint
            message = StatisticsReply(success=True, report=statisticsReport)
            message.setConversationId(envelope.message.conversationId)
            out_envelope = Envelope(message=message, endpoint=endpoint)
            self.comm.sendMessage(out_envelope)

    def filterData(self, data, timePeriod):
        start = datetime.strptime(timePeriod.startDate, '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(timePeriod.endDate, '%Y-%m-%d %H:%M:%S')
        filteredData = []
        for d in data:
            date = d['timeStamp']
            date = datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S.%f')
            if date >= start and date <= end:
                filteredData.append(date)
        return filteredData

    def calculateHourly(self, data):
        # counts the sum of visits per hour
        # returns dictionary of { dayZ_hourA: count of dayZ_hourA, dayY_hourB: counts of dayY_hourB, ...}
        recordedHours = {}
        for d in data:
            key = datetime.strftime(d,'%Y-%m-%d %H')
            if key in recordedHours:
                recordedHours[key] += 1
            else:
                recordedHours[key] = 1
        return recordedHours

    def calculateDaily(self, data):
        # counts the sum of visits per day
        # returns dictionary of { monthZ_dayA: count of monthZ_dayA, monthY_dayB: counts of monthY_dayB, ...}
        recordedDays = {}
        for d in data:
            key = datetime.strftime(d,'%Y-%m-%d')
            if key in recordedDays:
                recordedDays[key] += 1
            else:
                recordedDays[key] = 1
        return recordedDays


if __name__ == '__main__':
    StatisticsServer()
