#!/usr/bin
from AbstractMessages.Reply import Reply

class LoginReply(Reply):

    def __init__(self, messageId, conversationId, success, process):
        super(LoginReply,self).__init__(messageId, conversationId, success)
        self.process = process
