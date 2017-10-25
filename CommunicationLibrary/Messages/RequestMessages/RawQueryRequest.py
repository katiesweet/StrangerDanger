#!/usr/bin
from AbstractMessages.Request import Request

class RawQueryRequest(Request):

    def __init__(self, messageId, conversationId, timePeriod, cameras):
        super(RawQueryRequest,self).__init__(messageId, conversationId)
        self.timePeriod = timePeriod
        self.cameras = cameras
