#!/usr/bin
from AbstractMessages.Request import Request

class ServerListRequest(Request):

    def __init__(self, messageId, conversationId):
        super(ServerListRequest,self).__init__(messageId, conversationId)
