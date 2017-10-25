#!/usr/bin
from AbstractMessages.Request import Request

class RegisterRequest(Request):

    def __init__(self, messageId, conversationId, identity):
        super(RegisterRequest,self).__init__(messageId, conversationId)
        self.identity = identity
