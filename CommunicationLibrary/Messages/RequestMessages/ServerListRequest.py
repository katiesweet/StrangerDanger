#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class ServerListRequest(Request):

    def __init__(self, processType):
        super(ServerListRequest, self).__init__()
        self.processType = processType
