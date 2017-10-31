#!/usr/bin
from AbstractMessages.Reply import Reply


class SyncDataReply(Reply):

    def __init__(self, success):
        super(SyncDataReply, self).__init__(success)
