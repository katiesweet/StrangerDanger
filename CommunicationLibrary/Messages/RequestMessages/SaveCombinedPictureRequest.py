#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request

class SaveCombinedPictureRequest(Request):

    def __init__(self, pictureInfo):
        super(SaveCombinedPictureRequest, self).__init__()
        self.pictureInfo = pictureInfo
