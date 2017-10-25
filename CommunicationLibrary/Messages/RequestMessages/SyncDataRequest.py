#!/usr/bin
from AbstractMessages.Request import Request

class SyncDataRequest(Request):

    def __init__(self, messageId, conversationId, data):
        super(SyncDataRequest,self).__init__(messageId, conversationId)
        self.data = data
