#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class RegisterRequest(Request):

    def __init__(self, identity):
        super(RegisterRequest, self).__init__()
        self.identity = identity
