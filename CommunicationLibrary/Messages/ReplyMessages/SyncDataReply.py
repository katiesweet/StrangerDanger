#!/usr/bin
from AbstractMessages.Reply import Reply

class SyncDataReply(Reply):

    def __init__(self, messageId, conversationId, success):
        super(SyncDataReply,self).__init__(messageId, conversationId, success)
