#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class RawQueryRequest(Request):

    def __init__(self, mostRecent, timePeriod, cameras):
        super(RawQueryRequest, self).__init__()
        self.mostRecent = mostRecent # T/F
        self.timePeriod = timePeriod
        self.cameras = cameras
