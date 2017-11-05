#!/usr/bin/python
from LoginRequest import LoginRequest


class ClientLoginRequest(LoginRequest):

    def __init__(self, processType, processLabel, identity, username, password):
        super(ClientLoginRequest, self).__init__(processType, processLabel, identity)
        self.username = username
        self.password = password
