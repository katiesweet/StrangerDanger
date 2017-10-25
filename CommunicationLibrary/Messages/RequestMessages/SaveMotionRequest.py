#!/usr/bin
from AbstractMessages.Request import Request

class SaveMotionRequest(Request):

    def __init__(self, messageId, conversationId, pictureInfo):
        super(SaveMotionRequest,self).__init__(messageId, conversationId)
        self.pictureInfo = pictureInfo
