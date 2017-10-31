#!/usr/bin
from AbstractMessages.Request import Request


class CalcStatisticsRequest(Request):

    def __init__(self, timePeriod, statsType, data):
        super(CalcStatisticsRequest, self).__init__()
        self.timePeriod = timePeriod
        self.statsType = statsType
        self.data = data
