#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class RawQueryRequest(Request):

    def __init__(self, mostRecent, startDate, endDate, cameras):
        super(RawQueryRequest, self).__init__()
        self.mostRecent = mostRecent # T/F
        self.startDate = startDate
        self.endDate = endDate
        self.cameras = cameras
