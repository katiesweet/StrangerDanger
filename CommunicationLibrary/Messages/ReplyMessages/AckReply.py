#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Reply import Reply


class AckReply(Reply):

    def __init__(self, success):
        super(AckReply, self).__init__(success)
