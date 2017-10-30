#!/usr/bin
from AbstractMessages.Reply import Reply


class AliveReply(Reply):

    def __init__(self, success):
        super(AliveReply, self).__init__(success)
