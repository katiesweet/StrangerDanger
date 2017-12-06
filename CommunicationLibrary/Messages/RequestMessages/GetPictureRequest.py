#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class GetPictureRequest(Request):

    def __init__(self, picLocation):
        super(GetPictureRequest, self).__init__()
        self.picLocation = picLocation
