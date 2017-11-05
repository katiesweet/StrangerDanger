#!/usr/bin/python
from LoginRequest import LoginRequest


class ServerLoginRequest(LoginRequest):

    def __init__(self, processType, processLabel, identity):
        super(ServerLoginRequest, self).__init__(processType, processLabel, identity)
