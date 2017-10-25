#!/usr/bin
from AbstractMessages.Request import Request

class CalcStatisticsRequest(Request):

    def __init__(self, messageId, conversationId, timePeriod, statsType, data):
        super(CalcStatisticsRequest,self).__init__(messageId, conversationId)
        self.timePeriod = timePeriod
        self.statsType = statsType
        self.data = data
