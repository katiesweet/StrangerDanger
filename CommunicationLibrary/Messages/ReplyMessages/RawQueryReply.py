#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Reply import Reply


class RawQueryReply(Reply):

    def __init__(self, success, data):
        super(RawQueryReply, self).__init__(success)
        # Data : [(camName, timestamp), (camName, timeStamp)...]
        self.data = data
