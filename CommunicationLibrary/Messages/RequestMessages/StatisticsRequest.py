#!/usr/bin
from AbstractMessages.Request import Request

class StatisticsRequest(Request):

    def __init__(self, messageId, conversationId, timePeriod, statsType, cameras):
        super(StatisticsRequest,self).__init__(messageId, conversationId)
        self.timePeriod = timePeriod
        self.statsType = statsType
        self.cameras = cameras
