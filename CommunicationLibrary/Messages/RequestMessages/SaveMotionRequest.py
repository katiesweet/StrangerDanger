#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class SaveMotionRequest(Request):

    def __init__(self, pictureInfo, cameraName):
        super(SaveMotionRequest, self).__init__()
        self.pictureInfo = pictureInfo
        self.cameraName = cameraName
