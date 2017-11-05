#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Reply import Reply


class LoginReply(Reply):

    def __init__(self, success, process):
        super(LoginReply, self).__init__(success)
        self.process = process
