#!/usr/bin
from AbstractMessages.Reply import Reply

class MotionDetectedReply(Reply):

    def __init__(self, messageId, conversationId, success):
        super(MotionDetectedReply,self).__init__(messageId, conversationId, success)
