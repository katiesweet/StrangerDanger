#!/usr/bin
from AbstractMessages.Reply import Reply


class StatisticsReply(Reply):

    def __init__(self, success, report):
        super(StatisticsReply, self).__init__(success)
        self.report = report
