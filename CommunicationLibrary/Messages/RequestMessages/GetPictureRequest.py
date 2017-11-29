#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class GetPictureRequest(Request):

    def __init__(self, camName, timeStamp):
        super(GetPictureRequest, self).__init__()
        self.camName = camName
        self.timeStamp = timeStamp
