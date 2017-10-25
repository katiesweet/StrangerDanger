#!/usr/bin
from AbstractMessages.Request import Request

class SubscribeRequest(Request):

    def __init__(self, messageId, conversationId, clusterId):
        super(SubscribeRequest,self).__init__(messagedId, conversationId)
        self.clusterId = clusterId
