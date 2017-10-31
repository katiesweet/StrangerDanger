#!/usr/bin
from AbstractMessages.Request import Request


class SaveMotionRequest(Request):

    def __init__(self, pictureInfo):
        super(SaveMotionRequest, self).__init__()
        self.pictureInfo = pictureInfo
