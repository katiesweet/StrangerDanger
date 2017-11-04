#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class SyncDataRequest(Request):

    def __init__(self, data):
        super(SyncDataRequest, self).__init__()
        self.data = data
