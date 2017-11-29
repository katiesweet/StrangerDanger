#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request

class SavePictureInfoRequest(Request):

    def __init__(self, numberOfParts, timeStamp, cameraName):
        super(SavePictureInfoRequest, self).__init__()
        self.numberOfParts = numberOfParts
        self.timeStamp = timeStamp
        self.cameraName = cameraName
