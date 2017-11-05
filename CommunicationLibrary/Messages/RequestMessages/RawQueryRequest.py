#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class RawQueryRequest(Request):

    def __init__(self, timePeriod, cameras):
        super(RawQueryRequest, self).__init__()
        self.timePeriod = timePeriod
        self.cameras = cameras
