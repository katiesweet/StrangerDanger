#!/usr/bin
from AbstractMessages.Request import Request

class LoginRequest(Request):

    def __init__(self, messageId, conversationId, processType, processLabel, identity):
        super(LoginRequest,self).__init__(messageId, conversationId)
        self.processType = processType
        self.processLabel = processLabel
        self.identity = identity
