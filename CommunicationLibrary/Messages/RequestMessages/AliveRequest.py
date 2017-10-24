#!/usr/bin
from AbstractMessages.Request import Request

class AliveRequest(Request):

    def __init__(self, messageId, conversationId):
        super(AliveRequest,self).__init__(messageId, conversationId)
