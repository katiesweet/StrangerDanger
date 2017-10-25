#!/usr/bin
from LoginRequest import LoginRequest

class ClientLoginRequest(LoginRequest):

    def __init__(self, messageId, conversationId, processType, processLabel, identity, username, password):
        super(ClientLoginRequest,self).__init__(messageId, conversationId, processType, processLabel, identity)
        self.username = username
        self.password = password
