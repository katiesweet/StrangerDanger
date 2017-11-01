#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class ServerListRequest(Request):

    def __init__(self):
        super(ServerListRequest, self).__init__()
