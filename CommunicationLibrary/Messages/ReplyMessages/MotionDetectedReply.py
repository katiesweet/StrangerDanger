#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Reply import Reply


class MotionDetectedReply(Reply):

    def __init__(self, success):
        super(MotionDetectedReply, self).__init__(success)
