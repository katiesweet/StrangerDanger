#!/usr/bin
from AbstractMessages.Reply import Reply

class RawQueryReply(Reply):

    def __init__(self, messageId, conversationId, success, data):
        super(RawQueryReply,self).__init__(messageId, conversationId, success)
        self.data = data
