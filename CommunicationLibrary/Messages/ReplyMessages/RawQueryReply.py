#!/usr/bin
from AbstractMessages.Reply import Reply


class RawQueryReply(Reply):

    def __init__(self, success, data):
        super(RawQueryReply, self).__init__(success)
        self.data = data
