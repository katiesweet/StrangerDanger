#!/usr/bin
from AbstractMessages.Reply import Reply

class RegisterReply(Reply):

    def __init__(self, messageId, conversationId, success, process):
        super(RegisterReply,self).__init__(messageId, conversationId, success)
        self.process = process
