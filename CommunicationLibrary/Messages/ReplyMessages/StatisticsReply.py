#!/usr/bin
from AbstractMessages.Reply import Reply

class StatisticsReply(Reply):

    def __init__(self, messageId, conversationId, success, report):
        super(StatisticsReply,self).__init__(messageId, conversationId, success)
        self.report = report
