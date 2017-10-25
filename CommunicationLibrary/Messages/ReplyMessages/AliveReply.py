#!/usr/bin
from AbstractMessages.Reply import Reply

class AliveReply(Reply):

    def __init__(self, messageId, conversationId, success):
        super(AliveReply,self).__init__(messageId, conversationId, success)
