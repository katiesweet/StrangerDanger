#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Reply import Reply


class RegisterReply(Reply):

    def __init__(self, success, processId):
        super(RegisterReply, self).__init__(success)
        self.processId = processId
