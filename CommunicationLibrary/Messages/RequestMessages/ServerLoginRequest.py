#!/usr/bin
from LoginRequest import LoginRequest

class ServerLoginRequest(LoginRequest):

    def __init__(self, messageId, conversationId, processType, processLabel, identity):
        super(ServerLoginRequest,self).__init__(messageId, conversationId, processType, processLabel, identity)
