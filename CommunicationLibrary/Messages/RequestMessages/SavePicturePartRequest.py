#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request

class SavePicturePartRequest(Request):

    def __init__(self, picturePart):
        super(SavePicturePartRequest, self).__init__()
        self.picturePart = picturePart
