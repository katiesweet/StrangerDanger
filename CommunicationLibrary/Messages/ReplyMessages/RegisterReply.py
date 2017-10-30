#!/usr/bin
from AbstractMessages.Reply import Reply


class RegisterReply(Reply):

    def __init__(self, success, process):
        super(RegisterReply, self).__init__(success)
        self.process = process
