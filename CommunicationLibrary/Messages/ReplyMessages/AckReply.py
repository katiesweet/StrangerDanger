#!/usr/bin
from AbstractMessages.Reply import Reply

class AckReply(Reply):

    def __init__(self, messageId, conversationId, success):
        super(AckReply,self).__init__(messageId, conversationId, success)
