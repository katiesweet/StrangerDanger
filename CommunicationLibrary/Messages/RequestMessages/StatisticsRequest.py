#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class StatisticsRequest(Request):

    def __init__(self, timePeriod, statsType, cameras):
        super(StatisticsRequest, self).__init__()
        self.timePeriod = timePeriod
        self.statsType = statsType
        self.cameras = cameras
